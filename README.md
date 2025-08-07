# AI Appointment Booking Agent

## Overview

This project is an AI-powered appointment booking agent that automates scheduling via phone calls and sends email notifications. Built for a demo in India, it uses Twilio for voice calls, Flask for webhooks, and Gmail for notifications, with Ngrok enabling local testing. The agent calls a recipient, prompts for appointment confirmation (press 1, 2, or hang up), logs outcomes, and emails the status.


## Features
Automated Calls: Initiates calls with a personalized voice prompt (e.g., “on behalf of Amaan” for “Dentist, July 21, 2 PM”) using Twilio and Polly’s Aditi voice.

DTMF Handling: Processes keypad inputs (1 for confirm, 2 for reschedule, hang up for reject).

Email Notifications: Sends status updates (Scheduled, Reschedule Requested, Not Scheduled) via Gmail.

Logging: Stores call details (name, appointment, status, Call SID, timestamp) in JSON and text files.

India-Friendly: Handles TRAI/DND compliance by adding Twilio numbers to contacts and testing on stable Wi-Fi.


## Tech Stack
Python 3: Core language for scripting and automation. 

Flask: Lightweight web framework for handling Twilio webhooks (/voice, /handle_response).

Twilio: Cloud platform for making calls and processing DTMF inputs.

Ngrok: Tunnels local server (localhost:5001) to a public URL for Twilio webhooks.

Gmail (smtplib): Sends email notifications using an App Password for security.

VS Code: Development environment with Python extension for coding and debugging.

Conda: Manages Python environment and dependencies.

dotenv: Secures sensitive credentials (Twilio SID, Auth Token, Gmail App Password).


## Folder Structure
ai_agent_dtmf_email_india.py: Main script for Flask server, Twilio calls, and email notifications.

appointment_status.txt: Stores call outcome (e.g., “Scheduled”).

appointments.json: Logs call details in JSON format.

.env: Stores sensitive credentials.


## Setup and Usage
Install Python 3, VS Code, and Conda.

Set up Twilio: Sign up, buy a phone number, verify recipient number, configure webhook.

Configure Gmail: Enable 2FA, generate App Password, add to .env.

Install Ngrok: Run ngrok http 5001 --basic-auth "testuser:testpass".

Run python3 ai_agent_dtmf_email_india.py, enter details, and answer the call.

Check email and logs for results.



## Demo
Check out - 

(https://www.instagram.com/reel/DNA31KIOyyZ/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

(https://www.instagram.com/reel/DNCnLIwSUri/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)
