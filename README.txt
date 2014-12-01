This is a rewrite of the uwosh.intranet.tabs product that Nathan and I did. The
main reason for the rewrite was to use more built-in Plone things and do less
custom coding. This was because the old product was turning into a bit of a
mess, with a lot of code duplicating what Plone already does, and Kim did
not want to maintain it with both Nathan and I leaving.

This *new* product was created mostly by me (Marshall), but I probably stole 
a lot of stuff that Nathan did in the old product. Thus, he's partially 
responsible too.

The main purpose of this product is to allow creating, organizing, and displaying
tabs which contain groups of links. Our main use case for this is an intranet
home page that allows users to find links to other service that they frequently
use, or that they need to accomplish some process within the university. 

Here's an ascii mockup of how we want the tabs to look:
TabTitle
--------
Some *rich* descriptive text.
* Maybe a list
* Telling you what to do
-----------------    -----------------
| Group 1       |    | Group 2       |
| -------       |    | -------       |
| Link1         |    | Link3         |
| Link2         |    | Link4         |
-----------------    -----------------

Tabs are folders and contain TabGroups, TabLinks, and TabDescriptions. 
TabGroups are folders and only contain TabLinks
TabLinks are just Plone Link types
TabDescriptions are just Plone Document types

A Tab is built by doing catalog queries to get all of it's Group objects
and their contained Link objects. Only one TabDescription is allowed and it
is displayed at the top of the Tab. Everything is displayed in the order it is
in its parent folder.

The Tabs are listed in a viewlet that displays at the top of the Plone site.

Which Tabs are listed is determined by which Tabs a user has manually added
using the "Manage My Tabs" view (@@manage_tabs). Here users can add and remove
the Tabs that they want to appear at the top of the site. This preference
is stored in their member properties. Tabs can also show in the viewlet if
they have been suggested by a group that the user is a member of. The list of
suggested groups is stored in a group property as 
"uwosh_intrnaet_tabsredux_suggested_tabs".

At install time, a folder to contain the Tabs is created at the root of the 
site. This folder is simply called "Tabs". A content rule is also included
that moves any Tabs that are created to that folder.

That's about it I guess. If you have any questions email me at:
<marshall dot scorcio at gmail dot com>
