import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

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

# ================= CONTACT ROUTE (SendGrid) =================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message_text = request.form.get("message")

        # Use your verified SendGrid sender
        sender_email = 'vitalaandrew@gmail.com'  # VERIFIED sender
        receiver_email = 'vitalaandrew@gmail.com'  # Where emails will be receiving messages
        api_key = os.environ.get("SENDGRID_API_KEY")  # From Render Environment Variables

        # Create the email
        message = Mail(
            from_email=sender_email,
            to_emails=receiver_email,
            subject="New Portfolio Contact Message",
            html_content=f"<p><strong>Name:</strong> {name}<br>"
                         f"<strong>Email:</strong> {email}<br>"
                         f"<strong>Message:</strong><br>{message_text}</p>"
        )

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
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