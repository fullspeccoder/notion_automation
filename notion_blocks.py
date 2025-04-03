import os
from dotenv import load_dotenv
from notion_client import Client
from notion_pages import *
from notion_props import *


class NotionBlock:
    def __init__(self, type):
        self.type = type
        self.content = dict()

    def to_dict(self):
        return {"object": "block", "type": self.type, self.type: self.content}


class NotionHeading(NotionBlock):
    def __init__(self, type, text, color="default"):
        super().__init__(f"heading_{type}")
        self.content = {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }
            ],
            "color": color,
            "is_toggleable": False
        }


class NotionDivider(NotionBlock):
    def __init__(self):
        super().__init__('divider')
        self.content = {}


class NotionBulletedListItem(NotionBlock):
    def __init__(self, text, color='default'):
        super().__init__('bulleted_list_item')
        self.content = {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }
            ],
            "color": color
        }


class NotionNumberedListItem(NotionBlock):
    def __init__(self, text, color='default'):
        super().__init__('numbered_list_item')
        self.content = {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }
            ],
            "color": color
        }


class NotionTodo(NotionBlock):
    def __init__(self, text, color="default", checked=False):
        super().__init__("to_do")
        self.content = {
            "rich_text": [{
                "type": "text",
                "text": {
                        "content": text,
                        "link": None
                }
            }],
            "checked": checked,
            "color": color,
        }


load_dotenv()

client = Client(auth=os.getenv('NOTION_API_KEY'))

page = client.pages.retrieve(os.getenv("NOTION_PAGE_ID"))
client.pages.update(page_id=os.getenv("NOTION_PAGE_ID"),
                    properties=NotionTitleProperty("title", "Books").to_dict())
page_id = page['id']
divider = NotionDivider().to_dict()
heading = NotionHeading("1", "Ingredients", "orange_background").to_dict()
todo = NotionTodo("1 Loaf Italian Bread").to_dict()
heading2 = NotionHeading("1", "Instructions", "green_background").to_dict()
number_list_item = NotionNumberedListItem(
    "Instruction1").to_dict()
heading3 = NotionHeading(
    '1', 'Aspects to tweak next time', 'red_background').to_dict()
bulleted_list_item = NotionBulletedListItem("some item").to_dict()


# client.blocks.children.append(block_id=page_id, children=[
#                               heading,
#                               divider,
#                               todo,
#                               todo,
#                               todo,
#                               todo,
#                               todo,
#                               todo,
#                               todo,
#                               heading2,
#                               divider,
#                               number_list_item,
#                               number_list_item,
#                               number_list_item,
#                               heading3,
#                               bulleted_list_item,
#                               bulleted_list_item,
#                               bulleted_list_item,
#                               divider,
#                               ])
