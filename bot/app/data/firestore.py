import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from foodflex.util.logging import logger

def init_firebase():
    global leaderboard, weekly_data, current_week_id, voting_map, db
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

    voting_map_ref = weekly_collection.document(u'voting-map')
    voting_map = voting_map_ref.get().to_dict()

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(u'Received document snapshot: {}'.format(doc.id))
            if doc.id == current_leaderboard_ref.get().id:
                leaderboard = doc.to_dict()
            elif doc.id == weekly_data_ref.get().id:
                weekly_data = doc.to_dict()
                
    leaderboard_watch = current_leaderboard_ref.on_snapshot(on_snapshot)
    weekly_data_watch = weekly_data_ref.on_snapshot(on_snapshot)
    voting_map_watch = voting_map_ref.on_snapshot(on_snapshot)

def create_new_weekly_document(week_number):
    name = u'week' + str(week_number)
    db.collection(u'weekly-data').document(name).set({})
    current_week = {
        'id': week_number
    }
    db.collection(u'weekly_data').document(u'current-week').set(data)
    logger.info(f'Week {week_number} document created')

def update_weekly_document():
    current_week_id = int(db.collection(u'weekly-data').document(u'current-week').get().to_dict()['id'])
    current_week = u'week-' + str(current_week_id)
    
    db.collection('weekly_data').document(current_week).set(weekly_data)
    logger.info(f'Week {current_week} document updated')


def build_voting_map():
    counter = 0
    logger.debug('Building voting_map map...')

    # ensure voting_map is empty
    if len(voting_map) != 0:
        logger.warn('voting_map map has not been cleared, clearing now')
        voting_map.clear()

    # assign a letter to every person who has submitted
    for user_id in weekly_data:
        if weekly_data[user_id]['submitted']:
            assigned_letter = chr(ord('A') + counter)
            counter += 1
            logger.debug(f'Assigned letter \'{assigned_letter}\' to user_id \'{user_id}\'')
            voting_map[assigned_letter] = user_id

    logger.debug(f'Map built, {len(voting_map)} letter(s)')
    db.collection('weekly-data').document('voting-map').set(voting_map)
    
def update_voting_map()
    db.collection('weekly-data').document('voting-map').set(voting_map)

