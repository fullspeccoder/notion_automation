import os
from dotenv import load_dotenv
from notion_client import Client
from recipe_communicator import *
import random

api = MealAPI()
random_meal = api.get_random_meal()

load_dotenv()

meal_parser = MealParser()

parsed_random_meal = meal_parser.parse_meal(random_meal)

emojis = [  # Fruits
    "🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐",
    "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝",

    # Vegetables
    "🥦", "🥬", "🥒", "🌶️", "🫑", "🌽", "🥕", "🫒", "🧄", "🧅",

    # Prepared food
    "🍞", "🥐", "🥖", "🫓", "🥨", "🥯", "🥞", "🧇", "🧀",
    "🍖", "🍗", "🥩", "🥓", "🍔", "🍟", "🍕", "🌭", "🥪",
    "🌮", "🌯", "🫔", "🥙", "🧆", "🥚", "🍳", "🥘", "🍲",
    "🫕", "🥣", "🥗", "🍿", "🧈",

    # Desserts & sweets
    "🍰", "🎂", "🧁", "🥧", "🍦", "🍨", "🍧", "🍩", "🍪",
    "🍫", "🍬", "🍭", "🍮", "🍯",

    # Snacks & misc
    "🥜", "🌰", "🥟", "🥠", "🥡", "🦪",]

recipe = NotionRecipe(db_id=os.getenv("NOTION_RECIPE_DATABASE_ID"), emoji=random.choice(emojis), children=[],
                      **parsed_random_meal)

notion_client = Client(auth=os.getenv("NOTION_API_KEY"))

notion_client.pages.create(page_id=os.getenv(
    "NOTION_RECIPE_DATABASE_ID"), **recipe.to_dict())
