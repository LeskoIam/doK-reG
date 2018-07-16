import os

__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


class DokRegAppConfig(object):

    SECRET_KEY = "you-will-never-guess"

    UPLOAD_FOLDER = r"C:\Users\mpolensek\workspace\personal\doK-reG\upload_dir"

    db_user = "dokreg"
    db_password = "dokreg"
    db_database = "dokreg"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@localhost:5432/{database}".format(user=db_user,
                                                                                                password=db_password,
                                                                                                database=db_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


ALLOWED_EXTENSIONS = {"txt", "pdf",

                      "png", "jpg", "jpeg",
                      "gif",

                      "zip", "rar",
                      "xlsx", "xls",
                      "docx", "doc"}
