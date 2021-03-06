# -*- coding: utf-8 -*-
from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from __init__ import db
import mongoengine

class Douban(db.Document):
    meta = {
        'collection': 'DoubanItem',
        'ordering': ['-add_time'],
        'strict': False,
    }
    title = db.StringField()
    content = db.StringField()
    message_url = db.StringField()
    data_id = db.StringField()
    image_url = db.StringField()
    source_from = db.StringField()
    add_time = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        json_douban = {
            'title': self.title,
            'content': self.content,
            'message_url': self.message_url,
            'image_url': self.image_url,
            'source_from': self.source_from

        }
        return json_douban


class Guoke(db.Document):
    meta = {
        'collection': 'GuokeItem',
        'ordering': ['-add_time'],
        'strict': False,
    }
    title = db.StringField()
    content = db.StringField()
    message_url = db.StringField()
    data_id = db.StringField()
    image_url = db.StringField()
    source_from = db.StringField()
    add_time = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        json_douban = {
            'title': self.title,
            'content': self.content,
            'message_url': self.message_url,
            'image_url': self.image_url,
            'source_from': self.source_from

        }
        return json_douban


class Zhihu(db.Document):
    meta = {
        'collection': 'ZhihuItem',
        'ordering': ['-add_time'],
        'strict': False,
    }
    title = db.StringField()
    content = db.StringField()
    message_url = db.StringField()
    data_id = db.StringField()
    image_url = db.StringField()
    source_from = db.StringField()
    add_time = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        json_douban = {
            'title': self.title,
            'content': self.content,
            'message_url': self.message_url,
            'image_url': self.image_url,
            'source_from': self.source_from

        }
        return json_douban


class User(db.Document):
    meta = {
        'collection': 'User',
        'indexes': [
            'username',
            'email'
        ]
    }
    username = db.StringField(required=True, max_length=30, unique=True)
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField(required=True, max_length=128)
    favor = db.ListField(db.GenericReferenceField())
    add_time = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'favor': [i.to_json() for i in self.favor]
        }
        return user_data

    @property
    def password(self):
        raise AttributeError('password can not be read')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def generate_auth_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        u = User.objects(email=data['email']).first()
        if  u:
            return u
        return None


class ItemFavor(db.Document):
    """"
    被收藏的文章的表
    item:文章关联Douban Guoke Zhihu
    favor_user:收藏该文章的用户
    """
    meta = {
        'collection': 'ItemFavor',
        'indexes': [
            'item',

        ]
    }
    item = db.GenericReferenceField()
    favor_user = db.ListField(db.ReferenceField('User',reverse_delete_rule=mongoengine.PULL))



