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

    def to_dict(self):
        """
        Converts NotionProperties Object to json format for Notion Client.

        Returns:
            Returns properties object for Notion Client.
        """
        obj = {}
        for prop in self.properties:
            obj.update(prop.to_dict())

        return obj


class NotionProperty:
    '''
    General Class for Property Creation
    '''

    def __init__(self, prop_name):
        self.prop_name = prop_name
        self.content = dict()

    def to_dict(self):
        '''
        Converts object to json format

        Returns:
            Returns this instance of object in json format
        '''
        return {self.prop_name: self.content}


class NotionCheckboxProperty(NotionProperty):
    '''
    Represents a Notion Checkbox Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of checkbox properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (bool): A boolean value that represents whether the box 
        is checked or unchecked (True or False).
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Checkbox content. 

        This class instantiates a Notion Checkbox Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionCheckboxProperty object
        '''
        if not isinstance(content, bool):
            raise TypeError(
                f'Expected a boolean, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'checkbox': content
        }


class NotionCreatedByProperty(NotionProperty):
    '''
    !!! DO NOT USE - Notion SETS THIS PROPERTY FOR YOU UPON PAGE CREATION !!!

    Represents a Notion Created By Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of created by properties in Notion Pages.

    Attributes:
        content (str): A string that represents the user that created the page.
    '''

    def __init__(self, content):
        '''
        Creates a Notion property for Created By content. 

        This class instantiates a Notion Created By Property for a Notion client. 

        Parameters:
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionCreatedByProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__("Created By")
        self.content = {
            'created_by': content
        }


class NotionCreatedTimeProperty(NotionProperty):
    '''
    !!! DO NOT USE - Notion SETS THIS PROPERTY FOR YOU UPON PAGE CREATION !!!

    Represents a Notion Created Time Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of created time properties in Notion Pages.

    Attributes:
        content (str): A string that represents a created time of page.
    '''

    def __init__(self, content):
        '''
        Creates a Notion property for Created Time content. 

        This class instantiates a Notion Created Time Property for a Notion client. 

        Parameters:
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionCreatedTimeProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__("Created At")
        self.content = {
            'created_time': content
        }


class NotionDateProperty(NotionProperty):
    '''
    Represents a Notion Date Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of date properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (str): A string that represent a date.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Date content. 

        This class instantiates a Notion Date Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionDateProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'date': content
        }


class NotionEmailProperty(NotionProperty):
    '''
    Represents a Notion Email Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of email properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (string): A string value that represent an email.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Email content. 

        This class instantiates a Notion Email Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionEmailProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'email': content
        }


class NotionFilesProperty(NotionProperty):
    '''
    !!! DO NOT USE, NOTION API DOES NOT SUPPORT THIS YET !!!
    Represents a Notion Files Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of files properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (str): A string value that represent the file name.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Files content. 

        This class instantiates a Notion Files Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionFilesProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'files': content
        }


class NotionFormulaProperty(NotionProperty):
    '''
    Represents a Notion Formula Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of formula properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        expression (calculation): A calculation to be handed into property.
    '''

    def __init__(self, prop_name, expression):
        '''
        Creates a Notion property for Formula content. 

        This class instantiates a Notion Formula Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionFormulaProperty object
        '''
        # if not isinstance(content, str):
        #     raise TypeError(
        #         f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'formula': {
                'expression': expression
            }
        }


class NotionLastEditedByProperty(NotionProperty):
    '''
    !!! DO NOT USE; RESULTS IN ERROR IN PAGE CREATION !!!

    Represents a Notion LastEditedBy Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of last edited by properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (str): A str that represents the last person who edited the page.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for LastEditedBy content. 

        This class instantiates a Notion LastEditedBy Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionLastEditedByProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'last_edited_by': content
        }


