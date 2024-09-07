from flask import Flask, request, jsonify
from models.publication import Publication, PublicationSchema
from models.comment import Comment, CommentSchema
from models.user import User, UserSchema
import datetime as dt

app = Flask(__name__)

publications = [
    Publication(1, "First Publication", "Content of my first publication", "Author1", dt.datetime.now()),
    Publication(2, "Second Publication", "Content of my second publication", "Author2", dt.datetime.now()),
    Publication(3, "Third Publication", "Content of my third publication", "Author3", dt.datetime.now())
]

@app.route("/")
def index():
    return "Hello, World!?"
  
@app.route("/publications")
def get_publications():
    publication_schema = PublicationSchema(many=True)
    publications_json = publication_schema.dump(publications)
    return jsonify(publications_json)
  
  
if __name__ == "__main__":
    app.run(debug=True)