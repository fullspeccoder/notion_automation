from notion_objs.notion_pages import NotionDatabase
from notion_objs.notion_props import NotionProperties, NotionSelectProperty, NotionUrlProperty, NotionMultiSelectProperty, NotionTitleProperty
from notion_objs.notion_blocks import NotionHeading, NotionDivider, NotionTodo, NotionParagraphBlock, NotionBulletedListItem, NotionNumberedListItem


class NotionRecipe(NotionDatabase):
    def __init__(self, db_id, emoji='🍕', children=[], cover_url='', category='', source_url='', tags=list(), youtube_url='', name="Recipe Name", instructions='', ingredients=dict()):
        super().__init__(db_id, emoji=emoji, children=children, cover_url=cover_url)
        self.properties = NotionProperties()
        # Category (Select Property)
        self.properties.add_property(
            NotionSelectProperty("Category", category))
        # Source URL (URL Property)
        self.properties.add_property(NotionUrlProperty(
            "Source URL", source_url))
        # Tags (Multi Select Property)
        self.properties.add_property(NotionMultiSelectProperty(
            "Tags", tags))
        # Youtube URL (URL Property)
        self.properties.add_property(NotionUrlProperty(
            "Youtube URL", youtube_url))
        # Name (Title Property)
        self.properties.add_property(NotionTitleProperty(
            name))
        self.properties = self.properties.to_dict()
        # Ingredients (Todo Blocks)

        self.children.append(NotionHeading(
            "1", "Ingredients", "orange_background"))
        self.children.append(NotionDivider())
        for key, value in ingredients.items():
            self.children.append(NotionTodo(f'{value} {key}'))
        self.children.append(NotionParagraphBlock(""))
        # Instructions (Textual Blocks)
        self.children.append(NotionHeading(
            "1", "Instructions", "green_background"))
        self.children.append(NotionDivider())
        for instruction_step in instructions.split("\r\n"):
            self.children.append(NotionNumberedListItem(instruction_step))
        self.children.append(NotionParagraphBlock(""))
        self.children.append(NotionHeading(
            "1", "Aspects to tweak next time", 'red_background'))
        self.children.append(NotionDivider())
        for _ in range(0, 3):
            self.children.append(NotionBulletedListItem(""))
        self.children.append(NotionParagraphBlock(""))
        self.children.append(NotionDivider())
