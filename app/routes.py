from flask import (render_template,
                   flash,
                   request,
                   redirect,
                   url_for,
                   send_file)

from app.forms import (RegistrationForm,
                       LoginForm,
                       UploadForm,
                       AddProjectForm,
                       NewRevUploadForm)

from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from app.models import (User,
                        Document,
                        Project,
                        Revision,
                        UserDocument)

from app import (app,
                 db)

from app.common.databse_helpers import execute_query
from werkzeug.utils import secure_filename
import os

__author__ = 'mpolensek'


# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


@app.route("/")
@app.route("/index", methods=["GET"])
def index():
    documents = UserDocument.query.filter_by(user_id=current_user.get_id()) \
        .join(Document, Document.id == UserDocument.document_id) \
        .filter_by(active=True, under_edit=False).order_by(Document.created_on.desc()).all()
    return render_template("index.html", documents=documents)


@app.route("/document/<int:document_id>", methods=["GET", "POST"])
def document_details(document_id):
    upload_form = NewRevUploadForm()
    document = Document.query.filter_by(id=document_id).join(Project).first()
    last_edits = Revision.query.filter_by(document_id=document_id).order_by(Revision.created_on.desc()).all()
    if request.method == "POST":
        if upload_form.validate_on_submit():
            file = upload_form.file.data
            filename = secure_filename(file.filename)

            document = Document.query.filter_by(id=document_id).first()
            fd = Revision.query.filter_by(document_id=document_id, revision=document.active_revision).first()
            # Calculate new revision and generate new file name
            new_rev = document.active_revision + 1
            n = fd.internal_file_name.rsplit("_", 1)
            fname, fext = os.path.splitext(filename)
            new_file_name = "{name}_{rev}{ext}".format(name=n[0], rev=new_rev, ext=fext)

            file_info = Revision(original_file_name=filename,
                                 internal_file_name=new_file_name,
                                 file_path=fd.file_path,
                                 revision=new_rev,
                                 comment=upload_form.comment.data,
                                 document_id=document_id,
                                 user_id=current_user.get_id())
            db.session.add(file_info)
            # Update document active revision
            document.active_revision = new_rev
            db.session.add(document)

            file.save(os.path.join(fd.file_path, new_file_name))
            db.session.commit()
            return redirect(url_for("document_details", document_id=document_id))
    return render_template("document_details.html", document=document, last_edits=last_edits, upload_form=upload_form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def new_file_upload():
    upload_form = UploadForm()
    if request.method == "POST":
        # check if upload form is valid
        if upload_form.validate_on_submit():
            file = upload_form.file.data
            filename = secure_filename(file.filename)
            fname, fext = os.path.splitext(filename)
            internal_filename = "{name}_{rev}{ext}".format(name=title2filename(upload_form.title.data),
                                                           rev=upload_form.revision.data,
                                                           ext=fext)
            doc = Document(title=upload_form.title.data,
                           active=True,
                           under_edit=True,
                           active_revision=upload_form.revision.data,
                           project_id=upload_form.project.data.id,
                           owner_id=current_user.get_id())
            db.session.add(doc)
            db.session.flush()

            user_document = UserDocument(user_id=current_user.get_id(),
                                         document_id=doc.id)
            db.session.add(user_document)

            # Generate path to where file will be saved on server
            file_path = os.path.join(app.config["UPLOAD_FOLDER"],
                                     "project_{}".format(upload_form.project.data.id),
                                     "dokument_{}".format(doc.id))

            file_info = Revision(original_file_name=filename,
                                 internal_file_name=internal_filename,
                                 file_path=file_path,
                                 revision=upload_form.revision.data,
                                 comment=upload_form.comment.data,
                                 document_id=doc.id,
                                 user_id=current_user.get_id())
            db.session.add(file_info)

            # Document is not under edit any more (all uploaded)
            edit_doc_u = Document.query.filter_by(id=doc.id).first()
            edit_doc_u.under_edit = False
            db.session.add(edit_doc_u)

            os.makedirs(file_path)
            file.save(os.path.join(file_path, internal_filename))

            db.session.commit()
            return redirect(url_for("index"))
    return render_template("upload.html", form=upload_form)


@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    add_project_form = AddProjectForm()
    if request.method == "POST":
        if add_project_form.validate_on_submit():
            name = add_project_form.name.data
            project = Project(name=name, owner_id=current_user.get_id(), active=True)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("add_project"))
        return render_template("add_project.html", form=add_project_form)
    elif request.method == "GET":
        projects = Project.query.filter().order_by(Project.name.desc()).all()
        return render_template("add_project.html", form=add_project_form, projects=projects)


@app.route("/download/<int:document_id>/<int:revision>", methods=["GET"])
@login_required
def download(document_id, revision):
    fd = Revision.query.filter(Revision.document_id == document_id, Revision.revision == revision).first()
    return send_file(os.path.join(fd.file_path, fd.internal_file_name), as_attachment=True)


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


def title2filename(title):
    return title.replace(" ", "").lower()
