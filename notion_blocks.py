from enum import Enum
'''
notion_blocks.py

Provides high-level abstractions for building Notion API-compatible blocks
without manually writing the complex nested JSON structures.

These classes enable simple and intuitive block creation for developers
interacting with Notion programmatically.

Includes:
    - Enum definitions for supported colors and code languages
    - A base `NotionBlock` class
    - Block-specific subclasses (e.g. Paragraph, Heading, Code)

Example:
    >>> block = NotionParagraphBlock("Hello, world!")
    >>> block.to_json()
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": "Hello, world!"}
            }]
        }
    }
'''


class NotionColor(Enum):
    '''Enum representing supported Notion color options.

    This enum includes both text and background color values that can be
    applied to various block types in the Notion API.

    Example:
        >>> NotionColor.BLUE.value
        'blue'
    '''
    BLUE = 'blue'
    BROWN = 'brown'
    DEFAULT = 'default'
    GRAY = 'gray'
    GREEN = 'green'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    PINK = 'pink'
    PURPLE = 'purple'
    RED = 'red'
    BLUE_BACKGROUND = 'blue_background'
    BROWN_BACKGROUND = 'brown_background'
    GRAY_BACKGROUND = 'gray_background'
    GREEN_BACKGROUND = 'green_background'
    ORANGE_BACKGROUND = 'orange_background'
    YELLOW_BACKGROUND = 'yellow_background'
    PINK_BACKGROUND = 'pink_background'
    PURPLE_BACKGROUND = 'purple_background'
    RED_BACKGROUND = 'red_background'


class NotionCodeLanguage(Enum):
    '''Enum representing programming languages supported in Notion code blocks.

    These language identifiers are used to specify syntax highlighting in Notion's
    code block feature.

    Example:
        >>> NotionCodeLanguage.PYTHON.value
        'python'
    '''
    ABAP = "abap"
    ARDUINO = "arduino"
    BASH = "bash"
    BASIC = "basic"
    C = "c"
    CLOJURE = "clojure"
    COFFEESCRIPT = "coffeescript"
    CPP = "c++"
    CSHARP = "c#"
    CSS = "css"
    DART = "dart"
    DIFF = "diff"
    DOCKER = "docker"
    ELIXIR = "elixir"
    ELM = "elm"
    ERLANG = "erlang"
    FLOW = "flow"
    FORTRAN = "fortran"
    FSHARP = "f#"
    GHERKIN = "gherkin"
    GLSL = "glsl"
    GO = "go"
    GRAPHQL = "graphql"
    GROOVY = "groovy"
    HASKELL = "haskell"
    HTML = "html"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    JULIA = "julia"
    KOTLIN = "kotlin"
    LATEX = "latex"
    LESS = "less"
    LISP = "lisp"
    LIVESCRIPT = "livescript"
    LUA = "lua"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    MARKUP = "markup"
    MATLAB = "matlab"
    MERMAID = "mermaid"
    NIX = "nix"
    OBJECTIVE_C = "objective-c"
    OCAML = "ocaml"
    PASCAL = "pascal"
    PERL = "perl"
    PHP = "php"
    PLAIN_TEXT = "plain text"
    POWERSHELL = "powershell"
    PROLOG = "prolog"
    PROTOBUF = "protobuf"
    PYTHON = "python"
    R = "r"
    REASON = "reason"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCALA = "scala"
    SCHEME = "scheme"
    SCSS = "scss"
    SHELL = "shell"
    SQL = "sql"
    SWIFT = "swift"
    TYPESCRIPT = "typescript"
    VB_NET = "vb.net"
    VERILOG = "verilog"
    VHDL = "vhdl"
    VISUAL_BASIC = "visual basic"
    WEBASSEMBLY = "webassembly"
    XML = "xml"
    YAML = "yaml"
    MULTI_LANGUAGE = "java/c/c++/c#"


