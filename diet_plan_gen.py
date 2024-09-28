import pandas as pd
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump, load


meals_data = [
    # Vegetarian Healthy Meals (Breakfast, Lunch, Dinner)
    {"name": "Poha (Flattened Rice)", "calories": 250, "protein": 4, "carbs": 45, "fats": 5, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},
    {"name": "Upma (Semolina)", "calories": 300, "protein": 6, "carbs": 50, "fats": 8, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},
    {"name": "Idli with Sambar", "calories": 250, "protein": 5, "carbs": 45, "fats": 3, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},
    {"name": "Aloo Paratha with Curd", "calories": 400, "protein": 10, "carbs": 60, "fats": 15, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},
    {"name": "Dosa with Coconut Chutney", "calories": 350, "protein": 7, "carbs": 60, "fats": 8, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},
    {"name": "Sabudana Khichdi", "calories": 300, "protein": 5, "carbs": 55, "fats": 8, "vegetarian": True, "meal_type": "meal", "meal_time": "breakfast"},

    {"name": "Rajma Chawal", "calories": 450, "protein": 15, "carbs": 70, "fats": 10, "vegetarian": True, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Palak Paneer with Roti", "calories": 400, "protein": 20, "carbs": 40, "fats": 15, "vegetarian": True, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Vegetable Biryani", "calories": 400, "protein": 10, "carbs": 60, "fats": 15, "vegetarian": True, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Paneer Butter Masala with Naan", "calories": 600, "protein": 25, "carbs": 60, "fats": 35, "vegetarian": True, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Baingan Bharta with Chapati", "calories": 350, "protein": 7, "carbs": 45, "fats": 12, "vegetarian": True, "meal_type": "meal", "meal_time": "lunch"},

    {"name": "Vegetable Pulao", "calories": 400, "protein": 10, "carbs": 60, "fats": 12, "vegetarian": True, "meal_type": "meal", "meal_time": "dinner"},
    {"name": "Masoor Dal with Brown Rice", "calories": 350, "protein": 15, "carbs": 55, "fats": 5, "vegetarian": True, "meal_type": "meal", "meal_time": "dinner"},
    {"name": "Dal Makhani with Rice", "calories": 500, "protein": 18, "carbs": 70, "fats": 20, "vegetarian": True, "meal_type": "meal", "meal_time": "dinner"},
    {"name": "Bhindi Masala with Roti", "calories": 300, "protein": 8, "carbs": 45, "fats": 10, "vegetarian": True, "meal_type": "meal", "meal_time": "dinner"},
    
    # Non-Vegetarian Healthy Meals
    {"name": "Grilled Chicken Breast with Steamed Broccoli", "calories": 400, "protein": 40, "carbs": 30, "fats": 10, "vegetarian": False, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Baked Salmon with Quinoa", "calories": 450, "protein": 35, "carbs": 35, "fats": 15, "vegetarian": False, "meal_type": "meal", "meal_time": "dinner"},
    {"name": "Tandoori Chicken with Salad", "calories": 350, "protein": 40, "carbs": 10, "fats": 15, "vegetarian": False, "meal_type": "meal", "meal_time": "lunch"},
    {"name": "Butter Chicken with Naan", "calories": 600, "protein": 30, "carbs": 50, "fats": 35, "vegetarian": False, "meal_type": "meal", "meal_time": "dinner"},
    {"name": "Shrimp Curry with Rice", "calories": 450, "protein": 35, "carbs": 50, "fats": 10, "vegetarian": False, "meal_type": "meal", "meal_time": "dinner"},

    # Snacks (for after lunch or in the evening)
    {"name": "Apple Slices with Peanut Butter", "calories": 200, "protein": 6, "carbs": 25, "fats": 10, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"},
    {"name": "Carrot and Hummus", "calories": 150, "protein": 5, "carbs": 20, "fats": 8, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"},
    {"name": "Mixed Nuts", "calories": 200, "protein": 6, "carbs": 15, "fats": 15, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"},
    {"name": "Greek Yogurt with Honey", "calories": 250, "protein": 15, "carbs": 25, "fats": 10, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"},
    {"name": "Chana Chaat", "calories": 200, "protein": 10, "carbs": 30, "fats": 5, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"},
    {"name": "Makhana (Roasted Foxnuts)", "calories": 150, "protein": 4, "carbs": 20, "fats": 7, "vegetarian": True, "meal_type": "snack", "meal_time": "evening"}
]
# Generate sample data for AI/ML model
def generate_sample_data(num_samples=100):
    age = np.random.randint(18, 60, num_samples)
    weight = np.random.randint(50, 120, num_samples)
    activity_level = np.random.randint(1, 6, num_samples)
    goal = np.random.randint(0, 3, num_samples)

    # Basic calorie calculation logic for generating sample data
    calories_needed = weight * 30 + (activity_level - 3) * 100 + np.random.randint(-100, 100, num_samples)
    calories_needed = np.where(goal == 1, calories_needed - 500, calories_needed)  # Lose weight
    calories_needed = np.where(goal == 2, calories_needed + 500, calories_needed)  # Gain muscle

    X = np.column_stack((age, weight, activity_level, goal))
    y = calories_needed

    return X, y

# Train and save the ML model
def train_and_save_model():
    X, y = generate_sample_data(num_samples=500)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    model_filename = 'calories_predictor_model.joblib'
    dump(model, model_filename)
    
    print(f"Model trained and saved to {model_filename}")
    return model

# Load the trained model
def load_trained_model(filename='calories_predictor_model.joblib'):
    model = load(filename)
    return model

def predict_calories_with_ai(age, weight, activity_level, goal):
    model = load_trained_model()  # Load the saved model

    # Convert 'goal' to numeric: 0 for 'Maintain Weight', 1 for 'Lose Weight', 2 for 'Gain Muscle'
    goal_mapping = {
        "Maintain Weight": 0,
        "Lose Weight": 1,
        "Gain Muscle": 2
    }

    if goal not in goal_mapping:
        raise ValueError(f"Invalid goal: {goal}")

    # Prepare the input data
    input_data = np.array([[age, weight, activity_level, goal_mapping[goal]]], dtype=float)
    
    # Predict the calories
    predicted_calories = model.predict(input_data)
    
    return int(predicted_calories)

# Existing calorie estimation logic
def generate_calories(age, weight, gender, activity_level, goal):
    # Use AI/ML model for calorie prediction
    predicted_calories_ai = predict_calories_with_ai(age, weight, activity_level, goal)
    print(f"Predicted calories (AI): {predicted_calories_ai}")
    
    return predicted_calories_ai

def generate_meals(predicted_calories, vegetarian=False, dietary_restrictions=None):
    meal_plan = []
    chosen_meals = []

    # Total nutrients to calculate
    total_nutrients = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0
    }

    # Filter meals based on vegetarian preference
    suitable_meals = [meal for meal in meals_data if meal['vegetarian'] or not vegetarian]

    # Filter meals based on dietary restrictions
    if dietary_restrictions and dietary_restrictions != "None":
        suitable_meals = [meal for meal in suitable_meals if dietary_restrictions in meal.get("dietary_restrictions", [])]

    # Separate snacks and meals
    meals = [meal for meal in suitable_meals if meal.get("meal_type") == "meal"]
    snacks = [meal for meal in suitable_meals if meal.get("meal_type") == "snack"]

    # Define calorie distribution for meals and snacks
    meal_distributions = {
        "breakfast": predicted_calories * 0.3,
        "lunch": predicted_calories * 0.4,
        "dinner": predicted_calories * 0.3
    }

    snack_distributions = {
        "evening_snack": predicted_calories * 0.1  # Assign 10% for evening snack
    }

    # Select meals based on calorie distribution (closest match)
    for meal_time, target_calories in meal_distributions.items():
        # Ensure there are meals for the given meal time
        suitable_meals_for_time = [meal for meal in meals if meal["meal_time"] == meal_time]
        if suitable_meals_for_time:
            # Sort to find the closest match
            sorted_meals = sorted(suitable_meals_for_time, key=lambda meal: abs(meal["calories"] - target_calories))
            chosen_meal = sorted_meals[0]  # Get the closest meal
            chosen_meals.append(chosen_meal)
            meal_plan.append({
                "meal_time": meal_time.title(),
                "name": chosen_meal["name"],
                "calories": chosen_meal["calories"],
                "protein": chosen_meal["protein"],
                "carbs": chosen_meal["carbs"],
                "fats": chosen_meal["fats"]
            })

            # Update total nutrients
            total_nutrients["calories"] += chosen_meal["calories"]
            total_nutrients["protein"] += chosen_meal["protein"]
            total_nutrients["carbs"] += chosen_meal["carbs"]
            total_nutrients["fats"] += chosen_meal["fats"]

    # Add evening snack (closest match)
    for snack_time, target_calories in snack_distributions.items():
        suitable_snacks_for_time = [snack for snack in snacks if snack["meal_time"] == "evening"]
        if suitable_snacks_for_time:
            # Sort to find the closest match
            sorted_snacks = sorted(suitable_snacks_for_time, key=lambda snack: abs(snack["calories"] - target_calories))
            chosen_snack = sorted_snacks[0]  # Get the closest snack
            chosen_meals.append(chosen_snack)
            meal_plan.append({
                "meal_time": snack_time.replace('_', ' ').title(),
                "name": chosen_snack["name"],
                "calories": chosen_snack["calories"],
                "protein": chosen_snack["protein"],
                "carbs": chosen_snack["carbs"],
                "fats": chosen_snack["fats"]
            })

            # Update total nutrients
            total_nutrients["calories"] += chosen_snack["calories"]
            total_nutrients["protein"] += chosen_snack["protein"]
            total_nutrients["carbs"] += chosen_snack["carbs"]
            total_nutrients["fats"] += chosen_snack["fats"]

    # Return the meal plan and the total nutrient breakdown
    return meal_plan, total_nutrients




# Function to handle form submission and use AI-calculated calories
def handle_form_submission(age, weight, gender, activity_level, goal, dietary_restrictions, vegetarian):
    predicted_calories = generate_calories(age, weight, gender, activity_level, goal)
    print(f"Predicted Calories: {predicted_calories}")
    
    diet_plan, nutrients = generate_meals(predicted_calories, vegetarian, dietary_restrictions)
    print(f"Generated Diet Plan: {diet_plan}")
    print(f"Generated Nutrients: {nutrients}")
    
    return diet_plan, nutrients

# Train and save the AI model (run this initially to generate and save the model)
train_and_save_model()