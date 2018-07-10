import os

__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


class DokRegAppConfig(object):

    SECRET_KEY = "you-will-never-guess"

    UPLOAD_FOLDER = r"C:\Users\mpolensek\workspace\personal\doK-reG\upload_dir"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(SQLALCHEMY_DATABASE_URI)


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "zip", "rar"}