class NotionBlock:
    '''Base class for Notion block abstractions.

    Provides common structure and utility methods shared by all specific
    Notion block types.

    Attributes:
        type (str): The Notion block type (e.g., "paragraph", "code").
        content (dict): The inner block content to be formatted into a Notion API payload.

    Example:
        >>> class NotionParagraphBlock(NotionBlock):
        ...     def __init__(self, text):
        ...         super().__init__("paragraph")
        ...         self.content = {"rich_text": [{"type": "text", "text": {"content": text}}]}
        >>> block = NotionParagraphBlock("Hello")
        >>> block.to_dict()
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Hello"}
                }]
            }
        }
    '''

    def __init__(self, type):
         '''Initializes a base Notion block.

            Args:
                type (str): The Notion block type (e.g., "code", "paragraph").
        '''
        self.type = type
        self.content = dict()

    def to_dict(self):
         '''Returns the full dictionary representation of the block.

        Returns:
            dict: A Notion API-compatible dictionary with type and content.
        '''
        return {"object": "block", "type": self.type, self.type: self.content}

    def resolve_color(self, color_input):
        '''Resolves a color string or enum to a valid NotionColor value.

        Args:
            color_input (str | NotionColor): The input color to validate.

        Returns:
            NotionColor: The corresponding NotionColor enum.

        Raises:
            ValueError: If the string does not match any valid NotionColor.
            TypeError: If the input is not a string or NotionColor.
        '''
        '''Converts a string or NotionColor enum to a valid NotionColor.'''
        if isinstance(color_input, NotionColor):
            return color_input
        elif isinstance(color_input, str):
            try:
                return NotionColor(color_input)
            except ValueError:
                raise ValueError(
                    f"Invalid color: {color_input}. Must be one of {[c.value for c in NotionColor]}")
        else:
            raise TypeError("Color must be a str or NotionColor enum")


class NotionBookmarkBlock(NotionBlock):
    """Represents a Notion Bookmark block.

    Creates a bookmark-style block that links to a given URL with an optional caption.

    Attributes:
        caption (str): Optional caption text to display.
        url (str): The URL to be bookmarked.

    Example:
        >>> block = NotionBookmarkBlock("Python Docs", "https://docs.python.org")
        >>> block.to_dict()
        {
            "object": "block",
            "type": "bookmark",
            "bookmark": {
                "caption": [{
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": "Python Docs",
                            "link": "https://docs.python.org"
                        }
                    }]
                }]
            }
        }
    """
    def __init__(self, caption=None, url=None):
        super().__init__("bookmark")
        self.content = {"caption": [{"rich_text": [
            {
                "type": "text",
                "text": {
                    "content": caption,
                    "link": url,
                }
            }
        ]}]}


class NotionBreadcrumbBlock(NotionBlock):
    """Represents a Notion Breadcrumb block.

    Creates a breadcrumb navigation element.
    Typically used for visual structure in the Notion UI.

    Note:
        Currently creates an empty block — the visual breadcrumb is handled
        entirely by Notion.

    Example:
        >>> block = NotionBreadcrumbBlock()
        >>> block.to_dict()
        {
            "object": "block",
            "type": "breadcrumb",
            "breadcrumb": {}
        }
    """
    def __init__(self, text=None, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("breadcrumb")
        self.content = {}


class NotionBulletedListItem(NotionBlock):
    """Represents a Notion bulleted list item block.

    Accepts plain text and optional child blocks, and renders it as a bulleted list item.

    Attributes:
        text (str): The bullet item content.
        color (NotionColor): Optional text color.
        children (list[NotionBlock], optional): Nested blocks under this list item.

    Example:
        >>> block = NotionBulletedListItem("Learn Python", NotionColor.BLUE)
        >>> block.to_dict()
    """
    def __init__(self, text, color=NotionColor.DEFAULT, children=None):
        color = self.resolve_color(color)
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
            "color": color,
            "children": children
        }


