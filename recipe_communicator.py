import requests as rq
from notion_props import *


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

        parsed_meal = NotionMeal(meal['strMeal'], meal['strCategory'], meal['strInstructions'],
                                 meal['strMealThumb'], meal['strTags'].split(','), meal['strYoutube'], ingredients_w_measurements, meal['strSource'])
        return parsed_meal.to_json()


class NotionMeal:
    def __init__(self, name: str = None, category: str = None, instructions: str = None, thumbnail_url: str = None, tags: list = None, youtube_url: str = None, ingredients: dict = None, source_url: str = None) -> None:
        # Title Property
        self.meal_name = name
        NotionTitleProperty("Title", name)
        # Text Property
        self.category = category
        NotionRichTextProperty("Category", category)
        # Child Block
        self.instructions = instructions

        # Cover Image
        self.thumbnail_url = thumbnail_url
        # Multi Select
        self.tags = tags
        NotionMultiSelectProperty("Tags", tags)
        # Url Property
        self.youtube_url = youtube_url
        NotionUrlProperty("Youtube Url", youtube_url)
        # Child Block
        self.ingredients = ingredients
        # Url Property
        self.source_url = source_url
        NotionUrlProperty("Source Url", source_url)

    def to_json(self):
        return {'meal_name': self.meal_name, "category": self.category, "instructions": self.instructions, "thumbnail_url": self.thumbnail_url, "tags": self.tags, "youtube_url": self.youtube_url, "ingredients": self.ingredients, "source_url": self.source_url}


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

url = 'https://www.themealdb.com/api/json/v1/1/random.php'

res = rq.get(url)
json_data = res.json()

random_meal = json_data['meals'][0]

meal_parser = MealParser()

parsed_random_meal = meal_parser.parse_meal(random_meal)

print(parsed_random_meal)
