from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

MAX_ATTEMPTS = 5

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    game_over = False

    # Initialize game
    if "number" not in session or "attempts" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
            session["attempts"] += 1

            if guess == session["number"]:
                message = f"🎉 Correct! The number was {session['number']}."
                game_over = True
            elif guess < session["number"]:
                message = "🔻 Too low!"
            else:
                message = "🔺 Too high!"

            if session["attempts"] >= MAX_ATTEMPTS and guess != session["number"]:
                message = f"❌ Out of attempts! The number was {session['number']}."
                game_over = True

        except ValueError:
            message = "⚠️ Please enter a valid number."

    return render_template("index.html", message=message, game_over=game_over, attempts=session.get("attempts", 0))

@app.route("/restart")
def restart():
    session.pop("number", None)
    session.pop("attempts", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
