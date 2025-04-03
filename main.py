import os
from dotenv import load_dotenv
from notion_client import Client
import notion_objs as NO
import notion_pages as NP

load_dotenv()

# client = Client(auth=os.getenv('NOTION_API_KEY'))

notion_t = NO.NotionTitleProperty('Name', "Jacob Wilson")
notion_rt = NO.NotionRichTextProperty("Title", "Full Stack Engineer")
notion_st = NO.NotionStatusProperty("Status", "Not started")
notion_se = NO.NotionMultiSelectProperty(
    "Multi-select", ["TypeScript", "Python"])
notion_cb = NO.NotionCheckboxProperty("I Died", True)
notion_cr_b = NO.NotionCreatedByProperty("Jacob Wilson")
notion_cr_t = NO.NotionCreatedTimeProperty("10:40")
notion_date = NO.NotionDateProperty("Start Date", "03-04-1996")
properties = [notion_t, notion_rt, notion_st, notion_se,
              notion_cb, notion_cr_b, notion_cr_t, notion_date]

props = NO.NotionProperties()

props.add_properties(properties)


# new_page.set_parent_page(os.getenv("NOTION_PAGE_ID"))
# new_page.set_parent_database(os.getenv("NOTION_DATABASE_ID"))
# new_page.set_cover("https://images.unsplash.com/photo-1501504905252-473c47e087f8?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
# new_page.set_icon("🐱")
# new_page.set_properties(props)

# client.pages.create(parent={"type": "database_id", "database_id": os.getenv(
#     'NOTION_DATABASE_ID')}, properties=props_obj)

# ARCHIVED CODE
# client.pages.create(parent={"type": "database_id", "database_id": os.getenv('NOTION_DATABASE_ID')}, properties={
#     "Name": {
#         "title": [
#             {
#                 "type": "text",
#                 "text": {
#                     "content": "Jacob Wilson"
#                 }
#             }
#         ]
#     },
#     "Title": {
#         "rich_text": [
#             {
#                 "type": "text",
#                 "text": {
#                     "content": "Full Stack Engineer"
#                 }
#             }
#         ]
#     },
#     "Status": {
#         "status": {
#             "name": "Not started"
#         }
#     },
#     "Multi-select": {
#         "multi_select": [
#             {
#                 "name": "TypeScript"
#             },
#             {
#                 "name": "Python"
#             }
#         ]
#     },
#     "Email": {
#         "email": "jcbwlsn04@gmail.com"
#     }
# })
