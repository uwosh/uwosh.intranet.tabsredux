from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TabView(BrowserView):

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def path(self):
        return '/'.join(self.context.getPhysicalPath())

    @property
    def description(self):
        brains = self.catalog.searchResults(
                     portal_type='TabDescription', 
                     path=self.path) 
        if len(brains) < 1:
            return ''
        else:
            obj = brains[0].getObject()
            text = obj.getText()
            return text.decode('utf-8')
            
    @property
    def groups(self):
        groups = []
        group_brains = self.catalog.searchResults(
                           portal_type='TabGroup', 
                           path=self.path, 
                           sort_on='getObjPositionInParent') 
        for brain in group_brains:
            group = {'id':brain.id, 'title':brain.Title, 'path':brain.getPath()}
            groups.append(group)
        for group in groups:
            links = []
            link_brains = self.catalog.searchResults(
                              portal_type='TabLink', 
                              path=group['path'], 
                              sort_on='getObjPositionInParent') 
            for brain in link_brains:
                link = {'id':brain.id, 'title':brain.Title, 'url':brain.getRemoteUrl}
                links.append(link)
            group['links'] = links
        if len(self.ungrouped_links) > 0:
            ungrouped = {'id':'ungrouped-links', 'title':'Ungrouped Links', 'links':self.ungrouped_links}
            groups.append(ungrouped)
        return groups
        
    @property
    def ungrouped_links(self):
        links = []
        brains = self.catalog.searchResults(
                     portal_type='TabLink',
                     path={'query':self.path, 'depth':1},
                     sort_on='getObjPositionInParent')
        for brain in brains:
            link = {'id':brain.id, 'title':brain.Title, 'url':brain.getRemoteUrl}
            links.append(link)
        return links
        
class ManageMemberTabsMixin(object):

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def member_tool(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def group_tool(self):
        return getToolByName(self.context, 'portal_groups')

    def get_tabs_to_show(self):
        if self.member_tool.isAnonymousUser():
            return self.get_all_tabs() # XXX: probably want to return a default set of tabs
        member = self.member_tool.getAuthenticatedMember()
        added_tabs = set(member.getProperty('uwosh_intranet_tabsredux_added_tabs', ()))
        hidden_tabs = set(member.getProperty('uwosh_intranet_tabsredux_hidden_tabs', ()))
        groups = [self.group_tool.getGroupById(id) for id in self.group_tool.getGroupsForPrincipal(member)]
        suggested_tabs = set()
        for group in [g for g in groups if g]:
            suggested = group.getProperty('uwosh_intranet_tabsredux_suggested_tabs', ())
            for tab in suggested:
                suggested_tabs.add(tab)            
        visible_tabs = list((suggested_tabs - hidden_tabs) | added_tabs)
        brains = self.catalog.searchResults(id=visible_tabs, portal_type='Tab', sort_on='id')
        return [{'id':brain.id, 'title':brain.Title, 'url':brain.getURL()} for brain in brains]

    def get_all_tabs(self):
        brains = self.catalog.searchResults(portal_type='Tab', sort_on='id')
        return [{'id':brain.id, 'title':brain.Title, 'url':brain.getURL()} for brain in brains]
        
    def show_tab(self, tab_id):
        if self.member_tool.isAnonymousUser():
            return
        member = self.member_tool.getAuthenticatedMember()
        added_tabs = list(member.getProperty('uwosh_intranet_tabsredux_added_tabs', ()))
        if tab_id not in added_tabs:
            added_tabs.append(tab_id)
            member.setMemberProperties({'uwosh_intranet_tabsredux_added_tabs': tuple(added_tabs)})
    
    def hide_tab(self, tab_id):
        if self.member_tool.isAnonymousUser():
            return
        member = self.member_tool.getAuthenticatedMember()
        added_tabs = list(member.getProperty('uwosh_intranet_tabsredux_added_tabs', ()))
        hidden_tabs = list(member.getProperty('uwosh_intranet_tabsredux_hidden_tabs', ()))
        if tab_id in added_tabs:
            added_tabs.remove(tab_id)
        if tab_id not in hidden_tabs:
            hidden_tabs.append(tab_id)
        member.setMemberProperties({'uwosh_intranet_tabsredux_added_tabs': tuple(added_tabs),
                                    'uwosh_intranet_tabsredux_hidden_tabs': tuple(hidden_tabs)})

class TabsViewlet(ViewletBase, ManageMemberTabsMixin):

    render = ViewPageTemplateFile('tabs_viewlet.pt')

    def update(self):
        super(TabsViewlet, self).update()
        self.is_anonymous_user = bool(self.member_tool.isAnonymousUser())
        self.tabs = self.get_tabs_to_show()
        
class ManageTabsView(BrowserView, ManageMemberTabsMixin):     

    @property
    def my_tabs(self):
        return self.get_tabs_to_show()
        
    @property
    def all_tabs(self):
        return self.get_all_tabs()
        
    def remove_from_my_tabs(self):
        tab_id = self.request.get('tab', '')
        if not tab_id:
            raise ValueError('The required argument "tab" was missing from the request.')
        self.hide_tab(tab_id)
        self.request.response.redirect(self.context.absolute_url() + '/@@manage_tabs')
        
    def add_to_my_tabs(self):
        tab_id = self.request.get('tab', '')
        if not tab_id:
            raise ValueError('The required argument "tab" was missing from the request.')
        self.show_tab(tab_id)
        self.request.response.redirect(self.context.absolute_url() + '/@@manage_tabs')
        