from flask import (render_template,
                   flash,
                   request,
                   redirect,
                   url_for)

from app.forms import (RegistrationForm,
                       LoginForm,
                       UploadForm,
                       AddProjectForm)

from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS
from app.models import (User,
                        Document,
                        Project)
from app import (app,
                 db)
import os


__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    upload_form = UploadForm()
    if request.method == "POST":
        # check if upload form is valid
        if upload_form.validate_on_submit():
            file = upload_form.file.data
            filename = secure_filename(file.filename)
            doc = Document(title=upload_form.title.data,
                           file_name=filename,
                           file_path=app.config["UPLOAD_FOLDER"],
                           revision=upload_form.revision.data,
                           project_id=upload_form.project.data.id,
                           owner_id=current_user.get_id())
            db.session.add(doc)
            db.session.commit()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("upload_file"))
    return render_template("upload.html", form=upload_form)


@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    add_project_form = AddProjectForm()
    if request.method == "POST":
        if add_project_form.validate_on_submit():
            name = add_project_form.name.data
            project = Project(name=name, owner_id=current_user.get_id())
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("add_project"))
    return render_template("add_project.html", form=add_project_form)

# @app.route("/download")
# # @login_required
# def download():
#     return send_file(r"C:\Users\mpolensek\workspace\personal\dokreg_tryes\static\img\404_page.jpg", as_attachment=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged-in")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        flash("Already logged-in")
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.errorhandler(404)
def not_found(error):
    app.logger.debug(error)
    return render_template("error_404.html"), 404


@app.errorhandler(401)
def unauthorized(error):
    app.logger.debug(error)
    return render_template("error_401.html"), 401
