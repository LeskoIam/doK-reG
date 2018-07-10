from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from app import (db,
                 login)
from flask_login import UserMixin
import datetime


__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Back-reference for foreign keys
    document = db.relationship("Document", backref="user", lazy=True)
    project = db.relationship("Project", backref="user", lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Project(db.Model):

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    # Foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Back-reference for foreign keys
    document = db.relationship("Document", backref="project", lazy=True)


class Document(db.Model):

    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    revision = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)



go = 2
if go == 1:
    db.create_all()
    print("create all")
