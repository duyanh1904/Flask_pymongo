from functools import partial
import pymongo
from peewee import *
from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    post_dump,
    post_load,
    ValidationError,
)
# x = mycol.insert_one(mydict)

db = MySQLDatabase('TodoList', user='root', passwd='test')

class BaseModel(Model):
    class Meta:
        database = db

class Item(BaseModel):
    item_id = AutoField()
    item_name = CharField(unique=True)
    item_describe = CharField(null=False, max_length=100)
    user_id = TextField()

    class Meta:
        table_name = 'items'

class ItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    item_describe = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    user_id = fields.Str()


class Users(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    password = CharField()
    public_id = TextField()
    admin = BooleanField()
    class Meta:
        table_name = 'Users2'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Email(error="Not a valid email address"), validate1=[validate.Length(min=6, max=36)], load_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    admin =fields.Boolean()

user_schema = UserSchema()
item_schema = ItemSchema()
db.create_tables([Users])
db.create_tables([Item])
