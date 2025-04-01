class NotionPage:
    def __init__(self, db_id=None, page_id=None, properties=None, children=None, emoji=None, cover_url=None):
        '''
        IF SETTING ENVIRONMENT VARIABLES, BE SURE TO RESTART YOUR ENVIRONMENT FOR THEM TO TAKE EFFECT
        '''
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
        if self.parent.get('database_id', None) is not None:
            self.parent.pop("database_id")
        self.parent.update({"page_id": p_id})

    def set_parent_database(self, db_id):
        if self.parent.get('page_id', None) is not None:
            self.parent.pop("page_id")
        self.parent.update({"database_id": db_id})

    def set_icon(self, emoji):
        self.icon.update({'emoji': emoji})

    def set_cover(self, url):
        self.cover.update({"external": {"url": url}})

    def set_properties(self, props):
        self.properties = props.to_dict()

    def to_dict(self):
        return {"parent": self.parent, "icon": self.icon, "cover": self.cover, "properties": self.properties, "children": self.children}

    def __str__(self):
        return str({"parent": self.parent, "icon": self.icon, "cover": self.cover, "properties": self.properties, "children": self.children})
