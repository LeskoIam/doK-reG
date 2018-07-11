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

from app.models import (User,
                        Document,
                        Project,
                        EditDocument,
                        UserDocument)

from app import (app,
                 db)

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
    documents = UserDocument.query.filter_by(user_id=current_user.get_id())\
        .join(Document, Document.id == UserDocument.document_id).filter_by(active=True).order_by(Document.created_on.desc()).all()

    return render_template("index.html", documents=documents)


@app.route("/document/<int:document_id>")
def document_details(document_id):
    document = Document.query.filter_by(id=document_id).join(Project).first()
    last_edits = EditDocument.query.filter_by(document_id=document_id).order_by(EditDocument.created_on.desc()).all()
    return render_template("document_details.html", document=document, last_edits=last_edits)


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
            internal_filename = "{name}_{rev}{ext}".format(name=title2filename(upload_form.title.data), rev=upload_form.revision.data, ext=fext)
            doc = Document(title=upload_form.title.data,
                           original_file_name=filename,
                           internal_file_name=internal_filename,
                           file_path="dummy",
                           project_id=upload_form.project.data.id,
                           owner_id=current_user.get_id())
            db.session.add(doc)
            db.session.flush()

            user_document = UserDocument(owner=True,
                                         user_id=current_user.get_id(),
                                         document_id=doc.id)
            db.session.add(user_document)

            edit_doc = EditDocument(user_id=current_user.get_id(),
                                    document_id=doc.id,
                                    under_edit=True,
                                    from_revision=None,
                                    to_revision=1,
                                    comment=upload_form.comment.data)
            db.session.add(edit_doc)
            db.session.flush()

            # Generate path to where file will be saved on server
            file_path = os.path.join(app.config["UPLOAD_FOLDER"],
                                     "project_{}".format(upload_form.project.data.id),
                                     "dokument_{}".format(doc.id))
            os.makedirs(file_path)
            file.save(os.path.join(file_path, internal_filename))
            # Update with before generated file path
            doc_u = Document.query.filter_by(id=doc.id).first()
            doc_u.file_path = file_path
            db.session.add(doc_u)
            # Document is not under edit any more (all uploaded)
            edit_doc_u = EditDocument.query.filter_by(id=edit_doc.id).first()
            edit_doc_u.under_edit = False
            db.session.add(edit_doc_u)

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
            # db.session.flush()
            #
            # user_project = UserDocument(owner=True,
            #                             user_id=current_user.get_id(),
            #                             document_id=project.id)
            # db.session.add(user_project)
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


def title2filename(title):
    return title.replace(" ", "").lower()