class NotionCalloutBlock(NotionBlock):
    """Represents a Notion Callout block.

    A styled container block with an emoji icon and colored background.

    Attributes:
        text (str): The callout message.
        emoji (str): Emoji character to display as an icon.
        color (NotionColor): Optional background/text color.

    Example:
        >>> block = NotionCalloutBlock("Remember to hydrate!", "💧", NotionColor.YELLOW)
        >>> block.to_dict()
    """
    def __init__(self, text=None, emoji="⭐️", color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("callout")
        self.content = {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                }
            }],
            "icon": {
                "emoji": emoji
            },
            "color": color
        }


class NotionCodeBlock(NotionBlock):
    """Represents a Notion Code block.

    Formats a code snippet using syntax highlighting for the specified language.

    Attributes:
        code (str): The code string to be displayed.
        language (str | NotionCodeLanguage): The language for syntax highlighting.

    Example:
        >>> block = NotionCodeBlock("print('Hello')", "python")
        >>> block.to_dict()
    """
    def __init__(self, code=None, language="javascript"):
        language = self.resolve_code_language(language)
        super().__init__("code")
        self.content = {
            "caption": [],
            "rich_text": [{
                "type": "text",
                "text": {
                        "content": code
                }
            }],
            "language": language
        }

    def resolve_code_language(self, language_input):
        """Converts a string or enum into a valid NotionCodeLanguage value.

        Args:
            language_input (str | NotionCodeLanguage): Language to validate.

        Returns:
            str: A string representing the valid code language.

        Raises:
            ValueError: If the language is unsupported.
            TypeError: If the input is not a string or NotionCodeLanguage.
        """
        if isinstance(language_input, NotionCodeLanguage):
            return language_input
        elif isinstance(language_input, str):
            try:
                return NotionCodeLanguage(language_input)
            except ValueError:
                valid = [lang.value for lang in NotionCodeLanguage]
                raise ValueError(
                    f"Invalid language: '{language_input}'. Must be one of: {valid}")
        else:
            raise TypeError(
                "Language must be a str or NotionCodeLanguage enum")


class NotionColumnListBlock(NotionBlock):
    """Represents a Notion Column List block.

    A container for two or more `NotionColumnBlock` elements, creating a multi-column layout.

    Note:
        When appending to a page, this block must contain at least two child columns,
        and each column must contain at least one block.

    Example:
        >>> block = NotionColumnListBlock()
        >>> block.to_dict()
    """
    def __init__(self):
        super().__init__("column_list")
        self.content = {}


class NotionColumnBlock(NotionBlock):
    """Represents a Notion Column block.

    Intended to be a direct child of a `NotionColumnListBlock`. Each column should
    contain at least one content block (e.g. Paragraph, Callout).

    Example:
        >>> block = NotionColumnBlock()
        >>> block.to_dict()
    """
    def __init__(self):
        super().__init__("column")
        self.content = {}


class NotionDivider(NotionBlock):
     """Represents a Notion Divider block.

    A horizontal rule used to visually separate content.

    Example:
        >>> block = NotionDivider()
        >>> block.to_dict()
    """
    def __init__(self):
        super().__init__('divider')
        self.content = {}


class NotionEmbedBlock(NotionBlock):
     """Represents a Notion Embed block.

    Embeds external media (like videos, audio, or web tools) via a URL.

    Note:
        Some embeds may not appear as expected or may load slowly in the Notion UI.
        Vimeo is known to embed well.

    Attributes:
        url (str): The URL of the content to embed.

    Example:
        >>> block = NotionEmbedBlock("https://vimeo.com/123456")
        >>> block.to_dict()
    """
    def __init__(self, url=None):
        super().__init__("embed")
        self.content = {
            "url": url
        }


class NotionEquationBlock(NotionBlock):
     """Represents a Notion Equation block.

    Displays a KaTeX compatible equation.

    Attributes:
        expression (str): A KaTeX-compatible math expression.

    Example:
        >>> block = NotionEquationBlock("x^2 + y^2 = z^2")
        >>> block.to_dict()
    """
    def __init__(self, expression=None):
        super().__init__("equation")
        self.content = {"expression": expression}


