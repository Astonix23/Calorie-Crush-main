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