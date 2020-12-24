import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from dbMongo import *
from flask import Flask
from flask_pymongo import PyMongo
import json


app = Flask(__name__)

app.config['SECRET_KEY']='LongAndRandomSecretKey'
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
todos = db.todo

# new_posts = [{"item_name": "Mike", "item_describe": "Another!"}]
# result = mongo.db.items.insert_many(new_posts)



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # current_user = Users.select().where(Users.public_id==data['public_id']).get()
        except:
            return jsonify({'message': 'token is invalid'})
        # return f(current_user, *args, **kwargs)
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    # user = Users.get(Users.name == auth.username)
    #
    # if check_password_hash(user.password, auth.password):
    #     token = jwt.encode(
    #         {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
    #         app.config['SECRET_KEY'])
    #     return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/')
def home():
    page = request.args.get('page', 1 ,int)
    posts = [1,2,3,4,5,6,7,8]
    sorts_list = ['desc', 'asc']
    # item_list = Item.select().order_by(Item.item_id.desc()).paginate(page=page, paginate_by = 4) #peewee
    item_list = todos.find().sort("_id",pymongo.DESCENDING)
    return render_template("base.html", item_list = item_list, posts = posts, sorts_list = sorts_list)

# @app.route('/asc')
# def home1():
#     page = request.args.get('page', 1 ,int)
#     posts = [1, 2, 3, 4, 5, 6, 7 ,8]
#     sorts_list = ['desc', 'asc']
#     item_list = Item.select().order_by(Item.item_id.asc()).paginate(page=page, paginate_by = 4)
#     return render_template("base.html", item_list = item_list, posts = posts, sorts_list = sorts_list)

# @app.route("/add", methods=["POST"])
# @token_required
# def add(current_user):
    # item =Item.create(
    #     item_name = request.form['itemName'],
    #     item_describe =request.form['itemDescribe'])
    # return redirect(url_for("home"))

    # if current_user.id == Users.public_id:
    #     try:  # Use get to see if user already exists
    #         Item.get(Item.item_name == request.form["itemName"])
    #     except Item.DoesNotExist:
    #         item = Item.create(
    #             item_name=request.form["itemName"], item_describe=request.form["itemDescribe"]
    #         )
    #         message = "Successfully created item: {}".format(item.item_name)
    #     else:
    #         return {"errors": "That item address is already in the database"}, 400
    #     return message
    # else:
    #     return {"error": "That user not current user"}, 400

@app.route("/add", methods = ['POST'])
def add():
    item_name = request.values.get("itemName")
    item_desc = request.values.get("itemDescribe")
    todos.insert({"item_name": item_name, "item_desc": item_desc})
    return redirect('/')

@app.route("/delete")
def delete():
    key = request.values.get("_id")
    todos.remove({"_id": ObjectId(key)})
    return redirect(url_for("home"))

@app.route("/update")
def updateRoute():
    # if not item_id or item_id != 0:
    #     entry = todos.db.users.find({"item_id": item_id})
    #     if entry:
    #         return render_template('update.html', item_id=item_id)
    # return redirect(url_for("home"))
    id = request.values.get("_id")
    item_list = todos.find({"_id": ObjectId(id)})
    return render_template('update.html', item_list=item_list)

@app.route("/action_update",methods=['post'])
# def update(item_id):
    # with db.atomic():
    #     itemUpdate = (Item
    #            .update(item_name = request.form['itemName'], item_describe = request.form['itemDescribe'])
    #            .where(Item.item_id == item_id)
    #            .execute())
    # return redirect(url_for("home"))
def update():
    item_name = request.values.get("item_name")
    item_desc = request.values.get("item_desc")
    id = request.values.get("_id")
    todos.update({"_id": ObjectId(id)}, {'$set': {"item_name": item_name, "item_desc": item_desc}})
    return redirect(url_for("home"))


@app.route("/api/v1.0/tasks", methods = ['GET'])
def tasks():
    # page = request.args.get('page', 1, int)
    # items = [item for item in Item.select().dicts().paginate(page=page, paginate_by = 4)]

    item_list = todos.db.items.find()

    # items = User1.objects().to_json()
    return jsonify(item_list)

# @app.route("/api/v1.0/tasks/<int:item_id>")
# def update_tasks_get(item_id):
#     if not item_id or item_id != 0:
#         entry = Items.select(Items.item_id)
#         if entry:
#             return render_template('update_task.html', item_id = item_id)

# @app.route("/api/v1.0/tasks/<int:item_id>", methods = ['PUT'])
# def update_tasks(item_id):
#     items = [item for item in Items.select().dicts() if item['item_id'] == item_id]
#     if len(items) == 0:
#         abort(404)
#     items.item_name = request.args.get('itemName')
#     items.item_describe = request.args.get('itemDescribe')

# @app.route('/api/v1.0/tasks/delete/<int:item_id>', methods=['Delete'])
# def delete_task(item_id):
#     item = [item for item in Item.select().dicts() if item['item_id'] == item_id]
#     if len(item) == 0:
#         abort(404)
#     tasks.remove(item[item_id])
#     return jsonify({'result': True})


# @app.route('/register', methods=['POST'])
# def signup_user():
#     data_input = request.form.to_dict()
#     try:
#         data = user_schema.load(data_input)
#     except ValidationError as err:
#         return {"errors": err.messages}, 422
#     try:  # Use get to see if user already exists
#         Users.get(Users.name == data["name"])
#     except Users.DoesNotExist:
#         item = Users.create(
#             name=data["name"],public_id=str(uuid.uuid4()),
#             password=generate_password_hash(data['password'], method='sha256'), admin = False
#         )
#         message = "Successfully created user: {}".format(item.name)
#     else:
#         return {"errors": "That username is already in the database"}, 400
#     return message

if __name__ == "__main__":
    app.run(debug=True)

