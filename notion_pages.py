'''notion_pages.py

Provides abstractions to the traditional Notion Page & Database Objects

Includes:

    - Notion Page creation
    - Notion Database creation

Example:

    import notion_pages as np
    np.NotionDatabase(id=someid)
'''


class NotionObject:
    '''Notion Object for creating Notion Pages & Databases

    This class abstracts the information needed to create Notion Pages & Databases, 
    as these can be complex structures.

    Attributes:
        properties (NotionProperties): The Notion properties list.
        children (NotionChildren): The Notion children list.
        emoji (str): The emoji used in page/database.
        cover_url (str): The url for the covertr

    Examples:
        import notion_pages as np
        # NotionObject inherits from NotionObject
        np.NotionObject(id=someid) 
    '''

    def __init__(self, db_id=None, page_id=None, properties=None,
                 children=None, emoji=None, cover_url=None):
        """Initializes a Notion Object.

        Creates a general Notion Object that can represent either a NotionPage or NotionDatabase.
        For better readability and intent clarity, prefer using the NotionPage or NotionDatabase
        class directly when possible.

        Args:
            db_id (str, optional): The database ID string (found in the URL of the Notion page).
            page_id (str, optional): The page ID string (found in the URL of the Notion page).
            properties (NotionProperties, optional): The properties for the page or database schema.
            children (NotionChildren, optional): The list of children of the page or database.
            emoji (str, optional): An emoji to use as the icon for the page.
            cover_url (str, optional): A URL to an image to use as the cover for the page.

        Raises:
            ValueError: If both `db_id` and `page_id` are provided. Only one is allowed.

        Examples:
            >>> import notion_pages as np
            >>> obj = np.NotionObject(page_id="abc123", properties=my_props, emoji="🌟")

        Notes:
            If setting environment variables for your Notion integration, be sure to restart your
            environment for the changes to take effect.
        """

        if db_id is not None and page_id is not None:
            raise ValueError(
                "Only one of 'db_id' or 'page_id' can be provided, not both.")
        # Required
        self.parent = (db_id is not None and {"database_id": db_id}) or (
            page_id is not None and {"page_id": page_id}) or dict()
        # Required
        self.properties = properties or dict()
        self.children = children or list()
        self.icon = {"emoji": emoji or ""}
        self.cover = {"external": {"url": cover_url or ""}}

    def set_parent_page(self, p_id):
        """Sets the parent of the Notion object to a page.

        Updates the object's parent to the given `page_id`. If a `database_id` was previously
        set, it will be removed to ensure only one parent is defined.

        Args:
            p_id (str): The page ID string (found in the URL of the Notion page).

        Examples:
            >>> obj = NotionObject(db_id="abc123")
            >>> obj.set_parent_page("xyz456")
            >>> print(obj.parent)
            {'page_id': 'xyz456'}

        Notes:
            Only one parent is allowed in a Notion object. Calling this method will remove
            any existing `database_id` and replace it with the provided `page_id`.
        """

        if self.parent.get('database_id', None) is not None:
            self.parent.pop("database_id")
        self.parent.update({"page_id": p_id})

    def set_parent_database(self, db_id):
        '''Sets the parent of the Notion object to a page.

            Updates the object's parent to the given "database_id".If a "database_id" was previously 
            set, it will be removed to ensure only one parent is defined.

            Args:
                db_id (str): The database ID string (found in the URL of the Notion Page.)

            Examples:
                >>> obj = NotionObject(page_id="abc123")
                >>> obj.set_parent_database("xyz456")
                >>> print(obj.parent)
                {'database_id': 'xyz456'}

            Notes:
                Only one parent is allowed in a Notion object. Calling this method will remove
                any existing 'page_id' and replace it with the provided 'database_id'.
        '''

        if self.parent.get('page_id', None) is not None:
            self.parent.pop("page_id")
        self.parent.update({"database_id": db_id})

    def set_icon(self, emoji):
        '''Sets the icon of the Notion object.

            Updates the object's icon to the given "emoji". Goes through the structure used by
            the api to use the icon.

            Args:
                emoji (str): Represents the icon for the page

            Examples:
                >>> obj = NotionObject(page_id="abc123")
                >>> obj.set_icon("😀")
                >>> print(obj)
                {"emoji": "😀"}
        '''

        self.icon.update({'emoji': emoji})

    def set_cover_url(self, url):
        '''Sets the cover image of the Notion object using the provided URL

            Updates the object's cover image url to the given "url". Goes through the structure 
            used by the api to use the url.

            Args:
                url (str): Represents the cover image url for the page

            Examples:
                >>> obj = NotionObject(page_id="abc123")
                >>> obj.set_cover_url("https://someurl.com/")
                >>> print(obj.cover)
                {"external": {"url": "https://someurl.com/"}}
        '''

        self.cover.update({"external": {"url": url}})

    def set_properties(self, props):
        '''Sets the properties of the Notion object.

            Updates the object's properties to the given "properties". 
            Goes through the structure used by the api to use the properties.

            Args:
                props (NotionProperties): Represents the properties for the page

            Examples:
                >>> obj = NotionObject(page_id="abc123")
                >>> obj.set_properties(NotionProperties([...]))
                >>> print(obj.properties)
                {...}
        '''

        self.properties = props.to_dict()

    def to_dict(self):
        '''Converts the Notion Object to a dictionary.

            Uses the Notion Object attributes to create a Notion API structure. This structure can
            be used later on when creating a Notion Page or Notion Database.

            Examples:
                >>> obj = NotionObject(page_id="abc123", ...)
                >>> print(obj.to_dict())
                {"parent": {}, "icon": {}, "cover": {}, "properties": {}, "children": {}}

            Returns:
                dict: A dictionary representation of the Notion Object.
        '''

        return {"parent": self.parent, "icon": self.icon, "cover": self.cover,
                "properties": self.properties, "children": self.children}

    def __str__(self):
        '''Returns a string representation of the Notion Object.

            Examples:
                >>> obj = NotionObject(page_id="abc123", ...)
                >>> print(obj)
                '{"parent": {}, "icon": {}, "cover": {}, "properties": {}, "children": {}}'

            Returns:
                str: A string representation of the Notion Object.
        '''
        return str(self.to_dict())


