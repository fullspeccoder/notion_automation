import os
from notion_client import Client
from notion_pages import NotionDatabase
from notion_blocks import *
from notion_props import *


class NotionCourse(NotionDatabase):
    def __init__(self, db_id, cover_url, name, instructor, instructor_email, course_code, syllabus_url, start_date, end_date, goals_list):
        super().__init__(db_id, emoji="🍎", cover_url=cover_url)
        self.properties = NotionProperties()
        # Name Property
        self.properties.add_property(NotionTitleProperty(name))
        # Instructor Property
        self.properties.add_property(
            NotionRichTextProperty("Instructor", instructor))
        # Instructor Email Property
        self.properties.add_property(NotionEmailProperty(
            "Instructor Email", instructor_email))
        # Credits Property
        self.properties.add_property(NotionNumberProperty("Credits", 3))
        # Start Date Property
        self.properties.add_property(
            NotionDateProperty("Start Date", start_date))
        # End Date Property
        self.properties.add_property(
            NotionDateProperty("End Date", end_date))
        # Difficult Property
        self.properties.add_property(
            NotionSelectProperty("Difficulty", "Easy"))
        # Status Property
        self.properties.add_property(NotionStatusProperty("In progress"))
        # Course Code Property
        self.properties.add_property(
            NotionRichTextProperty("Course Code", course_code))
        # Syllabus URL Property
        self.properties.add_property(NotionUrlProperty(
            "Syllabus", syllabus_url))
        self.properties = self.properties.to_dict()
        # Learning Goals Block
        self.children.append(NotionHeading(
            "1", "Learning Goals", "green_background"))
        self.children.append(NotionDivider())
        for goal in goals_list:
            self.children.append(NotionBulletedListItem(goal))
        self.children.append(NotionParagraphBlock(""))
        # Assignments Due Block
        self.children.append(NotionHeading(
            "1", "Assignments Due", "orange_background"))
        self.children.append(NotionDivider())
        # A Table that will be made later
        self.children.append(NotionParagraphBlock(""))
        # Feedback From Assignments Block.
        self.children.append(NotionHeading(
            "1", "Feedback From Assignments", "blue_background"))
        self.children.append(NotionDivider())
