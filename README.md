# doK-reG
save your documents

This tries to be a clone of [docreg](https://github.com/scott-abernethy/docreg-web) with not so many bells and whistles.

## Installation
### General requirements
* Python 3.6.6
* PostgreSQL 10.0


1. clone repo
2. create virtual environment
3. install requirements.txt
4. set your download directory ("config.py" -> UPLOAD_FOLDER)
5. create necessary tables 
   * in "config.py" set your database connection string
   * open "app/models.py" and set "go" variable to 1.
     Yes, I know, it's not how you are supposed to do it, it's staying for now!
6. run "dok_reg_app.py"
