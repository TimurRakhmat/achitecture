from pymongo import TEXT, mongo_client
import random
import uuid
from datetime import datetime


def db_init():
    client = mongo_client.MongoClient(host='mongo', port=27017, uuidRepresentation='standard')
    lk = client['conf']['lectures']
    lk.create_index('name', unique = True)
    lk.create_index([('speaker', TEXT)])

    res = lk.find()
    if len(list(res)) == 0:
        for _ in range(20):
            lk_id = str(uuid.uuid4())
            print(lk_id)
            index = random.randint(1, 5)
            lk.insert_one(
                {
                    'name': lk_id,
                    'text': f'text in {lk_id} №{index}',
                    'speaker': 'admin',
                    'sending_time': datetime.now(),
                }
            )