class NotionFileBlock(NotionBlock):
    """Represents a Notion File block.

    Displays a downloadable file stored externally.

    Note:
        Uploading files to Notion is unsupported by the API

    Attributes:
        url (str): Publicly accessible URL to the file.
        name (str): Display name of the file.

    Example:
        >>> block = NotionFileBlock("https://example.com/myfile.pdf", "Resume.pdf")
        >>> block.to_dict()
    """
    def __init__(self, url=None, name=None):
        super().__init__("file")
        self.content = {
            "caption": [],
            "type": "external",
            "external": {
                    "url": url
            },
            "name": name
        }


class NotionHeading(NotionBlock):
    """Represents a Notion Heading block (H1, H2, or H3).

    Creates a heading of level 1, 2, or 3 with optional color.

    Attributes:
        type (int): Heading level (1, 2, or 3).
        text (str): The heading content.
        color (NotionColor): Optional text color.

    Example:
        >>> block = NotionHeading(2, "Project Overview", NotionColor.BLUE)
        >>> block.to_dict()
    """
    def __init__(self, type, text, color="default"):
        color = self.resolve_color(color)
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


class NotionImageBlock(NotionBlock):
    """Represents a Notion Image block.

    Embeds an external image by URL.

    Note:
        Supported file types: bmp, gif, heic, jpeg, jpg, png, svg, tif, tiff.

    Attributes:
        url (str): The URL of the image.

    Example:
        >>> block = NotionImageBlock("https://example.com/image.png")
        >>> block.to_dict()
    """
    def __init__(self, url=None):
        super().__init__("image")
        self.content = {
            "type": "external",
            "external": {
                "url": url
            }
        }


class NotionLinkPreviewBlock(NotionBlock):
    """Represents a Notion Link Preview block.

    Displays a rich preview of a URL. Note that the Notion API currently does
    not support creating or appending these blocks directly.

     Note:
        Does not support creating or appending this block type

    Attributes:
        url (str): The URL to preview.

    Example:
        >>> block = NotionLinkPreviewBlock("https://github.com")
        >>> block.to_dict()
    """
    def __init__(self, url=None):
        super().__init__("link_preview")
        self.content = {
            "url": url
        }


class NotionMentionBlock(NotionBlock):
    # Must be a child of a rich text object that
    # is nested in a paragraph block object.
    """Represents a Notion Mention block (specifically a page mention).

    Mentions a page inside a rich text object within a paragraph block.

    Notes:
        Must be a child of a rich text object inside of
        a paragraph block.

    Attributes:
        page_id (str): The Notion page ID to reference.

    Example:
        >>> block = NotionMentionBlock("some-page-id")
        >>> block.to_dict()
    """
    def __init__(self, page_id=None):
        super().__init__("page")
        self.content = {
            "id": page_id
        }


class NotionNumberedListItem(NotionBlock):
    """Represents a Notion numbered list item block.

    Creates a line in a numbered list with optional text color.

    Attributes:
        text (str): The content of the list item.
        color (NotionColor): Optional text color.

    Example:
        >>> block = NotionNumberedListItem("Step 1", NotionColor.GREEN)
        >>> block.to_dict()
    """
    def __init__(self, text, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
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


class NotionParagraphBlock(NotionBlock):
     """Represents a Notion Paragraph block.

    Creates a basic block of rich text content.

    Attributes:
        text (str): The paragraph content.
        color (NotionColor): Optional text color.

    Example:
        >>> block = NotionParagraphBlock("This is a paragraph.", NotionColor.GRAY)
        >>> block.to_dict()
    """
    def __init__(self, text=None, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("paragraph")
        self.content = {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                }
            }],
            "color": "default"
        }


