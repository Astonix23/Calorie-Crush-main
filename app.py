from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import random
from diet_plan_gen import *

app = Flask(__name__)
app.secret_key = "\xae7)\xa0\n\xb9J\xa4\xe3\x9aD\xd6\xb0$&\xad\x1b\x8a\xc6z\x1d%V\xbe"

COMMUNITY_DB_FILE = "community_database.json"


EXERCISE_CATEGORIES = {
    "Upper Body": {
        "Bodyweight": [
            "Pushups",
            "Tricep Dips",
            "Plank to Pushup",
            "Decline Pushups",
            "Diamond Pushups",
            "Plank",
        ],
        "Dumbbells": [
            "Dumbbell Bench Press",
            "Dumbbell Shoulder Press",
            "Dumbbell Rows",
            "Dumbbell Bicep Curl",
            "Dumbbell Lateral Raise",
            "Dumbbell Tricep Kickback",
            "Dumbbell Chest Fly",
            "Dumbbell Arnold Press",
            "Dumbbell Renegade Row",
            "Dumbbell Hammer Curl",
            "Dumbbell Shrugs",
        ],
        "Barbells": [
            "Barbell Bench Press",
            "Barbell Shoulder Press",
            "Barbell Rows",
            "Barbell Bicep Curl",
        ],
        "Kettlebells": [
            "Kettlebell Shoulder Press",
            "Kettlebell Rows",
            "Kettlebell Tricep Extension",
            "Kettlebell Chest Press",
            "Kettlebell Windmill",
        ],
        "Resistance Bands": [
            "Band Pull-Apart",
            "Band Chest Press",
            "Band Rows",
            "Band Bicep Curl",
            "Band Tricep Pushdown",
        ],
    },
    "Lower Body": {
        "Bodyweight": [
            "Bodyweight Squats",
            "Lunges",
            "Wall Sit",
            "Glute Bridge",
            "Step-ups",
        ],
        "Dumbbells": [
            "Dumbbell Squat",
            "Dumbbell Lunges",
            "Dumbbell Deadlift",
            "Dumbbell Step-ups",
            "Dumbbell Goblet Squat",
            "Dumbbell Bulgarian Split Squat",
            "Dumbbell Calf Raise",
        ],
        "Barbells": ["Barbell Squats", "Barbell Deadlift", "Barbell Lunges"],
        "Kettlebells": [
            "Kettlebell Goblet Squat",
            "Kettlebell Deadlift",
            "Kettlebell Lunges",
            "Kettlebell Step-ups",
            "Kettlebell Pistol Squat",
        ],
        "Resistance Bands": [
            "Band Squat",
            "Band Lunges",
            "Band Deadlift",
            "Band Kickbacks",
            "Band Glute Bridge",
        ],
    },
    "Full Body": {
        "Bodyweight": [
            "Burpees",
            "Mountain Climbers",
            "Jumping Jacks",
            "Bear Crawl",
            "Squat Jumps",
        ],
        "Dumbbells": [
            "Dumbbell Clean and Press",
            "Dumbbell Snatch",
            "Dumbbell Turkish Get-up",
            "Dumbbell Thruster",
            "Dumbbell Burpee",
        ],
        "Barbells": ["Barbell Clean and Press", "Barbell Snatch"],
        "Kettlebells": [
            "Kettlebell Clean and Press",
            "Kettlebell Swing",
            "Kettlebell Snatch",
            "Kettlebell Turkish Get-up",
            "Kettlebell Figure-8",
        ],
    },
    "Cardio": {
        "Cardio": [
            "Running",
            "Cycling",
            "Jump Rope",
            "Swimming",
            "Rowing",
            "High Knees",
            "Box Jumps",
        ]
    },
    "Yoga": {
        "Yoga/Stretching": [
            "Downward Dog",
            "Child’s Pose",
            "Warrior II",
            "Cobra Stretch",
            "Cat-Cow Stretch",
            "Pigeon Pose",
            "Seated Forward Bend",
            "Bridge Pose",
            "Lunge Stretch",
            "Standing Forward Fold",
        ]
    },
}


