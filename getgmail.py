from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import firebase_admin
from firebase_admin import credentials, firestore

# Step 1: Load Gmail API Credentials
creds = Credentials.from_authorized_user_file('./credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])

# Step 2: Build the Gmail service
service = build('gmail', 'v1', credentials=creds)

# Step 3: Initialize Firestore with Service Account Credentials
cred = credentials.Certificate('./serviceaccountkey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Step 4: Fetch messages from the Gmail inbox
results = service.users().messages().list(userId='me', maxResults=10).execute()
messages = results.get('messages', [])

# Step 5: Loop through each message and store in Firestore
for message in messages:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    
    # Extract necessary details
    data = {
        'id': message['id'],
        'snippet': msg['snippet'],
        'internalDate': msg.get('internalDate'),
        'payload': msg.get('payload')
    }
    
    # Store each message in Firestore under a collection named 'emails'
    db.collection('emails').document(message['id']).set(data)
    print(f"Stored message {message['id']} in Firestore.")
