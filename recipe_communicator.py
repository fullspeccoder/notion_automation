import requests as rq
from notion_props import *
from notion_blocks import *
from notion_pages import NotionDatabase
"""recipe_communicator.py

Module used to communicate with themealdb database to grab
recipes to send to Notion.

Includes:
    - Retrieves meals randomly, by name, by letter, by id, & lists the categories
    - Parses the meal object obtained from themealdb api
    - Communicates with Notion to create pages within a database.

Example:
    >>> api = MealAPI()
    >>> random_meal = api.get_random_meal()

    >>> load_dotenv()

    >>> meal_parser = MealParser()

    >>> parsed_random_meal = meal_parser.parse_meal(random_meal)

    >>> recipe = NotionRecipe(db_id=os.getenv("NOTION_RECIPE_DATABASE_ID"), emoji="🥦", children=[],
                        **parsed_random_meal)

    >>> notion_client = Client(auth=os.getenv("NOTION_API_KEY"))

    >>> notion_client.pages.create(page_id=os.getenv(
        "NOTION_RECIPE_DATABASE_ID"), **recipe.to_dict())

Notes:
    You will want to be sure that all values are correct when using them within the classes that are defined here.
"""


class MealAPI:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1/"

    def get_random_meal(self):
        url = f'{self.base_url}random.php'

        res = rq.get(url)
        json_data = res.json()

        random_meal = json_data['meals'][0]

        return random_meal

    def search_by_name(self, name):
        url = f'{self.base_url}search.php?s={name}'

        res = rq.get(url)
        json_data = res.json()

        named_meal = json_data['meals'][0]

        return named_meal

    def search_by_letter(self, letter):
        url = f'{self.base_url}search.php?f={letter}'

        res = rq.get(url)
        json_data = res.json()

        lettered_meal = json_data['meals'][0]

        return lettered_meal

    def search_by_id(self, id):
        url = f'{self.base_url}lookup.php?i={id}'

        res = rq.get(url)
        json_data = res.json()

        id_meal = json_data['meals'][0]

        return id_meal

    def list_categories(self):
        url = f'{self.base_url}categories.php'

        res = rq.get(url)
        json_data = res.json()

        categorical_meal = json_data['meals'][0]

        return categorical_meal


class MealParser:
    def parse_meal(self, meal: dict) -> dict:
        filtered_true_values = [{key: value} for key,
                                value in meal.items() if value not in ("", " ") and ('strIngredient' in key or 'strMeasure' in key)]
        halfway_point = int(len(filtered_true_values) / 2)
        filtered_ingredients = filtered_true_values[0: halfway_point]
        filtered_measurements = filtered_true_values[halfway_point:]

        ingredients_w_measurements = dict()

        for ind, obj in enumerate(filtered_ingredients):
            print(ind, obj)
            ingredients_w_measurements.update(
                {obj[f'strIngredient{ind + 1}']: filtered_measurements[ind][f'strMeasure{ind + 1}']})
        print(meal)
        meal = {"name": meal['strMeal'], "category": self.retrieve_category(meal['strCategory']), "instructions": meal['strInstructions'], "cover_url": meal['strMealThumb'],
                "tags": self.retrieve_tags(meal['strTags']), "youtube_url": self.retrieve_url(meal['strYoutube']), 'ingredients': ingredients_w_measurements, 'source_url': self.retrieve_url(meal["strSource"])}

        return meal

    def retrieve_category(self, category):
        if category is None:
            return "Undefined"
        return category

    def retrieve_url(self, url):
        if url == "":
            return None
        return url

    def retrieve_tags(self, meal_tags):
        if meal_tags is None:
            return list()
        tags = meal_tags.split(',')

        return tags


class NotionRecipe(NotionDatabase):
    def __init__(self, db_id, emoji, children, cover_url, category=None, source_url=None, tags=list(), youtube_url=None, name="Recipe Name", instructions=None, ingredients=dict()):
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