def generate_workout(fitness_goal, experience_level, equipment):
    # Sets and reps configuration based on experience level
    sets, reps, rest_period, additional_exercises = 2, 10, 60, 0
    supersets, tempo_control, pyramid_sets = False, False, False

    # Modify intensity based on experience level
    if experience_level == "Beginner":
        sets, reps, rest_period = 2, 10, 60
    elif experience_level == "Intermediate":
        sets, reps, rest_period = 3, 8, 45
        supersets = True
        additional_exercises = 1
    elif experience_level == "Advanced":
        sets, reps, rest_period = 4, 6, 30
        supersets = True
        tempo_control = True
        additional_exercises = 2
        pyramid_sets = True  # Add pyramid-style training for advanced users

    workout_plan = []
    day_count = 1

    # Helper to generate exercises based on categories and equipment
    def generate_day_plan(day_type):
        exercises = []
        for equip in equipment:
            exercises += EXERCISE_CATEGORIES[day_type].get(equip, [])

        # Add additional exercises for intermediate/advanced users
        exercises = random.sample(
            exercises, min(4 + additional_exercises, len(exercises))
        )

        # Apply advanced techniques for advanced users
        if supersets:
            exercises = [
                f"{ex1} + {ex2} 🔴" for ex1, ex2 in zip(exercises[::2], exercises[1::2])
            ]
        if tempo_control:
            exercises = [f"{ex} 🟠" for ex in exercises]
        if pyramid_sets:
            exercises = [f"{ex} 🔵" for ex in exercises]

        return exercises

    # Upper Body Day
    upper_body_exercises = generate_day_plan("Upper Body")
    workout_plan.append(
        {
            "Day": f"Day {day_count}: Upper Body",
            "Exercises": upper_body_exercises,
            "Sets": sets,
            "Reps": reps,
            "Rest Period": rest_period,
        }
    )
    day_count += 1

    # Lower Body Day
    lower_body_exercises = generate_day_plan("Lower Body")
    workout_plan.append(
        {
            "Day": f"Day {day_count}: Lower Body",
            "Exercises": lower_body_exercises,
            "Sets": sets,
            "Reps": reps,
            "Rest Period": rest_period,
        }
    )
    day_count += 1

    # Full Body Day
    full_body_exercises = generate_day_plan("Full Body")
    workout_plan.append(
        {
            "Day": f"Day {day_count}: Full Body",
            "Exercises": full_body_exercises,
            "Sets": sets,
            "Reps": reps,
            "Rest Period": rest_period,
        }
    )
    day_count += 1

    # Cardio/Rest Day (Optional for Advanced)
    if (
        fitness_goal in ["Lose Weight", "Increase Endurance"]
        or experience_level != "Beginner"
    ):
        cardio_exercises = random.sample(EXERCISE_CATEGORIES["Cardio"]["Cardio"], 2)
        yoga_exercises = random.sample(
            EXERCISE_CATEGORIES["Yoga"]["Yoga/Stretching"], 2
        )
        workout_plan.append(
            {
                "Day": f"Day {day_count}: Cardio & Yoga",
                "Exercises": cardio_exercises + yoga_exercises,
                "Rest Period": 30,
            }
        )

    # Optional advanced days for upper and lower body
    if experience_level != "Beginner":
        # Upper Body 2
        upper_body_exercises_2 = generate_day_plan("Upper Body")
        workout_plan.append(
            {
                "Day": f"Day {day_count + 1}: Upper Body 2",
                "Exercises": upper_body_exercises_2,
                "Sets": sets,
                "Reps": reps,
                "Rest Period": rest_period,
            }
        )
        day_count += 1

        # Lower Body 2
        lower_body_exercises_2 = generate_day_plan("Lower Body")
        workout_plan.append(
            {
                "Day": f"Day {day_count + 1}: Lower Body 2",
                "Exercises": lower_body_exercises_2,
                "Sets": sets,
                "Reps": reps,
                "Rest Period": rest_period,
            }
        )

    # Save workout plan to session
    session["generated_plan"] = workout_plan
    session["current_day"] = 0  # Start from Day 1

    return workout_plan


@app.route("/generate-fitness-plan", methods=["POST"])
def generate_fitness_plan():
    # Get form data
    fitness_goal = request.form.get("goal")
    experience_level = request.form.get("experience")
    equipment = request.form.getlist("equipment")

    # Generate workout plan using the advanced generator
    workout_plan = generate_workout(fitness_goal, experience_level, equipment)

    # Render the fitness plan page with the generated workout plan
    return render_template("fitness-plan.html", generated_plan=workout_plan)


# Route to display the form for creating the fitness plan
@app.route("/fitness-plan-page", methods=["GET"])
def fitness_plan_page():
    return render_template("fitness-plan.html")


