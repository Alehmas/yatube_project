#  Yatube

##  Description
The Yatube project is a social network. It will allow users to create an account,
post entries, subscribe to their favorite authors, and tag their favorites.

##  Technologies used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) ![Django](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)


##  Functionality
The project implements:
- creation of an administrator account and site management through the administration interface
- registration, login, change your password on the site yourself
- ability to publish posts
- attach images to published posts
- subscriptions to other authors
- opportunity to comment on posts

##  Run the project locally
- Clone the repository
```
git@github.com:Oleg-2006/yatube_project.git
```
- Move to a new directory
```
cd yatube_project/
```
- Initialize the virtual environment
```
python -m venv venv
```
- Activate the virtual environment
```
source venv/Scripts/activate
```
- Update pip and set project dependencies
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- From the directory with the file `manage.py` run the migrations
```
python manage.py migrate
```
- Create a superuser
```
python manage.py createsuperuser
```
- Collect statics
```
python manage.py collectstatic
```
- To disable debug mode, change `yatube.settings.py' to
```
DEBUG = False
```
- Project launch
```
python manage.py runserver
```
- Fill out the database

##  Project Applications
All applications of the project are covered by tests.
To run the tests you need to call from the `yatube/` directory
```
python manage.py test -v {0,1,2,3}
```
*where 0 means no details, 3 means maximum information.
### posts
The application is responsible for:
- displaying the home page
- group page display
- user page display
- display the post page
- post creation
- post editing
- comment creation
- display subscriptions page
- add subscriptions
- deletion of subscriptions
- admin settings
### about
The application is responsible for:
- displaying the author page
- technology page display
### users
The app is responsible for:
- user registration
- authorization
- logging out of your account
- password reset and change
### core
The application is responsible for the context processors:
- displaying the current year on pages
- custom page 404
- custom page 403
- custom page 500