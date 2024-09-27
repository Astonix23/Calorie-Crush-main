from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "\xae7)\xa0\n\xb9J\xa4\xe3\x9aD\xd6\xb0$&\xad\x1b\x8a\xc6z\x1d%V\xbe"


EXERCISE_CATEGORIES = {
    "Upper Body": {
        "Bodyweight": ["Pushups", "Tricep Dips", "Plank"],
        "Dumbbells": [
            "Dumbbell Bench Press",
            "Dumbbell Shoulder Press",
            "Dumbbell Rows",
            "Dumbbell Bicep Curl",
        ],
        "Barbells": ["Barbell Bench Press", "Barbell Shoulder Press", "Barbell Rows"],
    },
    "Lower Body": {
        "Bodyweight": ["Squats", "Lunges", "Wall Sit", "Bicycle Crunches"],
        "Dumbbells": ["Dumbbell Squat", "Dumbbell Lunges", "Dumbbell Deadlift"],
        "Barbells": ["Barbell Squats", "Barbell Deadlift", "Barbell Lunges"],
    },
    "Full Body": {
        "Bodyweight": ["Burpees", "Mountain Climbers", "Jumping Jacks"],
        "Dumbbells": ["Dumbbell Clean and Press"],
        "Barbells": ["Barbell Clean and Press"],
    },
    "Cardio": {"Cardio": ["Cycling", "Running", "Jogging"]},
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


@app.route("/generate-fitness-plan", methods=["POST"])
def generate_fitness_plan():
    # Capture form data
    fitness_goal = request.form.get("goal")
    experience_level = request.form.get("experience")
    equipment = request.form.getlist("equipment")

    # Define sets and reps based on experience level
    if experience_level == "Beginner":
        sets = 2
        reps = 10
    elif experience_level == "Intermediate":
        sets = 3
        reps = 8
    else:  # Advanced
        sets = 4
        reps = 6

    # Initialize the workout plan list
    workout_plan = []

    # Day 1: Upper Body
    upper_body_exercises = []
    for equip in equipment:
        upper_body_exercises += EXERCISE_CATEGORIES["Upper Body"].get(equip, [])
    upper_body_exercises = random.sample(upper_body_exercises, min(4, len(upper_body_exercises)))  # Limit to 4 exercises
    workout_plan.append({"Day": "Day 1: Upper Body", "Exercises": upper_body_exercises, "Sets": sets, "Reps": reps})

    # Day 2: Lower Body
    lower_body_exercises = []
    for equip in equipment:
        lower_body_exercises += EXERCISE_CATEGORIES["Lower Body"].get(equip, [])
    lower_body_exercises = random.sample(lower_body_exercises, min(4, len(lower_body_exercises)))  # Limit to 4 exercises
    workout_plan.append({"Day": "Day 2: Lower Body", "Exercises": lower_body_exercises, "Sets": sets, "Reps": reps})

    # Day 3: Full Body
    full_body_exercises = []
    for equip in equipment:
        full_body_exercises += EXERCISE_CATEGORIES["Full Body"].get(equip, [])
    full_body_exercises = random.sample(full_body_exercises, min(3, len(full_body_exercises)))  # Limit to 3 exercises
    workout_plan.append({"Day": "Day 3: Full Body", "Exercises": full_body_exercises, "Sets": sets, "Reps": reps})

    # Add Rest Day with Yoga & Stretching and Light Cardio
    rest_day_exercises = []
    yoga_exercises = EXERCISE_CATEGORIES["Yoga"]["Yoga/Stretching"]
    rest_day_exercises += random.sample(yoga_exercises, min(3, len(yoga_exercises)))  # Limit to 3 yoga exercises

    if fitness_goal in ["Lose Weight", "Increase Endurance"]:
        cardio_exercises = EXERCISE_CATEGORIES["Cardio"]["Cardio"]
        rest_day_exercises += random.sample(cardio_exercises, min(2, len(cardio_exercises)))  # Limit to 2 cardio exercises

    workout_plan.append({"Day": "Rest Day: Yoga & Stretching + Cardio", "Exercises": rest_day_exercises})

    # For more experienced users (Intermediate, Advanced), add additional workout days
    if experience_level != "Beginner":
        upper_body_exercises_2 = random.sample(upper_body_exercises, min(3, len(upper_body_exercises)))
        lower_body_exercises_2 = random.sample(lower_body_exercises, min(3, len(lower_body_exercises)))
        workout_plan.append({"Day": f"Day {len(workout_plan) + 1}: Upper Body 2", "Exercises": upper_body_exercises_2, "Sets": sets, "Reps": reps})
        workout_plan.append({"Day": f"Day {len(workout_plan) + 1}: Lower Body 2", "Exercises": lower_body_exercises_2, "Sets": sets, "Reps": reps})

    # Debugging: print the workout plan to the console
    print(f"Generated Workout Plan: {workout_plan}")

    # Render the template with the generated workout plan
    return render_template("fitness-plan.html", generated_plan=workout_plan)



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
    return render_template("index.html")


@app.route("/diet-plan-page")
def diet_plan_page():
    return render_template("diet-plan.html")


@app.route("/fitness-plan-page")
def fitness_plan_page():
    return render_template("fitness-plan.html")


@app.route("/progress-page")
def progress_page():
    database = load_database()

    # Ensure that workouts, body_measurements, and goal_progress exist in the database
    workouts = database.get("workouts", [])
    body_measurements = database.get(
        "body_measurements", [70, 68, 66, 65]
    )  # Default example values
    goal_progress = database.get("goal_progress", [75, 25])  # Default 75% complete

    if not workouts:
        total_workout_time = 0
        workout_data = []
    else:
        total_workout_time = sum(workout.get("duration", 0) for workout in workouts)
        recent_workouts = workouts[-7:]
        workout_data = [workout.get("duration", 0) for workout in recent_workouts]

    return render_template(
        "progress.html",
        total_workout_time=total_workout_time,
        workout_data=workout_data,
        body_measurements=body_measurements,
        goal_progress=goal_progress,
        workouts=workouts,
    )


# Route to serve the form
@app.route("/log-workout-page", methods=["GET"])
def show_log_workout_page():
    # Retrieve the exercises generated in the fitness plan, or use Bodyweight as the default
    exercises = session.get("generated_exercises")

    # Render the log workout page with the list of exercises
    return render_template("log-workout.html", exercises=exercises)


@app.route("/log-workout-page", methods=["POST"])
def log_workout():
    database = load_database()

    # Retrieve form data
    weight = request.form.get("weight")
    duration = request.form.get("duration")
    exercises = request.form.getlist("exercise")  # Get multiple checkbox values

    # Create a new workout entry
    try:
        new_workout = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": float(weight),
            "duration": int(duration),
            "exercises": exercises,
            "notes": request.form.get("notes", ""),
        }
    except ValueError:
        return "Invalid input", 400  # Handle invalid inputs gracefully

    # Add new workout to the database and save it
    database["workouts"].append(new_workout)
    save_database(database)

    # Redirect to the same form page after submission
    return redirect(url_for("show_log_workout_page"))


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

    data = request.get_json()
    content = data.get('content')
    
    # Load existing data from users.json
    with open('users.json', 'r') as file:
        users = json.load(file)
    
    # Update the content (assuming you want to update a specific user's data)
    # Here, I'm just updating the first user's content for demonstration
    users[0]['content'] = content
    
    # Save the updated data back to users.json
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)
    
    return json.jsonify({'message': 'Content saved successfully!'})

    # Show profile if logged in
    if "user" in session:
        return render_template("profile.html", user=session["user"])
    else:
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

next_post_id = 2  # For generating post IDs


@app.route("/community-page")
def community_page():
    return render_template("community.html", posts=posts)


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    global next_post_id
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        new_post = {
            "id": next_post_id,
            "title": title,
            "content": content,
            "author": author,
            "comments": [],
        }
        posts.append(new_post)
        next_post_id += 1
        return redirect(url_for("community_page"))
    return render_template("create-post.html")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        return render_template("post-detail.html", post=post)
    return "Post not found", 404


@app.route("/add-comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    author = request.form["author"]
    comment = request.form["comment"]
    for post in posts:
        if post["id"] == post_id:
            post["comments"].append({"author": author, "comment": comment})
            break
    return redirect(url_for("post_detail", post_id=post_id))


@app.route("/contact-us-page")
def contact_us_page():
    return render_template("contact-us.html")


if __name__ == "__main__":
    app.run(debug=True)