class NotionLastEditedTimeProperty(NotionProperty):
    '''
    !!! DO NOT USE; RESULTS IN ERROR IN PAGE CREATION !!!

    Represents a Notion LastEditedTime Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of last edited time properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        time (str): A str that represents the last time this page was edited.
    '''

    def __init__(self, prop_name, time):
        '''
        Creates a Notion property for LastEditedTime content. 

        This class instantiates a Notion LastEditedTime Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionLastEditedTimeProperty object
        '''
        if not isinstance(time, str):
            raise TypeError(
                f'Expected a string, got {type(time).__name__}')

        super().__init__(prop_name)
        self.content = {
            'lastEditedTime': time
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
            'multi_select': {"options": [{'name': selected_name} for selected_name in content]}
        }


class NotionNumberProperty(NotionProperty):
    '''
    Represents a Notion Number Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of number properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (int | float): A number to represent the number property.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Number content. 

        This class instantiates a Notion Number Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionNumberProperty object
        '''
        if not isinstance(content, float) or not isinstance(content, int):
            raise TypeError(
                f'Expected a number, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'number': content
        }


class NotionPeopleProperty(NotionProperty):
    '''
    Represents a Notion People Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of people properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (list[str]): A list of strings representing mentions of a user in the page.
    '''

    def __init__(self, prop_name, people):
        '''
        Creates a Notion property for People content. 

        This class instantiates a Notion People Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionPeopleProperty object
        '''
        if not isinstance(people, float) or not isinstance(people, int):
            raise TypeError(
                f'Expected a list of strings, got {type(people).__name__}')

        super().__init__(prop_name)
        self.content = {
            'people': people
        }


class NotionPhoneNumberProperty(NotionProperty):
    '''
    Represents a Notion PhoneNumber Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of phone number properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (str): A string to represent a phone number in the page.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Phone Number content. 

        This class instantiates a Notion Phone Number Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionPhoneNumberProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'phone_number': content
        }


class NotionRelationProperty(NotionProperty):
    '''
    Represents a Notion Relation Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of relation properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (str): A string to represent a relation in the page.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Relation content. 

        This class instantiates a Notion Relation Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionRelationProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(
                f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'phone_number': content
        }


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
        self.content = {'rich_text': [
            {'type': "text", "text": {"content": content}}]}


class NotionRollupProperty(NotionProperty):
    '''
    !!! DO NOT USE TO CREATE PAGES; RESULTS IN ERROR !!!
    Notion Text Property object. Allows for simple text to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for rollup content. 

        This class instantiates a Notion Rollup Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionRollupProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {'rich_text': [
            {'type': "text", "text": {"content": content}}]}


class NotionSelectProperty(NotionProperty):
    '''
    Represents a Notion Select Property.

    This classes provides conversion methods to convert object to json format.
    It also allows for the creation of select properties in Notion Pages.

    Attributes:
        prop_name (str): Properties identifiable name.
        content (list[str]): A list of strings that represent tags.
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for Select content. 

        This class instantiates a Notion Select Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionSelectProperty object
        '''
        if not isinstance(content, list):
            raise TypeError(
                f'Expected a list of strings, got {type(content).__name__}')

        if len(content) != 1:
            raise ValueError('List must contain only 1 value')

        super().__init__(prop_name)
        self.content = {
            'select': {"options": [{"name": name} for name in content]}
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


class NotionTitleProperty(NotionProperty):
    '''
    Notion Title Property object. Allows for simple text to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for text content. 

        This class instantiates a Notion Title Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionTitleProperty object
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


class NotionUrlProperty(NotionProperty):
    '''
    Notion Url Property object. Allows for simple text to be uploaded to Notion
    '''

    def __init__(self, prop_name, content):
        '''
        Creates a Notion property for text content. 

        This class instantiates a Notion Url Property for a Notion client. 

        Parameters:
            @prop_name = Property's name (User assigned to Todo)
            @content = Content used in property. (The todos in the list)

        Returns:
            NotionUrlProperty object
        '''
        if not isinstance(content, str):
            raise TypeError(f'Expected a string, got {type(content).__name__}')

        super().__init__(prop_name)
        self.content = {
            'url': content
        }

    def __str__(self):
        return f"{self.prop_name}: {self.content}"
