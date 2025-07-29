# 📋 EventEase — Smart Workshop & Event Registration System
⚠️ The code is currently named power-bi-bootcamp as it was built specifically for a Power BI Bootcamp event. However, the system is completely reusable and customizable for any future events, workshops, webinars, or bootcamps — just update the form content and branding.


A complete end-to-end registration platform built for organizing tech bootcamps and workshops. Designed with simplicity and functionality in mind — this system lets participants register, pay via UPI, upload payment proof, and instantly receive confirmation emails. Admins can securely track all registrations in real-time through a protected dashboard.

---

##  Features

-  **Responsive Registration Form** with live field validation
-  **QR-Based UPI Payment Integration**
-  **Auto Email Confirmations** (with custom templates)
-  **PDF Invoice Generation** per registration
-  **Payment Proof Upload & Admin Approval Workflow**
-  **Live Seat Tracking** (Max 50 registrations)
-  **Admin Login Dashboard** to view all participants & proofs
-  **Separate Host Confirmation Emails** per entry
-  **Automatic Form Closure** when capacity is reached
-  **Full client-side form validation**
-  **Proof image** viewing directly from dashboard

---

## Use Case

This project is ideal for:
- Tech/Management Bootcamps
- Workshops, Events, and Hackathons
- College Fests & Corporate Trainings

---

## What Makes It Unique?

Unlike typical Google Forms or Typeforms, this is a **completely automated backend-driven registration system**:
- Sends **real-time participant confirmations**
- Eliminates manual verification with **payment proof uploads**
- Gives hosts **centralized access** via a login-based admin dashboard
- Tracks total seats and **auto-disables** form when full
- And everything happens **without any third-party tools**

No Airtable. No Typeform. No Zapier. Just a clean, efficient Python + Flask-based system that does it all.

---

##  Built With

- Python (Flask)
- HTML, CSS, JS (Vanilla)
- Bootstrap (Frontend styling)
- SMTP Email via Gmail
- CSV & File Storage (Lightweight backend)

---


##  How to Run Locally

```bash
git clone https://github.com/your-username/powerbi-bootcamp-registration.git
cd powerbi-bootcamp-registration
pip install -r requirements.txt
python app.py
