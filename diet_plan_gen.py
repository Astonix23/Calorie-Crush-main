import pandas as pd
import random
meals_data = [
    # Vegetarian Healthy Meals
    {"name": "Oatmeal with Berries", "calories": 300, "protein": 10, "carbs": 50, "fats": 5, "vegetarian": True},
    {"name": "Avocado Toast with Whole Grain Bread", "calories": 350, "protein": 9, "carbs": 40, "fats": 15, "vegetarian": True},
    {"name": "Quinoa Salad with Chickpeas and Veggies", "calories": 400, "protein": 15, "carbs": 55, "fats": 12, "vegetarian": True},
    {"name": "Spinach and Feta Salad with Olive Oil", "calories": 300, "protein": 12, "carbs": 25, "fats": 20, "vegetarian": True},
    {"name": "Lentil Soup with Whole Grain Bread", "calories": 350, "protein": 18, "carbs": 45, "fats": 5, "vegetarian": True},
    {"name": "Stir-fried Vegetables with Tofu", "calories": 350, "protein": 20, "carbs": 40, "fats": 10, "vegetarian": True},
    {"name": "Sweet Potato and Black Bean Chili", "calories": 400, "protein": 15, "carbs": 55, "fats": 10, "vegetarian": True},
    {"name": "Greek Yogurt with Honey and Nuts", "calories": 250, "protein": 15, "carbs": 25, "fats": 10, "vegetarian": True},
    {"name": "Brown Rice and Vegetable Stir-fry", "calories": 400, "protein": 10, "carbs": 60, "fats": 12, "vegetarian": True},
    {"name": "Vegetarian Buddha Bowl", "calories": 450, "protein": 20, "carbs": 60, "fats": 15, "vegetarian": True},

    # Non-Vegetarian Healthy Meals
    {"name": "Grilled Chicken Breast with Steamed Broccoli", "calories": 400, "protein": 40, "carbs": 30, "fats": 10, "vegetarian": False},
    {"name": "Baked Salmon with Quinoa and Asparagus", "calories": 450, "protein": 35, "carbs": 35, "fats": 15, "vegetarian": False},
    {"name": "Turkey and Avocado Wrap in Whole Wheat Tortilla", "calories": 350, "protein": 25, "carbs": 40, "fats": 10, "vegetarian": False},
    {"name": "Shrimp and Brown Rice Stir-fry", "calories": 400, "protein": 30, "carbs": 55, "fats": 10, "vegetarian": False},
    {"name": "Grilled Chicken Salad with Olive Oil", "calories": 350, "protein": 35, "carbs": 20, "fats": 15, "vegetarian": False},
    {"name": "Egg White Omelette with Spinach and Mushrooms", "calories": 300, "protein": 25, "carbs": 10, "fats": 10, "vegetarian": False},
    {"name": "Tuna Salad with Mixed Greens", "calories": 350, "protein": 30, "carbs": 15, "fats": 20, "vegetarian": False},
    {"name": "Chicken and Avocado Salad", "calories": 400, "protein": 35, "carbs": 20, "fats": 20, "vegetarian": False},
    {"name": "Beef Stir-fry with Vegetables", "calories": 450, "protein": 40, "carbs": 35, "fats": 15, "vegetarian": False},
    {"name": "Baked Cod with Sweet Potatoes and Green Beans", "calories": 400, "protein": 35, "carbs": 40, "fats": 10, "vegetarian": False},

    # Healthy Snacks
    {"name": "Apple Slices with Peanut Butter", "calories": 200, "protein": 6, "carbs": 25, "fats": 10, "vegetarian": True},
    {"name": "Carrot and Hummus Snack", "calories": 150, "protein": 5, "carbs": 20, "fats": 8, "vegetarian": True},
    {"name": "Mixed Nuts", "calories": 200, "protein": 6, "carbs": 15, "fats": 15, "vegetarian": True},
    {"name": "Greek Yogurt with Blueberries", "calories": 200, "protein": 12, "carbs": 25, "fats": 5, "vegetarian": True},
    {"name": "Protein Bar (Low Sugar)", "calories": 250, "protein": 20, "carbs": 30, "fats": 7, "vegetarian": True},
    {"name": "Hard-boiled Eggs", "calories": 150, "protein": 12, "carbs": 1, "fats": 10, "vegetarian": False},
    {"name": "Smoothie with Spinach, Banana, and Protein Powder", "calories": 250, "protein": 20, "carbs": 40, "fats": 5, "vegetarian": True}
]

