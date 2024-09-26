from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)


# Existing Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/diet-plan-page")
def diet_plan_page():
    return render_template("diet-plan.html")


@app.route("/fitness-plan-page")
def fitness_plan_page():
    workout_data = [30, 45, 60, 40, 50, 70, 65]
    body_measurements = [70, 68, 66, 65]
    goal_progress = [75, 25]
    return render_template(
        "fitness-plan.html",
        workout_data=workout_data,
        body_measurements=body_measurements,
        goal_progress=goal_progress,
    )


# Load the database
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


@app.route("/progress-page")
def progress_page():
    # Load data from the database
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

    # Render the progress-page template
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
    return render_template("log-workout.html")


# Route to handle form submission and save workout data
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
            "exercises": exercises
        }
    except ValueError:
        return "Invalid input", 400  # Handle invalid inputs gracefully

    # Add new workout to the database and save it
    database["workouts"].append(new_workout)
    save_database(database)

    # Redirect to a confirmation or progress page
    return redirect(
        url_for("show_log_workout_page")
    )  # Redirect to the same form page after submission


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")


@app.route("/contact-us-page")
def contact_us_page():
    return render_template("contact-us.html")


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

@app.route("/profile-page")
def profile_page():
    return render_template("profile.html")


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


if __name__ == "__main__":
    app.run(debug=True)
