from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for flash messages

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

# ✅ CONTACT ROUTE WITH POST + EMAIL SENDING
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # ===== EMAIL CONFIG (GMAIL SMTP) =====
        
        
        sender_email = os.environ.get("EMAIL_USER")
        sender_password = os.environ.get("EMAIL_PASSWORD")
        receiver_email = os.environ.get("RECEIVER_EMAIL")

        print("EMAIL_USER:", sender_email )
        print("EMAIL_PASSWORD:", sender_password)   
        print("RECEIVER_EMAIL:", receiver_email)        
        

        subject = "New Portfolio Contact Message"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        email_message = f"Subject: {subject}\n\n{body}"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, email_message)
            # server = smtplib.SMTP("smtp.gmail.com", 587)
            # server.starttls()
            # server.login(sender_email, sender_password)
            # server.sendmail(sender_email, receiver_email, email_message)
            # server.quit()

            flash("✅ Message sent successfully! I will reply you shortly.")
        except Exception as e:
            flash("❌ Message failed to send. Please try again later.")
            print("ERROR:", e)

        return redirect(url_for("contact"))

    return render_template("contact.html")

# ================= RUN SERVER =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# if __name__ == "__main__":
#     app.run(debug=True) 