from marshmallow import Schema, fields

class Comment :
    def __init__(self, comment_id, user, publication_id, content):
        self.comment_id = comment_id
        self.user = user
        self.publication_id = publication_id
        self.content = content
        
class CommentSchema(Schema):
    comment_id = fields.Int()
    user = fields.Str()
    publication_id = fields.Int()
    content = fields.Str()
    
        