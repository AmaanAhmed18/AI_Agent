import os
import time
import json
from threading import Thread
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
gmail_user = "ahmedamaan250@gmail.com"  # Your Gmail
gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")  # Update in .env

app = Flask(__name__)

# Global dictionary to store call context by CallSid
call_context = {}

def notify_user(your_email, your_name, appointment_details, call_sid):
    try:
        # Initialize appointment_status.txt with "Pending"
        with open("appointment_status.txt", "w") as f:
            f.write("Pending")
        
        status = "Pending"
        attempts = 0
        while attempts < 60 and status == "Pending":  # 60 attempts (300 seconds)
            if os.path.exists("appointment_status.txt"):
                with open("appointment_status.txt", "r") as f:
                    status = f.read().strip()
            time.sleep(5)
            attempts += 1
        print(f"Final status after {attempts} attempts: {status}")  # Debug log
        
        # Save to log
        log_data = {
            "name": your_name,
            "details": appointment_details,
            "status": status,
            "call_sid": call_sid,
            "time": time.ctime()
        }
        with open("appointments.json", "a") as f:
            json.dump(log_data, f)
            f.write("\n")
        
        # Send email
        print(f"Attempting to send email to {your_email} with status {status}")  # Debug log
        msg = MIMEText(f"Meeting for {appointment_details} on behalf of {your_name}: {status}\nCall SID: {call_sid}")
        msg["Subject"] = "Appointment Status"
        msg["From"] = gmail_user
        msg["To"] = your_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.sendmail(gmail_user, your_email, msg.as_string())
        print("Email notification sent!")
    except Exception as e:
        print(f"Error sending email: {e}")
        print(f"Meeting for {appointment_details} on behalf of {your_name}: {status}")

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    call_sid = request.form.get('CallSid', 'unknown')
    print(f"Received in /voice: CallSid={call_sid}")  # Debug log
    # Retrieve context from global dictionary
    context = call_context.get(call_sid, {'your_name': 'unknown', 'appointment_details': 'unknown'})
    your_name = context['your_name']
    appointment_details = context['appointment_details']
    print(f"Using in /voice: your_name={your_name}, appointment_details={appointment_details}")  # Debug log
    response.say(
        f"Hello, this is an automated assistant calling on behalf of {your_name}. "
        f"I would like to book an appointment for {appointment_details}. "
        "Press 1 to confirm, 2 to suggest another time, or hang up to reject.",
        voice="Polly.Aditi"
    )
    response.gather(num_digits=1, action="/handle_response", method="POST", timeout=10)
    response.hangup()
    return str(response)

@app.route("/handle_response", methods=["POST"])
def handle_response():
    try:
        digits = request.form.get("Digits", "")
        print(f"Received digits: {digits}")  # Debug log
        response = VoiceResponse()
        status = "Not Scheduled"
        
        if digits == "1":
            response.say("Thank you, the appointment is confirmed.", voice="Polly.Aditi")
            status = "Scheduled"
        elif digits == "2":
            response.say("Please call back to suggest a new time.", voice="Polly.Aditi")
            status = "Reschedule Requested"
        else:
            response.say("No valid input received. The appointment is not confirmed.", voice="Polly.Aditi")
        
        with open("appointment_status.txt", "w") as f:
            f.write(status)
        response.hangup()
        return str(response)
    except Exception as e:
        print(f"Error in handle_response: {e}")
        response = VoiceResponse()
        response.say("Sorry, there has been an application error.", voice="Polly.Aditi")
        response.hangup()
        return str(response)

def run_ai_agent():
    print("AI Agent for Appointment Booking (India)")
    your_name = input("Enter your name: ")
    recipient_phone = input("Enter the recipient's phone number (e.g., +91xxxxxxxxxx): ")
    your_email = input("Enter your email for notification (e.g., user@example.com): ")
    appointment_details = input("Enter appointment details (e.g., 'Dentist, July 21, 2 PM'): ")

    client = Client(account_sid, auth_token)
    try:
        # Initiate call and get CallSid
        call = client.calls.create(
            to=recipient_phone,
            from_=twilio_phone,
            url="https://testuser:testpass@c60baab13aa7.ngrok-free.app/voice",
            method="POST",
            record=True
        )
        # Store context in global dictionary using CallSid
        call_context[call.sid] = {
            "your_name": your_name,
            "appointment_details": appointment_details
        }
        print(f"Call initiated! Call SID: {call.sid}")
        Thread(target=notify_user, args=(your_email, your_name, appointment_details, call.sid)).start()
    except Exception as e:
        print(f"Error making call: {e}")

if __name__ == "__main__":
    run_ai_agent()
    from threading import Thread
    Thread(target=lambda: app.run(port=5001)).start()