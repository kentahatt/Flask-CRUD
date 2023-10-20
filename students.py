from App import db, create_app
import os
from App.models import Student, LoginUser

# To run the application put the following command on the terminal
# cd to the root directory of project C:\Users\kenta\PycharmProjects\mbrtest2
# flask run

# This code defines a function named make_shell_context that is used to create a shell context
# for the Flask application. The shell context provides a set of variables and objects that are available
# in the interactive shell environment.

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    # Define the dictionary
    shell_context = dict(db=db, Student=Student, LoginUser=LoginUser)

    # Return the dictionary
    return shell_context
