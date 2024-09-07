from marshmallow import Schema, fields
class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
    
class UserSchema: 
    user_id = fields.Int()
    username = fields.Str()
    
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username    