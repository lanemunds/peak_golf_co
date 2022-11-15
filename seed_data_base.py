import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb putters")
os.system("createdb putters")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/putters.json') as f:
    putter_data = json.loads(f.read())

putters_in_db = []
for putter in putter_data:
    name, putter_path, price, company = (
        putter["name"], putter["putter_path"], putter["price"], putter["company"])
    db_putter = crud.create_putter(name, putter_path, price, company)
    putters_in_db.append(db_putter)
    print(putters_in_db)
model.db.session.add_all(putters_in_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@test.com"
    username = f"test{n}"
    password = "test"

    user = crud.create_user(username, email, password)
    model.db.session.add(user)


model.db.session.commit()
