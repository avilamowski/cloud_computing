from marshmallow import Schema, fields, post_dump

class Publication():
    def __init__(self, publication_id, title, content, author, date):
        self.publication_id = publication_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date

class PublicationSchema(Schema):
    publication_id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    author = fields.Str()
    date = fields.Date()
