import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{base_dir}/data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route("/")
def no():
    return ""


def create_user_from_dict(request_data):
    return User(
        username=request_data.get("username"),
        name=request_data.get("name"),
        surname=request_data.get("surname"),
        password=request_data.get("password")
    )


def check_username_on_duplicate(username, user_id=None):
    user = User.query.filter_by(username=username).first()
    if user and user_id != str(user.id):
        abort(400, f"Username {username} is already in use")
    return True


@app.route("/users", methods=["GET", "POST"])
@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def handle_users(user_id=None):
    request_method = request.method
    if request_method == "GET":
        if user_id:  # return specific user info
            user = User.query.filter_by(id=user_id).first()
            if not user:
                abort(404, f"User with id {user_id} not found")
            return jsonify(user.to_dict())
        users = User.query.filter_by().all()
        users = [u.to_dict() for u in users]
        return jsonify(users)
    elif request_method == "POST":
        request_data = request.get_json()
        check_username_on_duplicate(request_data.get("username"))

        new_user = create_user_from_dict(request_data)
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        return jsonify({"message": "User created"})
    elif request_method == "PUT":
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, "User not found")
        request_data = request.get_json()
        username = request_data.get("username")
        if username:
            check_username_on_duplicate(username, user_id)
            user.username = username
        if "name" in request_data:
            user.name = request_data.get("name")
        if "surname" in request_data:
            user.surname = request_data.get("surname")
        if "password" in request_data:
            user.password = request_data.get("password")
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User updated"})
    elif request_method == "DELETE":
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted"})
    else:
        abort(405, "Method not allowed")


if __name__ == '__main__':
    app.run(debug=True)
