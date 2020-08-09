import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from foodflex.util.logging import logger

def init_firebase():
    global leaderboard, weekly_data
    cred = credentials.Certificate('creds.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    leaderboard_collection = db.collection(u'leaderboard')
    current_leaderboard_id = leaderboard_collection.document(u'current-leaderboard').get().to_dict()['id']
    current_leaderboard_ref = leaderboard_collection.document(u'' + current_leaderboard_id)
    leaderboard = current_leaderboard_ref.get().to_dict()

    weekly_collection = db.collection(u'weekly-data')
    current_week_id = int(weekly_collection.document(u'current-week').get().to_dict()['id'])
    weekly_data_ref = weekly_collection.document(u'week-{}'.format(current_week_id))
    weekly_data = weekly_data_ref.get().to_dict()

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(u'Received document snapshot: {}'.format(doc.id))
            if doc.id == current_leaderboard_ref.get().id:
                leaderboard = doc.to_dict()
            elif doc.id == weekly_data_ref.get().id:
                weekly_data = doc.to_dict()
                
    leaderboard_watch = current_leaderboard_ref.on_snapshot(on_snapshot)
    weekly_data_watch = weekly_data_ref.on_snapshot(on_snapshot)
            