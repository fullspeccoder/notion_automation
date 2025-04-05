import requests as rq
import os
from dotenv import load_dotenv
from notion_client import Client
from notion_props import *
from notion_pages import NotionDatabase
"""filename

Desc

Includes:
    - feature

Example:
    >>> example here

Notes:
    
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
            ingredients_w_measurements.update(
                {obj[f'strIngredient{ind + 1}']: filtered_measurements[ind][f'strMeasure{ind + 1}']})

        meal = {"name": meal['strMeal'], "category": meal['strCategory'], "instructions": meal['strInstructions'], "thumbnail_url": meal['strMealThumb'],
                "tags": meal['strTags'].split(','), "youtube_url": meal['strYoutube'], 'ingredients': ingredients_w_measurements, 'source_url': meal["strSource"]}

        return meal


class NotionRecipe(NotionDatabase):
    def __init__(self, db_id, emoji, children, cover_url, category='Breakfast'):
        super().__init__(db_id, emoji=emoji, children=children, cover_url=cover_url)
        self.db_id = db_id
        self.properties = NotionProperties()
        # Category (Select Property)
        self.properties.add_property(
            NotionSelectProperty("Category", category))
        # Source URL (URL Property)
        self.properties.add_property(NotionUrlProperty(
            "Source URL", "http://www.vodkaandbiscuits.com/2014/03/06/bangin-breakfast-potatoes/"))
        # Tags (Multi Select Property)
        self.properties.add_property(NotionMultiSelectProperty(
            "Tags", ["Breakfast", "Italian"]))
        # Youtube URL (URL Property)
        self.properties.add_property(NotionUrlProperty(
            "Youtube URL", "https://www.youtube.com/watch?v=BoD0TIO9nE4"))
        # Name (Title Property)
        self.properties.add_property(NotionTitleProperty(
            "Name", "Garlic Bread Sloppy Joes"))
        self.properties = self.properties.to_dict()
        # Instructions (Textual Block)
        # Ingredients (Todo Block)


load_dotenv()
recipe = NotionRecipe(os.getenv("NOTION_RECIPE_DATABASE_ID"), "🍕", [],
                      "https://www.themealdb.com/images/media/meals/1550441882.jpg")

notion_client = Client(auth=os.getenv("NOTION_API_KEY"))

# The databse id here is now visible throughout the program, it would be better to use the ospdule to grab it everytime
notion_client.pages.create(page_id=recipe.db_id, **recipe.to_dict())


meal_object = {
    "meals": [
        {
            "idMeal": "52965",
            "strMeal": "Breakfast Potatoes",
            "strMealAlternate": None,
            "strCategory": "Breakfast",
            "strArea": "Canadian",
            "strInstructions": "Before you do anything, freeze your bacon slices that way when you're ready to prep, it'll be so much easier to chop!\r\nWash the potatoes and cut medium dice into square pieces. To prevent any browning, place the already cut potatoes in a bowl filled with water.\r\nIn the meantime, heat 1-2 tablespoons of oil in a large skillet over medium-high heat. Tilt the skillet so the oil spreads evenly.\r\nOnce the oil is hot, drain the potatoes and add to the skillet. Season with salt, pepper, and Old Bay as needed.\r\nCook for 10 minutes, stirring the potatoes often, until brown. If needed, add a tablespoon more of oil.\r\nChop up the bacon and add to the potatoes. The bacon will start to render and the fat will begin to further cook the potatoes. Toss it up a bit! The bacon will take 5-6 minutes to crisp.\r\nOnce the bacon is cooked, reduce the heat to medium-low, add the minced garlic and toss. Season once more. Add dried or fresh parsley. Control heat as needed.\r\nLet the garlic cook until fragrant, about one minute.\r\nJust before serving, drizzle over the maple syrup and toss. Let that cook another minute, giving the potatoes a caramelized effect.\r\nServe in a warm bowl with a sunny side up egg!",
            "strMealThumb": "https://www.themealdb.com/images/media/meals/1550441882.jpg",
            "strTags": "Breakfast,Brunch",
            "strYoutube": "https://www.youtube.com/watch?v=BoD0TIO9nE4",
            "strIngredient1": "Potatoes",
            "strIngredient2": "Olive Oil",
            "strIngredient3": "Bacon",
            "strIngredient4": "Garlic Clove",
            "strIngredient5": "Maple Syrup",
            "strIngredient6": "Parsley",
            "strIngredient7": "Salt",
            "strIngredient8": "Pepper",
            "strIngredient9": "Allspice",
            "strIngredient10": "",
            "strIngredient11": "",
            "strIngredient12": "",
            "strIngredient13": "",
            "strIngredient14": "",
            "strIngredient15": "",
            "strIngredient16": "",
            "strIngredient17": "",
            "strIngredient18": "",
            "strIngredient19": "",
            "strIngredient20": "",
            "strMeasure1": "3 Medium",
            "strMeasure2": "1 tbs",
            "strMeasure3": "2 strips",
            "strMeasure4": "Minced",
            "strMeasure5": "1 tbs",
            "strMeasure6": "Garnish",
            "strMeasure7": "Pinch",
            "strMeasure8": "Pinch",
            "strMeasure9": "To taste",
            "strMeasure10": " ",
            "strMeasure11": " ",
            "strMeasure12": " ",
            "strMeasure13": " ",
            "strMeasure14": " ",
            "strMeasure15": " ",
            "strMeasure16": " ",
            "strMeasure17": " ",
            "strMeasure18": " ",
            "strMeasure19": " ",
            "strMeasure20": " ",
            "strSource": "http://www.vodkaandbiscuits.com/2014/03/06/bangin-breakfast-potatoes/",
            "strImageSource": None,
            "strCreativeCommonsConfirmed": None,
            "dateModified": None
        }
    ]
}

# api = MealAPI()
# random_meal = api.get_random_meal()

# meal_parser = MealParser()

# parsed_random_meal = meal_parser.parse_meal(random_meal)

# print(parsed_random_meal)
# Recipe Page Creator
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
