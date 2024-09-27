import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import random

# Step 1: Generate a Synthetic Dataset
def generate_calories(age, weight, gender, activity_level, goal):
    """Estimate calories using synthetic data logic similar to Mifflin-St Jeor equation."""
    # Base BMR calculation (simplified for synthetic data generation)
    if gender == "Male":
        bmr = 10 * weight + 6.25 * 175 - 5 * age + 5  # Assuming height = 175 cm for males
    else:
        bmr = 10 * weight + 6.25 * 165 - 5 * age - 161  # Assuming height = 165 cm for females

    # Activity level multiplier
    activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][activity_level - 1]
    calories = bmr * activity_multiplier
    
    # Adjust for goal (lose weight, maintain, gain muscle)
    if goal == "lose weight":
        calories -= 500
    elif goal == "gain muscle":
        calories += 500
    
    return int(calories)

# Generate a synthetic dataset
def generate_synthetic_data():
    """Create a synthetic dataset for training the RandomForestRegressor."""
    data = []
    for _ in range(1000):  # Generate 1000 synthetic records
        age = random.randint(18, 60)
        weight = random.randint(50, 100)
        gender = random.choice(["Male", "Female"])
        activity_level = random.randint(1, 5)  # 1 (sedentary) to 5 (very active)
        goal = random.choice(["lose weight", "maintain", "gain muscle"])
        calories = generate_calories(age, weight, gender, activity_level, goal)
        
        data.append([age, weight, gender, activity_level, goal, calories])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=["age", "weight", "gender", "activity_level", "goal", "calories"])
    return df

# Generate and save the synthetic dataset
df = generate_synthetic_data()

# Step 2: Preprocess the Data
# Convert gender and goal to numerical format
df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})
df['goal'] = df['goal'].map({'lose weight': 0, 'maintain': 1, 'gain muscle': 2})

# Features and target
X = df[['age', 'weight', 'gender', 'activity_level', 'goal']]
y = df['calories']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Integrate with Spoonacular API
API_KEY = 'yob3ed4a94a8b24f60aee3ba3f29374f6a '

def get_meals(predicted_calories, dietary_restrictions, allergies):
    """Fetch meal plan from Spoonacular API based on predicted calories and user preferences."""
    url = 'https://api.spoonacular.com/mealplanner/generate'
    params = {
        'apiKey': API_KEY,
        'timeFrame': 'day',
        'targetCalories': predicted_calories,
        'diet': dietary_restrictions,
        'exclude': allergies
    }
    
    response = requests.get(url, params=params)

    # Add this to see exactly what the API is returning
    print("API Response:", response.json())
    
    if response.status_code == 200:
        meals = response.json()['meals']
        nutrients = response.json()['nutrients']
        return meals, nutrients
    else:
        return None, None
meals = get_meals(2500, None, None)
print(meals)
# Step 5: Predict Daily Caloric Needs and Generate Diet Plan
def predict_calories(age, weight, gender, activity_level, goal):
    """Predict the daily calorie intake based on user inputs."""
    user_input = pd.DataFrame({
        'age': [age],
        'weight': [weight],
        'gender': [0 if gender.lower() == 'male' else 1],
        'activity_level': [activity_level],
        'goal': [0 if goal == 'lose weight' else 1 if goal == 'maintain' else 2]
    })
    
    predicted_calories = model.predict(user_input)
    return int(predicted_calories[0])

def generate_diet_plan(age, weight, gender, activity_level, goal, dietary_restrictions, allergies):
    """Generate a personalized diet plan based on user preferences and predicted calories."""
    # Predict daily caloric needs
    predicted_calories = predict_calories(age, weight, gender, activity_level, goal)
    
    # Get meals from Spoonacular API
    meals, nutrients = get_meals(predicted_calories, dietary_restrictions, allergies)
    
    if meals:
        diet_plan = []
        for meal in meals:
            # Only access the title string directly, no need for title()
            diet_plan.append({
                'title': meal['title'],  # Use the title directly as a string
                'meal_url': f"https://spoonacular.com/recipes/{meal['title']}-{meal['id']}",
                'image': meal['image']
            })
        return diet_plan, nutrients
    else:
        return "Sorry, no meals found for your preferences.", None

def handle_form_submission(age, weight, gender, activity_level, goal, dietary_restrictions, allergies):
    """Handle the form submission and generate a diet plan based on user input."""
    return generate_diet_plan(age, weight, gender, activity_level, goal, dietary_restrictions, allergies)