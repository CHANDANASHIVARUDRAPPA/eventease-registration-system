from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import csv, smtplib, os
from email.message import EmailMessage
from datetime import datetime
from config import SMTP_EMAIL, SMTP_PASSWORD, HOST_EMAIL
from flask import session
from config import ADMIN_USERNAME, ADMIN_PASSWORD

app = Flask(__name__)
app.secret_key = 'your_secret_key'

REGISTRATION_FILE = 'registrations.csv'
UPLOAD_FOLDER = 'static/proofs'
MAX_REGISTRATIONS = 50
MAX_UPLOAD_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# Ensure proofs folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def count_registrations():
    if not os.path.exists(REGISTRATION_FILE):
        return 0
    with open(REGISTRATION_FILE, 'r') as f:
        return sum(1 for _ in csv.reader(f))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(msg)

@app.route('/')
def form():
    count = count_registrations()
    percent = int((count / MAX_REGISTRATIONS) * 100)
    if count >= MAX_REGISTRATIONS:
        return render_template('closed.html')
    return render_template('form.html', count=count, percent=percent)

@app.route('/submit', methods=['POST'])
def submit():
    if count_registrations() >= MAX_REGISTRATIONS:
        return render_template('closed.html')

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    college = request.form['college']
    branch = request.form['branch']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ref_id = f"REG2025_{count_registrations() + 1000:04d}"

    with open(REGISTRATION_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, email, phone, college, branch, ref_id])

    user_msg = f"""Hi {name},

Thank you for registering for the Power BI Bootcamp!
We have received your details.

Your Reference ID: {ref_id}

Please complete the payment using the QR code and upload your payment proof.

Regards,
Bootcamp Team"""

    host_msg = f"""New registration received:

Name: {name}
Email: {email}
Phone: {phone}
College: {college}
Branch: {branch}
Ref ID: {ref_id}
Time: {timestamp}
"""

    send_email(email, "Power BI Bootcamp Registration Confirmation", user_msg)
    send_email(HOST_EMAIL, "New Bootcamp Registration", host_msg)

    return render_template('qr.html', ref_id=ref_id)

@app.route('/upload-proof', methods=['POST'])
def upload_proof():
    ref_id = request.form['ref_id']
    file = request.files['proof']

    if file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
        filename = secure_filename(f"{ref_id}_{file.filename}")
        filepath = os.path.join('static/proofs', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        updated_rows = []
        participant = None

        with open(REGISTRATION_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 6 and row[6] == ref_id:
                    if len(row) == 7:
                        row.append(filepath)
                    else:
                        row[7] = filepath
                    participant = row  # Save the participant row
                updated_rows.append(row)

        with open(REGISTRATION_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)

        # Send final confirmation email only AFTER successful proof upload
        if participant:
            name, email = participant[1], participant[2]
            user_msg = f"""Hi {name},

Your registration for the Power BI Bootcamp is complete!

We have received your details and payment proof.

Your Reference ID: {ref_id}

We will get in touch with further event details.

Thank you for joining!

– Bootcamp Team"""

            send_email(email, " Power BI Bootcamp – Registration Confirmed", user_msg)

        return redirect(url_for('success', ref=ref_id))

    return "Invalid file format", 400

@app.route('/success')
def success():
    ref_id = request.args.get('ref', 'REG2025_XXXX')
    return render_template('success.html', ref_id=ref_id)

@app.route('/admin')
def admin_dashboard():
    if not os.path.exists(REGISTRATION_FILE):
        return "No registrations yet."

    with open(REGISTRATION_FILE, 'r') as f:
        rows = list(csv.reader(f))

    registrations = []
    for row in rows:
        if len(row) >= 7:
            timestamp, name, email, phone, college, branch, ref_id = row[:7]
            proof_path = None
            if len(row) > 7 and row[7].strip():
                proof_path = '/' + row[7].replace('\\', '/')
            registrations.append({
                "timestamp": timestamp,
                "name": name,
                "email": email,
                "phone": phone,
                "college": college,
                "branch": branch,
                "ref_id": ref_id,
                "proof": proof_path
            })

    count = len(registrations)
    remaining = MAX_REGISTRATIONS - count

    return render_template("admin.html", registrations=registrations, count=count, remaining=remaining)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials. Try again.")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.")
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
