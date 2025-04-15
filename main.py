import json
from notion_page_builder import NotionPageBuilder

json_data = dict()

with open("schema.json", "r") as file:
    data = file.read()
    json_data = json.loads(data)

NotionPageBuilder(json_data)
