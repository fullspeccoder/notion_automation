'''notion_props.py

This module provides an abstraction for Notion properties, simplifying interactions
with Notion's API.

By reducing complexity, it enhances code readability, minimizes the effort needed
to define properties, and accelerates workflow automation.

Includes:
    - Notion property creation
    - Notion Property management
    - Ease of conversion into Notion api

Example:
    >>> from notion_props import *
    >>> title_prop = NotionTitleProperty("Title", "Recipe Name")
    >>> recipe_props = NotionProperties()
    >>> recipe_props.add_property(title_prop)
'''


class NotionProperties:
    """Represents a collection of Notion property objects for a page.

    This class acts as a container and manager for Notion property components,
    providing methods to add individual or multiple properties and convert them
    into a dictionary format suitable for the Notion API.

    Attributes:
        properties (list): A list of JSON-like property dictionaries.

    Example:
        >>> title = NotionTitleProperty("Name", "My Task")
        >>> date = NotionDateProperty("Due Date", "2025-04-03")
        >>> props = NotionProperties()
        >>> props.add_property(title)
        >>> props.add_property(date)
        >>> notion_payload = props.to_dict()
    """

    def __init__(self):
        """Initializes an empty NotionProperties container."""
        self.properties = list()

    def add_property(self, prop: NotionProperty) -> None:
        """Adds a single NotionProperty object to the properties list.

        Args:
            prop (NotionProperty): The property object to add.

        Raises:
            TypeError: If `prop` is not an instance of NotionProperty.
        """

        if not isinstance(prop, NotionProperty):
            raise TypeError(
                f'Expected a NotionProperty Object, got {type(prop).__name__}')

        self.properties.append(prop.to_json())

    def add_properties(self, props: list) -> None:
        """Adds multiple NotionProperty objects to the properties list.

        Args:
            props (list): A list of NotionProperty objects.

        Raises:
            TypeError: If `props` is not a list of NotionProperty objects.
        """
        if not isinstance(props, list):
            raise TypeError(
                f'Expected a list of NotionProperty Objects, got {type(props).__name__}')

        self.properties = props

    def to_dict(self) -> dict:
        """Converts the stored properties into a dictionary.

        Returns:
            dict: A dictionary of Notion properties formatted for the Notion API.
        """
        obj = {}
        for prop in self.properties:
            obj.update(prop)

        return obj


class NotionProperty:
    """Base class for all Notion property types.

    This class provides a base structure for other Notion property classes to inherit from.
    It stores the property name and the data structure (`content`) used to represent the
    property in Notion's API format.

    Subclasses must define `self.content` in their constructors to be usable.

    Attributes:
        prop_name (str): The name of the Notion property (used as the key in the final output).
        content (dict): A dictionary representing the Notion property structure.

    Example:
        >>> class MyCustomProperty(NotionProperty):
        ...     def __init__(self, prop_name, value):
        ...         super().__init__(prop_name)
        ...         self.content = {"custom_type": value}

        >>> prop = MyCustomProperty("Demo", 123)
        >>> prop.to_json()
        {
            "Demo": {
                "custom_type": 123
            }
        }
    """

    def __init__(self, prop_name: str):
        """Initializes a base NotionProperty.

        Args:
            prop_name (str): The name/key for the Notion property.
        """
        self.prop_name = prop_name
        self.content = dict()

    def to_json(self) -> dict:
        """Converts the property into Notion-compatible JSON.

        Returns:
            dict: A dictionary representing the Notion property in API format.
        """
        return {self.prop_name: self.content}


class NotionCheckboxProperty(NotionProperty):
    """Represents a Notion Checkbox Property.

    Used to create a checkbox property in a Notion page, allowing for boolean
    values (checked or unchecked) to be stored.

    Attributes:
        prop_name (str): The name of the checkbox property.
        content (bool): A boolean value indicating whether the checkbox is checked.

    Example:
        >>> checkbox = NotionCheckboxProperty("Completed", True)
    """

    def __init__(self, prop_name: str, content: bool):
        """Initializes a NotionCheckboxProperty.

        Args:
            prop_name (str): The name of the checkbox property.
            content (bool): A boolean indicating if the checkbox is checked.

        Raises:
            TypeError: If `content` is not a boolean.
        """
        if not isinstance(content, bool):
            raise TypeError(
                f'Expected a boolean, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'checkbox': content
        }


