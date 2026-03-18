from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

correct_password = "admin123"
attempts = 0
max_attempts = 5


# Log function
def log_attempt(ip, status):
    with open("log.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} | IP: {ip} | {status}\n")


@app.route("/", methods=["GET", "POST"])
def login():
    global attempts
    message = ""
    alert = False

    if request.method == "POST":
        password = request.form["password"]
        ip = request.remote_addr

        if password == correct_password:
            message = "✅ Login Successful"
            attempts = 0
            log_attempt(ip, "SUCCESS")

        else:
            attempts += 1
            log_attempt(ip, "FAILED")

            if attempts < 3:
                message = f"❌ Incorrect Password ({attempts})"
            elif attempts < max_attempts:
                message = "⚠️ Warning: Multiple failed attempts!"
            else:
                message = "🚨 ALERT: Password Cracking Attempt Detected!"
                alert = True

    return render_template("login.html", message=message, alert=alert)


if __name__ == "__main__":
    app.run(debug=True)