class NotionPDFBlock(NotionBlock):"""Represents a Notion PDF block.

    Embeds a PDF from an external URL.

    Attributes:
        url (str): The public URL to the PDF file.

    Example:
        >>> block = NotionPDFBlock("https://example.com/file.pdf")
        >>> block.to_dict()
    """
    def __init__(self, url=None):
        super().__init__("pdf")
        self.content = {
            "type": "external",
            "external": {
                "url": url
            }
        }


class NotionQuoteBlock(NotionBlock):
    """Represents a Notion Quote block.

    Renders text in styled quotation formatting.

    Note:
        Can have nested child blocks, the API
        currently does not support this.

    Attributes:
        text (str): The quoted text.
        color (NotionColor): Optional text color.

    Example:
        >>> block = NotionQuoteBlock("Do or do not. There is no try.")
        >>> block.to_dict()
    """
    def __init__(self, text=None, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("quote")
        self.content = {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                },
            }],
            "color": "default"
        }


class NotionSyncedBlock(NotionBlock):
    """Represents a Notion Synced Block.

    Synced blocks mirror content across pages. This block marks the source synced block.

    Note:
        This is typically followed by content blocks or a `NotionSyncedFromBlock`.
        Also cannot update these blocks

    Example:
        >>> block = NotionSyncedBlockBlock()
        >>> block.to_dict()
    """
    def __init__(self):
        super().__init__("synced_block")
        self.content = {
            "synced_from": None,
            "children": [{}]
        }

    def append_child(self, child):
        self.content['children'][0].update(child.to_dict())


# class NotionTableBlock(NotionBlock):
#     def __init__(self, text=None, color=NotionColor.DEFAULT):
#         color = self.resolve_color(color)
#         pass


class NotionTableOfContentsBlock(NotionBlock):
    """Represents a Notion Table of Contents block.

    Automatically generates a linked index of headings on the page.

    Attributes:
        color (NotionColor): Optional text color.

    Example:
        >>> block = NotionTableOfContentsBlock()
        >>> block.to_dict()
    """
    def __init__(self, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("table_of_contents")
        self.content = {
            "color": color
        }


class NotionTodo(NotionBlock):
    """Represents a Notion To-Do block.

    A checkbox-style task item with completion state.

    Attributes:
        text (str): The task description.
        checked (bool): Whether the checkbox is marked.
        color (NotionColor): Optional color for the text.

    Example:
        >>> block = NotionToDoBlock("Finish homework", checked=True)
        >>> block.to_dict()
    """
    def __init__(self, text, color="default", checked=False):
        color = self.resolve_color(color)
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


class NotionToggleBlock(NotionBlock):
    """Represents a Notion Toggle block.

    A collapsible block that can hide/show nested content.

    Attributes:
        text (str): The toggle label.
        color (NotionColor): Optional color for the label.

    Example:
        >>> block = NotionToggleBlock("Click to expand")
        >>> block.to_dict()
    """
    def __init__(self, text=None, children=None, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("toggle")
        self.content = {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                }
            }],
            "color": color,
            "children": [child.to_dict() for child in children]
        }


class NotionVideoBlock(NotionBlock):
    """Represents a Notion Video block.

    Embeds a video from an external URL (e.g., YouTube, Vimeo).

    Note:
        Supported types are:
        amv,asf,avi,f4v,flv,gifv,mkv,mov,mpg,mpeg,mpv,mp4,m4v,qt,wmv
        Can support youtube video links that include embed or watch.
        E.g. https://www.youtube.com/watch?v=[id], https://www.youtube.com/embed/[id]


    Attributes:
        url (str): Public URL to the video.

    Example:
        >>> block = NotionVideoBlock("https://youtube.com/watch?v=xyz")
        >>> block.to_dict()
    """
    def __init__(self, url=None, color=NotionColor.DEFAULT):
        color = self.resolve_color(color)
        super().__init__("video")
        self.content = {
            "type": "external",
            "external": {
                "url": url
            }
        }