class NotionCreatedByProperty(NotionProperty):
    """Represents a Notion 'Created By' property.

    !!! WARNING: This property is set automatically by Notion and is read-only.

    Allows the user to supply a plain string to represent the person who created the page.
    Internally converts it into the correct structure for Notion's API.

    Attributes:
        content (str): The plain string name of the creator.

    Example:
        >>> prop = NotionCreatedByProperty("John Smith")
        >>> prop.to_json()
        {
            "Created By": {
                "created_by": "John Smith"
            }
        }
    """

    def __init__(self, content):
        """Initializes the CreatedBy property using a plain name string.

        Args:
            content (str): The name of the person who created the page.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__("Created By")
        self.content = {
            'created_by': content
        }


class NotionCreatedTimeProperty(NotionProperty):
    """Represents a Notion 'Created Time' property.

    !!! DO NOT USE - Notion SETS THIS PROPERTY FOR YOU UPON PAGE CREATION !!!

    Accepts a plain timestamp string from the user and wraps it in the correct
    Notion format for display or reference.

    Attributes:
        prop_name (str): The property name (always "Created At").
        content (str): A plain timestamp string.

    Example:
        >>> prop = NotionCreatedTimeProperty("02/03/1996")
        >>> prop.to_json()
        {
            "Created At": {
                "created_time": "02/03/1996"
            }
        }
    """

    def __init__(self, content: str):
        """Initializes the CreatedTime property with a raw string timestamp.

        Args:
            content (str): A readable timestamp string.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__("Created At")
        self.content = {
            'created_time': content
        }


class NotionDateProperty(NotionProperty):
    """Represents a Notion Date Property.

    Allows users to pass a plain date string (e.g. "02/03/1996") and converts it
    into the proper Notion format.

    Attributes:
        prop_name (str): The name of the property (e.g. "Birthday").
        content (str): The raw date string provided by the user.

    Example:
        >>> prop = NotionDateProperty("Birthday", "02/03/1996")
        >>> prop.to_json()
        {
            "Birthday": {
                "date": "02/03/1996"
            }
        }
    """

    def __init__(self, prop_name: str, content: str):
        """Initializes a Notion date property using a readable date string.

        Args:
            prop_name (str): The name of the date field.
            content (str): A date string in any expected user format.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'date': content
        }


class NotionEmailProperty(NotionProperty):
    """Represents a Notion Email Property.

    Allows users to supply a raw email address string, and wraps it in the correct
    Notion API format for use in database properties.

    Attributes:
        prop_name (str): The name of the property (e.g. "Contact").
        content (str): The email address.

    Example:
        >>> prop = NotionEmailProperty("Email", "example@email.com")
        >>> prop.to_json()
        {
            "Email": {
                "email": "example@email.com"
            }
        }
    """

    def __init__(self, prop_name: str, content: str):
        """Initializes an Email property using a plain email string.

        Args:
            prop_name (str): The name of the email property.
            content (str): The raw email address.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'email': content
        }


class NotionFilesProperty(NotionProperty):
    """Represents a Notion Files Property.

    !!! WARNING: Notion's API does not support creating files via this property yet.

    Wraps a plain filename string into a property structure. Intended for future use or
    reading existing file properties.

    Attributes:
        prop_name (str): The name of the property.
        content (str): The filename or file reference as a string.

    Example:
        >>> prop = NotionFilesProperty("Upload", "resume.pdf")
        >>> prop.to_json()
        {
            "Upload": {
                "files": "resume.pdf"
            }
        }
    """

    def __init__(self, prop_name: str, content: str):
        """Initializes a Files property using a filename string.

        Args:
            prop_name (str): The name of the files property.
            content (str): The raw file name or reference.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'files': content
        }


class NotionFormulaProperty(NotionProperty):
    """Represents a Notion Formula Property.

    Accepts a plain formula expression string and wraps it into the required format
    for Notion’s formula field.

    Attributes:
        prop_name (str): The name of the property (e.g. "Total").
        content (str): A string formula expression.

    Example:
        >>> prop = NotionFormulaProperty("Formula", "prop(\"Price\") * prop(\"Quantity\")")
        >>> prop.to_json()
        {
            "Formula": {
                "formula": {
                    "expression": "prop(\"Price\") * prop(\"Quantity\")"
                }
            }
        }
    """

    def __init__(self, prop_name: str, expression: str):
        """Initializes a Formula property using a plain expression string.

        Args:
            prop_name (str): The name of the formula property.
            expression (str): The raw formula expression string.

        Raises:
            TypeError: If `expression` is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError(
                f'Expected a string, got {type(expression).__name__}')

        super().__init__(prop_name)
        self.content = {
            'formula': {
                'expression': expression
            }
        }


