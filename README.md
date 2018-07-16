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
5. create database and necessary tables (diagram [here](https://app.sqldbm.com/SQLServer/Share/d3OpnSOmAtZQWMHDUGgfREGFrngIE8md_DYjF4jNYw0))
   * a)
       * crete new database (using pgAdmin for example)
       * create new user  and set a password for it
       * change database, password and user in "config.py"
   * b) 
       * open "app/models.py" and set "go" variable to 1.
         (yes, I know, it's not how you are supposed to do it, it's staying for now!)
6. run "dok_reg_app.py"
