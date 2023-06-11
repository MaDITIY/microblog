# Microblog
Microblog web application supporting public communications and private messaging between it's users.

This applicaton is developed based on Miguels Grinberg Flask [tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) as a self-educational pet-project.


## Description and features
Application allows users to write public posts and private messages and view other users posts, messages and profiles with additional information.

Here is the list of main application features implemented:
* Registration
* Main page containing the posts of all users followed by current user and text form to write own posts.
* Explore page containign ALL microblog posts from all users.
* Search form in Application header to search posts by its body.
* Messages page containing user private messages from other users.
* Users profile page. This page could be accessed through any user post and message. User profile page includes Follow/Unfollow buttons, all user public posts, "send private message" button and basic user info (user autogenerated avatar, last seen, user nickname, user description, number of followers/followed). Self profile page includes edit option and "Export your posts" option.
* Upon clicking on "Export your posts" button your public posts would be serrialized and send to the mail you provided during registration.
* Aplication allows user to reset password by email verificaton during login.
* Application partially covered by Babel for further translation.
* Automated posts translate to user native language function.
* REST API with token based authorization for most of application public entities: `app.api.v1`

## Quick start
Getting started with microblog base functionality should be fast and easy. Here are the steps:
1. Clone this repo: https://github.com/MaDITIY/TerminalCalculator.git
2. Open cloned directory.
3. Create new virtualenv:
```python3 -m venv venv```
4. Activate virtualenv:
```source ./venv/bin/activate```
5. Install packages:
```pip install -r requirements.txt```
### Launch microblog
[From root directory under activated venv. Make sure RDMS running.]
```flask run --host 0.0.0.0 --port 8080```

### Accesing microblog
Application is now accessible on <http://localhost:8080/>


### Extra features prerequesties:
* One of RDMS server running locally (`PostgreSQL`, `MySQL` or `SQLite`). Env vars:
```shell
SQLALCHEMY_DATABASE_URI="<your-connection-url>"
```
* `Elasticsearch` (`8.7.1` or later) for global search functionality. Env vars:
```shell
ELASTICSEARCH_URL="<your-connection-url>"
```
* `Reddis Queue` for profile export functionality. Env vars:
```shell
REDIS_URL="<your-connection-url>"
```
* `Microsoft Translator` created for posts automatic native language translate functionality
```shell
MS_TRANSLATOR_KEY="<microsof-translator-key>"
MS_TRANSLATOR_LOCATION="<ms-translator-location>"
```
* SMTP server configured to send password reset main and profile export mail
```shell
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=1
MAIL_USE_TLS=0
MAIL_USERNAME="<your-email-adress>"
MAIL_PASSWORD="<mail-app-password>"
```

## Next steps and action items
* Complete application API and models business logic coverage with tests. 
* Implement dialogs views (separated for each user and with both users and yours private messages)
* Complete API application representation (Posts entities. Follow/unfollow functions.)

## Environment, technologies and third-party tools used
* Python 3.10
* Flask
* SQLAlchemy
* PostgreSQL
* Babel
* Redis Queue
* Microsoft Translator
* Bootstrap