class NotionLastEditedByProperty(NotionProperty):
    """Represents a Notion 'Last Edited By' property.

    !!! WARNING: This property is automatically set by Notion and cannot be modified.

    Accepts a plain name string representing the last editor of the page. This class is
    best used for display or read-only purposes.

    Attributes:
        prop_name (str): The name of the property.
        content (str): The name of the last editor.

    Example:
        >>> prop = NotionLastEditedByProperty("Last Editor", "Jane Doe")
        >>> prop.to_json()
        {
            "Last Editor": {
                "last_edited_by": "Jane Doe"
            }
        }
    """

    def __init__(self, prop_name: str, content: str):
        """Initializes a LastEditedBy property using a raw name string.

        Args:
            prop_name (str): The name of the property.
            content (str): The name of the person who last edited the page.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'last_edited_by': content
        }


class NotionLastEditedTimeProperty(NotionProperty):
    """Represents a Notion 'Last Edited Time' property.

    !!! WARNING: This property is set automatically by Notion and is read-only.

    Accepts a plain date/time string and wraps it in the Notion format.

    Attributes:
        prop_name (str): The name of the property.
        content (str): The last edited timestamp.

    Example:
        >>> prop = NotionLastEditedTimeProperty("Edited", "04/03/2025 2:30 PM")
        >>> prop.to_json()
        {
            "Edited": {
                "lastEditedTime": "04/03/2025 2:30 PM"
            }
        }
    """

    def __init__(self, prop_name: str, time: str):
        """Initializes a LastEditedTime property using a raw string.

        Args:
            prop_name (str): The name of the property.
            time (str): A plain date/time string.

        Raises:
            TypeError: If `time` is not a string.
        """
        if not isinstance(time, str):
            raise TypeError(
                f'Expected a string, got {type(time).__name__}')

        super().__init__(prop_name)
        self.content = {
            'lastEditedTime': time
        }


class NotionMultiSelectProperty(NotionProperty):
    """Represents a Notion Multi-Select Property.

    Accepts a list of tags (as strings) and wraps them as multi-select options in the
    correct Notion format.

    Attributes:
        prop_name (str): The name of the multi-select property.
        content (list[str]): A list of option names.

    Example:
        >>> prop = NotionMultiSelectProperty("Tags", ["Python", "API", "Automation"])
        >>> prop.to_json()
        {
            "Tags": {
                "multi_select": {
                    "options": [
                        {"name": "Python"},
                        {"name": "API"},
                        {"name": "Automation"}
                    ]
                }
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Multi-Select property using a list of tags.

        Args:
            prop_name (str): The name of the property.
            content (list): A list of strings representing selected options.

        Raises:
            TypeError: If `content` is not a list of strings.
        """
        if not isinstance(content, list):
            raise TypeError(
                f'Expected a list of strings, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'multi_select': [{'name': selected_name} for selected_name in content]
        }


class NotionNumberProperty(NotionProperty):
    """Represents a Notion Number Property.

    Accepts a plain number (int or float) and wraps it for Notion API usage.

    Attributes:
        prop_name (str): The name of the number property.
        content (int | float): A numeric value.

    Example:
        >>> prop = NotionNumberProperty("Score", 95.5)
        >>> prop.to_json()
        {
            "Score": {
                "number": 95.5
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Number property using a plain number.

        Args:
            prop_name (str): The name of the property.
            content (int | float): The numeric value.

        Raises:
            TypeError: If `content` is not a number.
        """
        if not isinstance(content, float) or not isinstance(content, int):
            raise TypeError(
                f'Expected a number, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'number': content
        }


class NotionPeopleProperty(NotionProperty):
    """Represents a Notion People Property.

    Accepts a list of plain names or user references, abstracting away the
    API structure required by Notion for people fields.

    Attributes:
        prop_name (str): The name of the people property.
        content (list[str]): A list of people/user names.

    Example:
        >>> prop = NotionPeopleProperty("Team", ["Alice", "Bob"])
        >>> prop.to_json()
        {
            "Team": {
                "people": ["Alice", "Bob"]
            }
        }
    """

    def __init__(self, prop_name, people):
        """Initializes a People property using a list of names or user references.

        Args:
            prop_name (str): The name of the property.
            people (list[str]): A list of people names or identifiers.

        Raises:
            TypeError: If `people` is not a list of strings.
        """
        if not isinstance(people, float) or not isinstance(people, int):
            raise TypeError(
                f'Expected a list of strings, got {type(people).__name__}')

        super().__init__(prop_name)
        self.content = {
            'people': people
        }


class NotionPhoneNumberProperty(NotionProperty):
    """Represents a Notion Phone Number Property.

    Accepts a plain phone number string and wraps it for use in Notion’s API.

    Attributes:
        prop_name (str): The name of the phone number property.
        content (str): A raw phone number string.

    Example:
        >>> prop = NotionPhoneNumberProperty("Phone", "(555) 123-4567")
        >>> prop.to_json()
        {
            "Phone": {
                "phone_number": "(555) 123-4567"
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Phone Number property using a raw number string.

         Args:
             prop_name (str): The name of the property.
             content (str): The phone number.

         Raises:
             TypeError: If `content` is not a string.
         """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'phone_number': content
        }


class NotionRelationProperty(NotionProperty):
    """Represents a Notion Relation Property.

    Accepts a plain string representing a related page ID or value,
    and wraps it for Notion's relation field.

    Attributes:
        prop_name (str): The name of the relation property.
        content (str): The ID or label of the related item.

    Example:
        >>> prop = NotionRelationProperty("Related Task", "abc123-task-id")
        >>> prop.to_json()
        {
            "Related Task": {
                "phone_number": "abc123-task-id"
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Relation property using a related ID or label.

        Args:
            prop_name (str): The name of the property.
            content (str): The related page identifier or reference.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'relation': content
        }


class NotionRichTextProperty(NotionProperty):
    """Represents a Notion Rich Text Property.

    Accepts a plain string and wraps it as rich text for use in Notion databases.

    Attributes:
        prop_name (str): The name of the rich text property.
        content (str): A plain string of text.

    Example:
        >>> prop = NotionRichTextProperty("Note", "Remember to follow up")
        >>> prop.to_json()
        {
            "Note": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Remember to follow up"
                        }
                    }
                ]
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Rich Text property using a plain string.

        Args:
            prop_name (str): The name of the property.
            content (str): The text content.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {'rich_text': [
            {'type': "text", "text": {"content": content}}]}


class NotionRollupProperty(NotionProperty):
    """Represents a Notion Rollup Property.

    !!! WARNING: Cannot be used to create new pages via API — read-only.

    Accepts a plain string representing the rolled-up content for display purposes.

    Attributes:
        prop_name (str): The name of the rollup property.
        content (str): The rolled-up value as a string.

    Example:
        >>> prop = NotionRollupProperty("Total Sales", "$1,250")
        >>> prop.to_json()
        {
            "Total Sales": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "$1,250"
                        }
                    }
                ]
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Rollup property using plain string content.

        Args:
            prop_name (str): The name of the property.
            content (str): The display value of the rollup.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {'rich_text': [
            {'type': "text", "text": {"content": content}}]}


class NotionSelectProperty(NotionProperty):
    """Represents a Notion Select Property.

    Accepts a list with a single string value representing the selected option.
    Internally wraps it in the correct format for Notion’s select fields.

    Attributes:
        prop_name (str): The name of the select property.
        content (list[str]): A single-item list representing the selected option.

    Example:
        >>> prop = NotionSelectProperty("Priority", ["High"])
        >>> prop.to_json()
        {
            "Priority": {
                "select": {
                    "options": [{"name": "High"}]
                }
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Select property using a single-option list.

        Args:
            prop_name (str): The name of the select field.
            content (str): A str with one string as the selected option.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a str, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            "select": {
                "name": content
            }
        }
        print(self.content)


class NotionStatusProperty(NotionProperty):
    """Represents a Notion Status Property.

    Accepts a plain string that matches a predefined status name in Notion,
    and wraps it accordingly.

    Attributes:
        prop_name (str): The name of the status property.
        content (str): The selected status.

    Example:
        >>> prop = NotionStatusProperty("Stage", "In Progress")
        >>> prop.to_json()
        {
            "Stage": {
                "status": {
                    "name": "In Progress"
                }
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Status property using a plain string.

        Args:
            prop_name (str): The name of the property.
            content (str): The selected status name.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            "status": {
                "name": content
            }
        }


class NotionTitleProperty(NotionProperty):
    """Represents a Notion Title Property.

    Accepts a plain string and formats it as a title object for Notion.
    This is the main field used as the page title in most databases.

    Attributes:
        prop_name (str): The name of the title property.
        content (str): The title content.

    Example:
        >>> prop = NotionTitleProperty("Name", "My First Project")
        >>> prop.to_json()
        {
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "My First Project"
                        }
                    }
                ]
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a Title property using a plain string.

        Args:
            prop_name (str): The name of the property.
            content (str): The title text.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            "type": "title",
            'title': [
                {
                    'type': "text",
                    "text": {
                        "content": content
                    }
                }
            ]
        }

    def __str__(self):
        return f"{self.prop_name}: {self.content}"


class NotionUrlProperty(NotionProperty):
    """Represents a Notion URL Property.

    Accepts a plain URL string and formats it for use in Notion database properties.

    Attributes:
        prop_name (str): The name of the URL property.
        content (str): The URL string.

    Example:
        >>> prop = NotionUrlProperty("Website", "https://example.com")
        >>> prop.to_json()
        {
            "Website": {
                "url": "https://example.com"
            }
        }
    """

    def __init__(self, prop_name, content):
        """Initializes a URL property using a plain string.

        Args:
            prop_name (str): The name of the property.
            content (str): The URL value.

        Raises:
            TypeError: If `content` is not a string.
        """
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'url': content
        }

    def __str__(self):
        return f"{self.prop_name}: {self.content}"
