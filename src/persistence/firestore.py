import os
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, Optional
from datetime import datetime

# Global DB client variable
db = None

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK using the service account key.
    This should be called when the application starts.
    """
    global db
    
    # Check if already initialized to prevent errors
    if firebase_admin._apps:
        db = firestore.client()
        return

    key_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_key.json")
    
    if not os.path.exists(key_path):
        print(f"⚠️ WARNING: Firebase key not found at '{key_path}'. Persistence will not work.")
        return

    try:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Firestore connected successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize Firebase: {e}")

def save_report_to_firestore(
    report_data: Dict[str, Any], 
    app_id: str = "commit-card", 
    user_id: str = "default_user"
) -> Optional[str]:
    """
    Saves the structured report to the database.
    
    Structure: /artifacts/{app_id}/users/{user_id}/reports/{report_id}
    """
    if db is None:
        initialize_firebase()
        if db is None:
            return None # Fail gracefully if DB is down

    try:
        # 1. Define the path
        # We store reports under the specific user to allow for "My History" features later
        collection_ref = db.collection('artifacts').document(app_id)\
                           .collection('users').document(user_id)\
                           .collection('reports')

        # 2. Add Timestamp
        report_data['created_at'] = datetime.utcnow()

        # 3. Add Document (Firestore auto-generates the ID)
        update_time, doc_ref = collection_ref.add(report_data)
        
        print(f"💾 Report saved with ID: {doc_ref.id}")
        return doc_ref.id

    except Exception as e:
        print(f"❌ Error saving to Firestore: {e}")
        return None

def get_report_by_id(report_id: str, app_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific report by ID.
    """
    if db is None:
        initialize_firebase()
        if db is None:
            return None # Fail gracefully if DB is down
    
    try:
        doc_ref = db.collection('artifacts').document(app_id)\
                    .collection('users').document(user_id)\
                    .collection('reports').document(report_id)
        
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error fetching report: {e}")
        return None