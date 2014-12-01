from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder, document, link, schemata
from zope.interface import implements
from interfaces import ITab, ITabDescription, ITabGroup, ITabLink
from config import PROJECTNAME

TabSchema = folder.ATFolderSchema.copy() + atapi.Schema((
))
TabDescriptionSchema = document.ATDocumentSchema.copy() + atapi.Schema((
))
TabGroupSchema = folder.ATFolderSchema.copy() + atapi.Schema((
))
TabLinkSchema = link.ATLinkSchema.copy() + atapi.Schema((
))

schemata.finalizeATCTSchema(TabSchema, folderish=True, moveDiscussion=False)
schemata.finalizeATCTSchema(TabDescriptionSchema, folderish=False, moveDiscussion=False)
schemata.finalizeATCTSchema(TabGroupSchema, folderish=True, moveDiscussion=False)
schemata.finalizeATCTSchema(TabLinkSchema, folderish=False, moveDiscussion=False)

class Tab(folder.ATFolder):
    implements(ITab)
    portal_type = 'Tab'
    schema = TabSchema

class TabDescription(document.ATDocument):
    implements(ITabDescription)
    portal_type = 'TabDescription'
    schema = TabDescriptionSchema

class TabGroup(folder.ATFolder):
    implements(ITabGroup)
    portal_type = 'TabGroup'
    schema = TabGroupSchema

class TabLink(link.ATLink):
    implements(ITabLink)
    portal_type = 'TabLink'
    schema = TabLinkSchema

atapi.registerType(Tab, PROJECTNAME)
atapi.registerType(TabDescription, PROJECTNAME)
atapi.registerType(TabGroup, PROJECTNAME)
atapi.registerType(TabLink, PROJECTNAME)