class NotionPage(NotionObject):
    '''Notion Object for creating Notion Pages

        This class abstracts the information needed to create a Notion Page, 
        as this can be a complex structures.

        Attributes:
            properties (NotionProperties): The Notion properties list.
            children (NotionChildren): The Notion children list.
            emoji (str): The emoji used in a page.
            cover_url (str): The url for the cover image

        Examples:
            import notion_pages as np
            # NotionPage inherits from NotionObject
            np.NotionPage(id=someid) 
    '''

    def __init__(self, n_id=None, properties=None, children=None, emoji=None, cover_url=None):
        """Initializes a Notion Page.

        Creates a Notion Page that represents a NotionPage.

        Args:
            id (str, optional): The page ID string (found in the URL of the Notion page).
            properties (NotionProperties, optional): The properties for the page schema.
            children (NotionChildren, optional): The list of children of the page.
            emoji (str, optional): An emoji to use as the icon for the page.
            cover_url (str, optional): A URL to an image to use as the cover for the page.

        Examples:
            >>> import notion_pages as np
            >>> obj = np.NotionPage(n_id="abc123", properties=my_props, emoji="🌟")

        Notes:
            If setting environment variables for your Notion integration, be sure to restart your
            environment for the changes to take effect.
        """

        super().__init__(page_id=n_id, properties=properties,
                         children=children, emoji=emoji, cover_url=cover_url)

    def set_parent(self, n_id):
        """Sets the parent of the Notion object to a page.

        Updates the object's parent to the given `id`.

        Args:
            id (str): The page ID string (found in the URL of the Notion page).

        Examples:
            >>> obj = NotionPage(n_id="abc123")
            >>> obj.set_parent("xyz456")
            >>> print(obj.parent)
            {'page_id': 'xyz456'}
        """

        self.set_parent_page(n_id)


class NotionDatabase(NotionObject):
    '''Notion Object for creating Notion databases

        This class abstracts the information needed to create a Notion Database, 
        as this can be a complex structures.

        Attributes:
            properties (NotionProperties): The Notion properties list.
            children (NotionChildren): The Notion children list.
            emoji (str): The emoji used in a database.
            cover_url (str): The url for the cover image

        Examples:
            import notion_databases as np
            # NotionDatabase inherits from NotionObject
            np.NotionDatabase(n_id=someid) 
    '''

    def __init__(self, n_id=None, properties=None, children=None, emoji=None, cover_url=None):
        """Initializes a Notion Database.

        Creates a Notion Database that represents a NotionDatabase.

        Args:
            id (str, optional): The database ID string (found in the URL of the Notion database).
            properties (NotionProperties, optional): The properties for the database schema.
            children (NotionChildren, optional): The list of children of the database.
            emoji (str, optional): An emoji to use as the icon for the database.
            cover_url (str, optional): A URL to an image to use as the cover for the database.

        Examples:
            >>> import notion_pages as np
            >>> obj = np.NotionDatabase(n_id="abc123", properties=my_props, emoji="🌟")

        Notes:
            If setting environment variables for your Notion integration, be sure to restart your
            environment for the changes to take effect.
        """

        super().__init__(db_id=n_id, properties=properties,
                         children=children, emoji=emoji, cover_url=cover_url)

    def set_parent(self, n_id):
        """Sets the parent of the Notion object to a database.

        Updates the object's parent to the given `n_id`.

        Args:
            n_id (str): The database ID string (found in the URL of the Notion database).

        Examples:
            >>> obj = NotionDatabase(n_id="abc123")
            >>> obj.set_parent("xyz456")
            >>> print(obj.parent)
            {'database_id': 'xyz456'}
        """
        self.set_parent_database(n_id)
