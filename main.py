# import time
from recipe.recipe_communicator import MealAPI, MealParser
# import json

meals = list()
meal_api = MealAPI()

random_meal = meal_api.get_random_meal()

print(MealParser().parse_meal(random_meal))

# for _ in range(50):
#     random_meal = meal_api.get_random_meal()
#     time.sleep(2)
#     meals.append(random_meal)

# with open("meals", "w") as file:
#     json.dump(meals, file, indent=4)

# import json

# with open("meals.json", 'r') as file:
#     data = json.load(file)
#     first_item = data[0]
#     for item in data[1:]:
#         for key in item.keys():
#             if key in first_item.keys():
#                 continue
#             else:
#                 print("broken")
#                 break
