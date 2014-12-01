from Products.CMFCore.utils import getToolByName

def install(context):
    if not context.readDataFile('uwosh.intranet.tabsredux.txt'):
        return
    site = context.getSite()
    addGroupDataProperties(site)
    createTabsFolder(site)

def addGroupDataProperties(site):   
    gdt = getToolByName(site, 'portal_groupdata')
    if not gdt.hasProperty('uwosh_intranet_tabsredux_suggested_tabs'):
        gdt.manage_addProperty('uwosh_intranet_tabsredux_suggested_tabs', (), 'lines')

def createTabsFolder(site):
    id = 'tabs'
    if hasattr(site, id):
        return
    site.invokeFactory(type_name='Folder', id=id, title='Tabs')
    tabs_folder = site[id]
    pwt = getToolByName(site, 'portal_workflow')
    pwt.doActionFor(tabs_folder, 'publish')
    tabs_folder.reindexObject()
