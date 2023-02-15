import os
import json
from random import choice, randint
from datetime import datetime



import model
import server


        
with server.app.app_context():
        os.system('dropdb capstone')
        os.system('createdb capstone')

        model.connect_to_db(server.app)
        model.db.create_all()
        
        for n in range(12):
                email=f'test{n}@test.com'
                password= 'test'
                new_user = model.User.create_user(email, password)
                model.db.session.add(new_user)

        with open('data/activity.json') as f:
                act_data = json.loads(f.read())
                act_in_db =  []
                for act in act_data: 
                        kind, tools, cost, user_id=(
                                act['kind'],
                                # act['tools'] is something i may need to worry about.
                                # i think i can do in in jinja 
                                # because that would 
                                # make lots of sense
                                act['tools'],
                                act['cost'],
                                act['user_id']
                        )
                        
                                # maybe use an iterable?
                        db_act = model.Activity.create_activity(kind, tools, cost, user_id)
                        act_in_db.append(db_act)
                        model.db.session.add_all(act_in_db)


        with open('data/images.json') as f:
                img_data = json.loads(f.read())
                img_in_db = []
                for img in img_data:
                        image_path, location, weather, user_id, activity_id = (
                                img['image_path'],
                                img['location'],
                                img['weather'],
                                img['user_id'],
                                img['activity_id']
                                )
                        db_img = model.Image.create_image(image_path, location, weather, user_id, activity_id)
                        img_in_db.append(db_img)
                        model.db.session.add_all(img_in_db)
        
                        model.db.session.commit()

        