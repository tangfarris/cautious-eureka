import praw
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Posts, Base

engine = create_engine('sqlite:///sqlalchemy_example.db')

# binds the engine to the metadata of the base class so that
# the declaratives can be accessed through a dbsession instance.
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

reddit = praw.Reddit(client_id='xtsVHWcjLJDQIQ',
            client_secret='LuTE_qJuoa6Fdgy6U98KFH-yVDQ',
            user_agent='test',
            username='ucsc-slug-bot',
            password='4vjvTF9MUkuj3wg')

reddit.read_only=True
# a dbsession instance establishes all conversations with the database
# and represents a staging zone for all the objects loaded into the 
# database session object. any change made against the objects in the
# session wont be persisted into the database until you call
# session commit. if you are not happy with changes, you can rollback
# to the last commit with session.rollback()
session = DBSession()

# result = session.query(Posts).all()
# for row in result:
#     print(row.title)
#     print(row.content)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_example.db'
db = SQLAlchemy(app)

@app.route('/')
def index():        
    for submission in reddit.subreddit('ucsc').new(limit=10):
        post_title = submission.title
        post_content = submission.selftext
        new_post = Posts(title = post_title, content= post_content)
        session.add(new_post)
        session.commit()
    posts = session.query(Posts).all()
    Posts.__table__.drop()    
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)


