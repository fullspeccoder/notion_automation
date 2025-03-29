"""
This module provides an abstraction for Notion properties, simplifying interactions
with Notion's API.

By reducing complexity, it enhances code readability, minimizes the effort needed
to define properties, and accelerates workflow automation.
"""


class NotionProperties:
    '''
    Represents notion properties for a page.

    Attributes:
        properties (list): The list of properties of a page

    Methods:
        add_property(): Adds a NotionProperty Object to list
        add_properties(): Adds multiple NotionProperty Objects to list
        translate_to_json(): Converts object into readable Notion Client data.
    '''

    def __init__(self):
        """
        Initializes a NotionProperties object.
        """
        self.properties = list()

    def add_property(self, prop):
        """
        Adds a NotionProperty Object to properties attribute.

        Params:
            property (NotionProperty): NotionProperty object or subclasses.
        """
        if not isinstance(prop, NotionProperty):
            raise TypeError(
                f'Expected a NotionProperty Object, got {type(prop).__name__}')

        self.properties.append(prop.to_json())

    def add_properties(self, props):
        """
        Adds multiple NotionProperty Objects to properties attribute.

        Params:
            properties (list[<NotionProperty>]): List of NotionProperty objects or subclasses.
        """
        if not isinstance(props, list):
            raise TypeError(
                f'Expected a list of NotionProperty Objects, got {type(props).__name__}')

        self.properties = props

    def translate_to_json(self):
        """
        Converts NotionProperties Object to json format for Notion Client.

        Returns:
            Returns properties object for Notion Client.
        """
        obj = {}
        for prop in self.properties:
            obj.update(prop.to_json())

        return obj


class NotionProperty:
    '''
    General Class for Property Creation
    '''

    def __init__(self, prop_name):
        self.prop_name = prop_name
        self.content = dict()

    def to_json(self):
        '''
        Converts object to json format

        Returns:
            Returns this instance of object in json format
        '''
        return {self.prop_name: self.content}


class NotionTextProperty(NotionProperty):
    '''
    Notion Text Property object. Allows for simple text to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for text content. 

        This class instantiates a Notion Text Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionTextProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
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


class NotionRichTextProperty(NotionProperty):
    '''
    Notion Text Property object. Allows for simple text to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for rich text content. 

        This class instantiates a Notion Rich Text Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionRichTextProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'rich_text': [
                {
                    'type': "text",
                    "text": {
                        "content": content
                    }
                }
            ]
        }


class NotionStatusProperty(NotionProperty):
    '''
    Notion Status Property object. Allows for a status to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for status content. 

        This class instantiates a Notion Status Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionStatusProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            "status": {
                "name": content
            }
        }


class NotionMultiSelectProperty(NotionProperty):
    '''
    Represents a Notion MultiSelect Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of multi select properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (list[str]): A list of strings that represent tags.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Multi Select content. 

        This class instantiates a Notion Multi Select Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionMultiSelectProperty object
        '''
        if not isinstance(content, list):
            raise TypeError(
                f'Expected a list of strings, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'multi_select': [{'name': selected_name} for selected_name in content]
        }