def load_users():
    try:
        with open("users.json", "r") as file:
            users_data = json.load(file)
            # Ensure the file has a valid structure, even if it's empty
            if "users" not in users_data:
                return {"users": []}
            return users_data
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is missing or empty/corrupt, return an empty structure
        return {"users": []}


# Save users to the database
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


def load_database():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"workouts": []}


# Save the database
def save_database(data):
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)


# Existing Routes
@app.route("/")
def index():
    logged_in = "user" in session
    # Check if the user is logged in by looking for the 'user' key in the session
    if "user" in session:
        # The user is logged in, so they can see the full version of the page
        return render_template("index.html", logged_in=True)
    else:
        # The user is not logged in, show a restricted version of the page
        return render_template("index.html", logged_in=False)


@app.route("/diet-plan-page")
def diet_plan():
    return render_template("diet-plan.html")

@app.route("/generate-diet-plan", methods=["POST"])
def generate_diet_plan():
    # Collect user input from the form
    age = int(request.form["age"])
    weight = float(request.form["weight"])
    gender = request.form["gender"]
    activity_level = int(request.form["activity_level"])
    goal = request.form["goal"]
    dietary_restrictions = request.form.get("dietary_restrictions", "")
    vegetarian = request.form.get("vegetarian") == "Yes"  # Handle vegetarian preference

    # Debug: print user inputs to check if they are captured correctly
    print(f"Age: {age}, Weight: {weight}, Gender: {gender}, Activity Level: {activity_level}")
    print(f"Goal: {goal}, Dietary Restrictions: {dietary_restrictions}, Vegetarian: {vegetarian}")

    # Generate the diet plan (using your handle_form_submission function)
    diet_plan, nutrients = handle_form_submission(
        age,
        weight,
        gender,
        activity_level,
        goal,
        dietary_restrictions,
        vegetarian
    )

    # Debug: print diet plan and nutrients to check if they are generated correctly
    print(f"Diet Plan: {diet_plan}")
    print(f"Nutrients: {nutrients}")

    # Render the diet plan page with the generated diet plan
    return render_template("diet-plan.html", diet_plan=diet_plan, nutrients=nutrients)



@app.route("/log-workout-page", methods=["GET", "POST"])
def log_workout():
    database = load_database()

    if request.method == "POST":
        weight = request.form.get("weight")
        duration = request.form.get("duration")
        exercises = request.form.getlist("exercise")

        # MET value: assume moderate intensity for now
        MET_value = 5

        # Calories burned calculation (basic formula)
        try:
            weight = float(weight)
            duration = int(duration)
            calories_burned = (MET_value * weight * 3.5 / 200) * duration
        except ValueError:
            return "Invalid input", 400  # Handle invalid inputs gracefully

        # Create a new workout entry with calories burned
        new_workout = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": weight,
            "duration": duration,
            "exercises": exercises,
            "calories_burned": round(
                calories_burned, 2
            ),  # This line ensures calories are recorded
            "notes": request.form.get("notes", ""),
        }

        # Add new workout to the database and save it
        database["workouts"].append(new_workout)
        save_database(database)

        # Increment the day index after logging the workout
        session["current_day"] = session.get("current_day", 0) + 1

        # Redirect to the same form page after submission
        return redirect(url_for("log_workout"))

    # For GET requests, render the log workout page
    # Fetch the current day’s exercises from the fitness plan
    generated_plan = session.get("generated_plan", [])
    current_day = session.get("current_day", 0)

    # Ensure we don't go out of bounds with the current day index
    if current_day >= len(generated_plan):
        current_day = len(generated_plan) - 1  # Stay on the last day

    # Get the exercises for the current day
    day_plan = generated_plan[current_day]
    exercises = day_plan["Exercises"]

    return render_template("log-workout.html", exercises=exercises, day=day_plan["Day"])


