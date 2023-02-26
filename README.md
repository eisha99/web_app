
# Study Abroad Circle

## Functionality

This is a website for "Study Abroad Circle", a platform where users can get more information about studying abroad, finding opportunities and guides (resources in the form of videos, blogs etc). The website has a welcome page which allows users to log in and log out. Then they have the options of exploring different pages namely home, resources, opportunities, chats and mentorship.

## File Structure

These files are in the directory:

- `test.py` contains the unittests.
- `requirements.txt` contains the required packages for the project.
- `app.py` gets the app to run.
- .env includes env variables that need to be set

The `app` folder contains the application files:

- `__init__.py` contains the configuration and initializes the app.
- `routing.py` contains routes which serves frontend pages made up of HTML and CSS.
- `db_models.py` connects to the database and contains the SQLAlchemy tables.
- `templates/` is a folder which contains html templates to be rendered.

This is based on [this structure](http://flask.pocoo.org/docs/0.12/patterns/packages).

## Installation

Start virtual environment

    $ python -m venv venv
    $ source venv/bin/activate

Install necessary dependencies

    $ pip install -r requirements.txt

Start flask server (from the root directory)

    $ python app.py

the website should run at http://127.0.0.1:5000/

## Unit Testing

On the project root directory, run

    $ python3 -m unittest discover test


## Resources
I used these resources for this project:

- https://semantic-ui.com/ --for the design/styling

- https://flask.palletsprojects.com/en/2.0.x/tutorial/

- https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&ab_channel=TechWithTim

- Other material from CS162 pre-classes and sessions was also used and built upon to create this website as I have no prior experience in web-development.