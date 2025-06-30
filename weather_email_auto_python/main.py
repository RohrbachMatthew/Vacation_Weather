import imaplib
import email
from email.header import decode_header
import mysql.connector
from datetime import datetime

# To send confirmation email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def fetch_emails(subject_filter):
    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    # Login to your account
    mail.login("datacollection350@gmail.com", "evcw bafp nbhq heam")
    # Select the mailbox you want to check
    mail.select("inbox")

    # Get today's date in the format used by the email server
    today = datetime.today().strftime('%d-%b-%Y')

    # Search for all emails with the specified subject received today
    status, messages = mail.search(None, f'(SUBJECT "{subject_filter}" SINCE {today})')
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                # Get the email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            extract_and_store_data(body)
                else:
                    body = msg.get_payload(decode=True).decode()
                    extract_and_store_data(body)
    mail.logout()

def extract_and_store_data(body):
    # Extract data from the email body
    data = {}
    lines = body.split('\n')
    for line in lines:
        if line.startswith("day:"):
            data["day"] = line.split(":")[1].strip()
        elif line.startswith("date:"):
            date_str = line.split(":")[1].strip()
            # Convert date to yyyy-mm-dd for mysql
            date_parts = date_str.split('/')
            data["date"] = f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"
        elif line.startswith("time:"):
            time_str = line.split(":")[1].strip()
            # print(f"Original time string: {time_str}")  # Debugging print
            # Ensure time is in HH:MM:SS format
            if len(time_str.split(':')) == 2:
                time_str += ":00"  # Add seconds if missing
            elif len(time_str.split(':')) == 1:
                time_str += ":00:00"  # Add minutes and seconds if missing
            data["time"] = time_str
            # print(f"Formatted time string: {data['time']}")  # Debugging print
        elif line.startswith("temperature:"):
            data["temperature"] = line.split(":")[1].strip()
        elif line.startswith("conditions:"):
            data["conditions"] = line.split(":")[1].strip()
        elif line.startswith("humidity:"):
            data["humidity"] = line.split(":")[1].strip()
        elif line.startswith("wind speed and direction:"):
            data["wind_speed_direction"] = line.split(":")[1].strip()
        elif line.startswith("uv index:"):
            data["uv_index"] = line.split(":")[1].strip()
        elif line.startswith("tide height:"):
            data["tide_height"] = line.split(":")[1].strip()
        elif line.startswith("rip tide warning:"):
            data["rip_tide_warning"] = line.split(":")[1].strip()

    # Print extracted data for debugging
    # print("Extracted data:", data)

    # Store data in MySQL
    store_data(data)

def store_data(data):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="vacation",
        password="Password123",
        database="vacation_weather",
        port=3307
    )
    cursor = conn.cursor()

    # Insert the email data
    cursor.execute("""
    INSERT INTO vacation_weather_data (day, date, time, temperature, conditions, humidity, wind_speed_direction, uv_index, tide_height, rip_tide_warning)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (data["day"], data["date"], data["time"], data["temperature"], data["conditions"], data["humidity"],
          data["wind_speed_direction"], data["uv_index"], data["tide_height"], data["rip_tide_warning"]))

    conn.commit()
    cursor.close()
    conn.close()

    # Send the confirmation after storing data
    send_confirmation_email()

def send_confirmation_email():
    # Email configuration
    sender_email = "datacollection350@gmail.com"  # Replace with your email
    receiver_email = "mattcoding91@gmail.com"  # Replace with the recipient's email
    password = "evcw bafp nbhq heam"  # Replace with your email password

    # Create the email
    subject = "Weather Data Processing Completed"
    body = "Weather data has been successfully fetched and stored in the database.\n\n\n-Weather Data Automation Script"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
# Run the fetch_emails function with the subject filter
    fetch_emails("Weather Data Update")