@app.route("/progress-page")
def progress_page():
    database = load_database()  # Load the database

    # Retrieve workout data
    workouts = database.get("workouts", [])

    # Safely calculate total calories burned
    total_calories_burned = sum(
        workout.get("calories_burned", 0) for workout in workouts
    )

    # Sum total workout time
    total_workout_time = sum(workout.get("duration", 0) for workout in workouts)

    # Get last 7 workout durations
    if workouts:
        recent_workouts = workouts[-7:]  # Get the last 7 workouts
        workout_durations = [workout.get("duration", 0) for workout in recent_workouts]
    else:
        workout_durations = [0] * 7  # Default to 0 if no data

    # Get latest body weight (from the last logged workout)
    body_weight = (
        workouts[-1]["weight"] if workouts else 70
    )  # Default to 70 if no workout data
    body_measurements = (
        [workout["weight"] for workout in workouts[-4:]] if workouts else []
    )  # Last 4 weight entries for the line graph

    return render_template(
        "progress.html",
        total_workout_time=total_workout_time,
        total_calories_burned=total_calories_burned,
        workout_data=workout_durations,
        body_weight=body_weight,
        body_measurements=body_measurements,
        goal_progress=[80, 20],  # Example goal progress: 80% done
        goal_completion=80,  # Assuming goal_progress[0] is the completion percentage
    )


@app.route("/signup-page", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password)
        users_db = load_users()

        # Check if the email is already registered
        for user in users_db["users"]:
            if user["email"] == email:
                return "Email already exists", 400

        new_user = {"name": name, "email": email, "password": hashed_password}
        users_db["users"].append(new_user)
        save_users(users_db)

        return redirect(url_for("login_or_profile"))

    return render_template("signup.html")


@app.route("/login-profile-page", methods=["GET", "POST"])
def login_or_profile():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        users_db = load_users()

        for user in users_db["users"]:
            if user["email"].lower() == email:
                if check_password_hash(user["password"], password):
                    session["user"] = user["name"]
                    return redirect(url_for("login_or_profile"))
                else:
                    error_message = "Invalid password. Please try again."
                    return render_template("login.html", error=error_message)

        error_message = "Email not found. Please try again."
        return render_template("login.html", error=error_message)

    # Ensure that the data passed is serializable
    if "user" in session:
        # Assuming you're passing user-specific data like stats
        workout_data = [30, 45, 60, 40, 50, 70, 80]  # Example data
        body_measurements = [70, 69, 68, 67]  # Example data
        goal_progress = [80, 20]  # Example data

        # Pass this data to the profile page
        return render_template(
            "profile.html",
            user=session["user"],
            workout_data=workout_data,
            body_measurements=body_measurements,
            goal_progress=goal_progress,
        )

    # If not logged in, show login form
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_or_profile"))


# Blog-related routes
posts = [
    {
        "id": 1,
        "title": "My Fitness Journey",
        "content": "Started my fitness journey with Calorie Crush. The personalized plan is amazing!",
        "author": "John Doe",
        "comments": [{"author": "Jane", "comment": "Great work! Keep going!"}],
    }
]


def load_community_database():
    try:
        with open("community_database.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is missing or empty/corrupt, return an empty structure
        return {"posts": []}


def save_community_database(data):
    with open("community_database.json", "w") as file:
        json.dump(data, file, indent=4)


next_post_id = (
    2  # This can be dynamically set by checking the highest ID in the file if needed
)


# Route to display the community page with blog posts
@app.route("/community-page")
def community_page():
    # Load posts from the community database
    database = load_community_database()
    posts = database.get("posts", [])

    return render_template("community.html", posts=posts)


# Route to create a new post
@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    global next_post_id
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author")

        new_post = {
            "id": next_post_id,
            "title": title,
            "content": content,
            "author": author,
            "comments": [],
        }

        # Load the community database
        database = load_community_database()

        # Add the new post to the database
        database["posts"].append(new_post)
        next_post_id += 1

        # Save the updated community database
        save_community_database(database)

        return redirect(url_for("community_page"))

    return render_template("create-post.html")


# Route to view post details including comments
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    # Load posts from the community database
    database = load_community_database()
    post = next((p for p in database["posts"] if p["id"] == post_id), None)

    if post:
        return render_template("post-detail.html", post=post)
    return "Post not found", 404


# Route to add a comment to a post
@app.route("/add-comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    author = request.form["author"]
    comment = request.form["comment"]

    # Load the community database
    database = load_community_database()

    # Find the correct post and append the comment
    for post in database["posts"]:
        if post["id"] == post_id:
            post["comments"].append({"author": author, "comment": comment})
            break

    # Save the updated community database
    save_community_database(database)

    return redirect(url_for("post_detail", post_id=post_id))


@app.route("/contact-us-page")
def contact_us_page():
    return render_template("contact-us.html")


if __name__ == "__main__":
    app.run(debug=True)
