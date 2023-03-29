# Blog Lite App API

Project developed by Noufal Rahman [21f1005287](mailto:21f1005287@ds.study.iitm.ac.in)

## Project Structure:
- ### /.db/
  - db.sqlite3 - Not included. database for the app
- ### /apis/
  - [auth.py](apis/auth.py) - Contains `AuthAPI` for login and profile
  - [exportcontent.py](apis/exportcontent.py) - Contains `ExportContantAPI` with `GET` method for exporting content to JSON and send it to mail
  - [feed.py](apis/feed.py) - Contains `FeedAPI` to get the feed
  - [importcontent.py](apis/importcontent.py) - Contains `ImportContentAPI` with `POST` method for importing content
  - [post.py](apis/post.py) - Contains `PostAPI` with CRUD operations on Posts
  - [search.py](apis/search.py) - Contains `SearchAPI` with `GET` method
  - [user.py](apis/user.py) - Contains `UserAPI` with CRUD operations on Users
  - [verify.py](apis/verify.py) - Contains `VerifyAPI` for OTP verification
- ### /application/
  - [auth.py](application/auth.py) - Contains function for Cookie based authentication
  - [cache.py](application/cache.py) - Init of Flask-Caching
  - [config.py](/application/config.py) - Not uploaded with the project since it has app secrets. Contains Application config
  - [db.py](/application/db.py) - Init of SQLAlchemy
  - [mail.py](/application/mail.py) - Init of Flask-Mail
  - [models.py](/application/models.py) - Contains database schemas
  - [responses.py](/application/responses.py) - Contains API responses
  - [tasks.py](/application/tasks.py) - Contains Celery async and scheduled jobs
  - [workers.py](/application/workers.py) - Init of Celery workers
- ### /templates/
  - [export.py](/templates/export.html) - Mail 
  template for export content
  - [import.py](/templates/import.html) - Mail template for import content
  - [remainder.py](/templates/remainder.html) - Mail template for remainder
  - [report-mail.py](/templates/report-mail.html) - Mail template for sending monthly report
  - [report.py](/templates/report.html) - PDF design for monthly report
  - [verify-account.py](/templates/verify-account.html) - Mail template for OTP verification
- [app.py](app.py) - Entry point of the backend

## To run this API
1. Create a Virtual Environment ```python -m venv env```
2. Activate the Virtual Environment `env\Scripts\activate`
3. Install the packages from requirements.txt file `pip install -r requirements.txt`
4. Run the API `python app.py`

_These steps are applicable only for Windows machine_