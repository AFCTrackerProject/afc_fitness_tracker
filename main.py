from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


#create extension
db = SQLAlchemy()
#create app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    topicId = db.Column(db.String)

with app.app_context():
    db.create_all()

# homepage
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Add a new topic
        topic = Topic(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()

    topics = db.session.execute(db.select(Topic)).scalars()
    # for topic in topics:
    #     print(topic.title, topic.description, topic.id)
    return render_template("bootstrapindex.html", topics=topics)

# Page will display a given topic
@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # Add a new comment to the topic
        comment = Comment(
            text=request.form["text"],
            topicId=request.form["topicID"],
        )
        db.session.add(comment)
        db.session.commit()
    
    
    # Pull the topic and its comments
    return render_template("user/detail.html")




app.run(debug=True, port=5001)