import os.path

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


def create_user_from_json(request_data):
    return User(username=request_data.get("username"),
                name=request_data.get("name"),
                surname=request_data.get("surname"),
                password=request_data.get("password")
                )


@app.route("/users", methods=["GET", "POST"])
@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def handle_users(user_id=None):
    request_method = request.method
    if request_method == "GET":
        if user_id:
            # read specific user
            user = User.query.filter_by(id=user_id).first()
            if user:
                return jsonify(user.to_dict())
            abort(404, "User not found")
        users = User.query.filter_by().all()
        users = [u.to_dict() for u in users]

        return jsonify(users)

    if request_method == "POST":
        request_data = request.get_json()
        username = request_data.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            abort(400, "Username is already in use")
        new_user = create_user_from_json(request_data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User crated"})
    if request_method == "PUT":
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, "User Not Found")
        request_data = request.get_json()
        if "name" in request_data:
            user.name = request_data.get("name")
        if "surname" in request_data:
            user.surname = request_data.get("surname")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User Updated"})

    if request_method == "DELETE":
        if not user_id:
            abort(400, "User id is required")
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})
        # return "deleted"
    else:
        abort(405, "Method not allowed")


if __name__ == '__main__':
    app.run(debug=True)