# Calorie estimation logic
def generate_calories(age, weight, gender, activity_level, goal):
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * 175 - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * 165 - 5 * age - 161
    
    activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][activity_level - 1]
    calories = bmr * activity_multiplier

    if goal.lower() == "lose weight":
        calories -= 500
    elif goal.lower() == "gain muscle":
        calories += 500
    
    return int(calories)


def generate_meals(predicted_calories, vegetarian=False, dietary_restrictions=None, allergies=None):
    meal_plan = []
    chosen_meals = []  # Keep track of selected meals to ensure variety
    
    # Filter meals based on vegetarian preference
    suitable_meals = [meal for meal in meals_data if meal['vegetarian'] or not vegetarian]
    
    # Filter out meals based on dietary restrictions or allergies
    if dietary_restrictions:
        suitable_meals = [meal for meal in suitable_meals if dietary_restrictions.lower() not in meal['name'].lower()]
    
    if allergies:
        suitable_meals = [meal for meal in suitable_meals if allergies.lower() not in meal.get('ingredients', '').lower()]

    # Define calorie distribution for breakfast, lunch, and dinner
    meal_distributions = {
        "breakfast": predicted_calories * 0.3,
        "lunch": predicted_calories * 0.4,
        "dinner": predicted_calories * 0.3
    }

    # Debug: print the target calorie distribution
    print(f"Target Meal Calorie Distribution: {meal_distributions}")

    for meal_time, target_calories in meal_distributions.items():
        # Sort suitable meals by proximity to the target calories
        suitable_meals_for_time = sorted(suitable_meals, key=lambda meal: abs(meal["calories"] - target_calories))
        
        # Exclude already chosen meals
        suitable_meals_for_time = [meal for meal in suitable_meals_for_time if meal not in chosen_meals]
        
        # Pick the best match for the target calories and ensure variety
        if suitable_meals_for_time:
            chosen_meal = suitable_meals_for_time[0]  # Get the closest meal
            chosen_meals.append(chosen_meal)  # Add to the list of chosen meals
            meal_plan.append({
                "meal_time": meal_time.title(),
                "name": chosen_meal["name"],
                "calories": chosen_meal["calories"],
                "protein": chosen_meal["protein"],
                "carbs": chosen_meal["carbs"],
                "fats": chosen_meal["fats"]
            })

    # Calculate total nutrients
    total_nutrients = {
        "calories": sum([meal["calories"] for meal in meal_plan]),
        "protein": sum([meal["protein"] for meal in meal_plan]),
        "carbs": sum([meal["carbs"] for meal in meal_plan]),
        "fats": sum([meal["fats"] for meal in meal_plan])
    }

    # Debug: print total nutrients and the final meal plan
    print(f"Final Meal Plan: {meal_plan}")
    print(f"Total Nutrients: {total_nutrients}")

    return meal_plan, total_nutrients
# Function to generate meals based on predicted calories and preferences
def handle_form_submission(age, weight, gender, activity_level, goal, dietary_restrictions, allergies, vegetarian):
    predicted_calories = generate_calories(age, weight, gender, activity_level, goal)
    
    # Debug: print predicted calories to ensure correctness
    print(f"Predicted Calories: {predicted_calories}")
    
    diet_plan, nutrients = generate_meals(predicted_calories, vegetarian, dietary_restrictions, allergies)
    
    # Debug: print the diet plan and nutrients
    print(f"Generated Diet Plan: {diet_plan}")
    print(f"Generated Nutrients: {nutrients}")
    
    return diet_plan, nutrients
