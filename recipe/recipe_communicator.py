import requests as rq
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
                                value in meal.items() if value not in ("", " ", None, 'null') and ('strIngredient' in key or 'strMeasure' in key)]
        halfway_point = int(len(filtered_true_values) / 2)
        filtered_ingredients = filtered_true_values[0: halfway_point]
        filtered_measurements = filtered_true_values[halfway_point:]

        ingredients_w_measurements = dict()

        for ind, obj in enumerate(filtered_ingredients):
            ingredients_w_measurements.update(
                {obj[f'strIngredient{ind + 1}']: filtered_measurements[ind][f'strMeasure{ind + 1}']})
        meal = {"name": meal['strMeal'], "category": self.retriev_prop(meal['strCategory'], "Undefined"), "instructions": meal['strInstructions'], "cover_url": meal['strMealThumb'],
                "tags": self.retriev_prop(meal['strTags'], list), "youtube_url": self.retriev_prop(meal['strYoutube'], str), 'ingredients': ingredients_w_measurements, 'source_url': self.retriev_prop(meal["strSource"], str)}

        return meal

    def retriev_prop(self, prop, data_type):
        if prop in ("", " ", None, 'null'):
            return data_type()
        tags = prop

        return tags
