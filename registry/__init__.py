from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
import shelve

app = Flask(__name__)
api = Api(app)

#conectando a um db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("users.db")  
    return db

@app.teardown_appcontext
def teardown_bd(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class users_list(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        users = []

        for key in keys:
            users.append(shelf[key])

        return {
            'message': 'sucess',
            'users': users
        }

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('nickname', required=True)
        parser.add_argument('game_list')
        parser.add_argument('friends_list')

        user = parser.parse_args()

        shelf = get_db()
        shelf[user['id']] = user

        return {
            'message': 'User added',
            'user': user
        }

class user(Resource):
    def get(self, id):
        shelf = get_db()

        if not (id in shelf):
            return { 'message': 'User not found' }, 404
        
        return {
            'message': 'User found',
            'user': shelf[id]
        }, 200

    def delete(seld, id):
        shelf = get_db()

        if not (id in shelf):
            return { 'message': 'User not found' }
        
        removed_user = shelf[id]
        del shelf[id]
        
        return {
            'message': 'User removed',
            'user': removed_user
        }, 

api.add_resource(users_list, '/users')
api.add_resource(user, '/users/<string:id>')