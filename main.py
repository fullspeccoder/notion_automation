import os
from dotenv import load_dotenv
from notion_client import Client
from notion_objs import NotionMultiSelectProperty, NotionStatusProperty, NotionProperties, NotionRichTextProperty, NotionTextProperty

load_dotenv()

client = Client(auth=os.getenv('NOTION_API_KEY'))

notion_t = NotionTextProperty('Name', "Jacob Wilson")
notion_rt = NotionRichTextProperty("Title", "Full Stack Engineer")
notion_st = NotionStatusProperty("Status", "Not started")
notion_se = NotionMultiSelectProperty("Multi-select", ["TypeScript", "Python"])
properties = [notion_t, notion_rt, notion_st, notion_se]

props = NotionProperties()

props.add_properties(properties)

props_obj = props.translate_to_json()

client.pages.create(parent={"type": "database_id", "database_id": os.getenv(
    'NOTION_DATABASE_ID')}, properties=props_obj)

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
