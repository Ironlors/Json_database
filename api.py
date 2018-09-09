from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
import uuid

app = Flask(__name__)
api = Api(app)

path='users_test.json'

str(uuid.uuid4())

json_data=open(path).read()
users = json.loads(json_data)
class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("email")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "email": args["email"]
        }
        users.append(user)
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("email")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["email"] = args["email"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "email": args["email"]
        }
        users.append(user)
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return "{} is deleted.".format(name), 200

api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
