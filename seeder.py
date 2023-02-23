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
                username = f'user{n}'
                password= 'test'
                new_user = model.User.create_user(email, username, password)
                model.db.session.add(new_user)

        with open('data/activity.json') as f:
                act_data = json.loads(f.read())
                act_in_db =  []
                for act in act_data: 
                        kind, cost, user_id=(
                                act['kind'],
                                act['cost'],
                                act['user_id'],
                        )
                                # maybe use an iterable?
                        db_act = model.Activity.create_activity(kind, cost, user_id)
                        act_in_db.append(db_act)
                        model.db.session.add_all(act_in_db)

        with open('data/tools.json') as f:
                tool_data = json.loads(f.read())
                tool_in_db = []
                for t in tool_data:
                        name, activity_id=(
                                t['name'],
                                t['activity_id']
                        )
                        db_tool = model.Tool.create_tool(name, activity_id)
                        tool_in_db.append(db_tool)
                        model.db.session.add_all(tool_in_db)

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

                with open('data/comments.json') as f:
                        comment_data = json.loads(f.read())
                        comment_in_db = []
                        for t in comment_data:
                                comment, user_id, image_id=(
                                        t['comment'],
                                        t['user_id'],
                                        t['image_id'],
                                )
                                db_comment = model.Comment.create_comment(comment, user_id, image_id)
                                comment_in_db.append(db_comment)
                                model.db.session.add_all(comment_in_db)
                        
                                model.db.session.commit()