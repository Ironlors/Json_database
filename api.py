from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
import uuid

app = Flask(__name__)
api = Api(app)

path='user_test.json'


json_data=open(path).read()
users = json.loads(json_data)

class User(Resource):
    def get(self, id):
        for user in users:
            if(id == user["id"]):
                return user, 200
        return "User not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("email")
        args = parser.parse_args()

        for user in users:
            if(args["email"] == user["email"]):
                return "User with email {} already exists".format(args["email"]), 400

        user = {
            "id": str(uuid.uuid4()),
            "name": args["name"],
            "age": args["age"],
            "email": args["email"]
        }
        users.append(user)
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return user, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("email")
        args = parser.parse_args()

        for user in users:
            if(args["email"] == user["email"]):
                user["name"]= args["name"]
                user["age"] = args["age"]
                user["email"] = args["email"]
                with open(path, 'w') as outfile:
                    json.dump(users, outfile)
                return user, 200

        user = {
            "id": str(uuid.uuid4()),
            "name": args["name"],
            "age": args["age"],
            "email": args["email"]
        }
        users.append(user)
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return user, 201

    def delete(self, id):
        global users
        users = [user for user in users if user["id"] != id]
        with open(path, 'w') as outfile:
            json.dump(users, outfile)
        return "{} is deleted.".format(id), 200

api.add_resource(User, "/details/<string:id>")

app.run(debug=True)
