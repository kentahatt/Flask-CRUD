from . import db
from .models import Student
from flask import abort, request, render_template, url_for, redirect, Blueprint
from flask_login import login_required, current_user

# The create_app() function instantiates the app instance and then uses the app.route() to register the endpoints
main = Blueprint('main', __name__, template_folder='templates')


# create_student() is a function that is triggered when a POST request is made to the '/student/list' endpoint.
# It creates a new student object using the data received from the request form, adds it to the database session,
# and commits the changes. Finally, it redirects the user to the 'get_students' endpoint defined in @main.route.
@main.route('/student/list', methods=["POST"])
def create_student():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    student = Student(name, email, phone)

    db.session.add(student)
    db.session.commit()
    return redirect(url_for('main.get_students'))


# Read from database (Points to index.html)
@main.route("/student/list", methods=["GET"])
def get_students():
    students = Student.query.all()
    return render_template("main/index.html", students=students)


@main.route("/studentinfo/<stu_id>", methods=["GET"])
def get_individual(stu_id):
    student = Student.query.get(stu_id)
    if student is None:
        abort(404)
    return render_template("main/studentinfo.html", student=student)


# update_student() is a function that handles both GET and POST requests.
# It updates the attributes of a student object in the database based on the form data submitted in the POST request.
@main.route('/update', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        try:
            student = Student.query.get(request.form.get('id'))
            if student is None:
                return "Student not found", 404

            student.name = request.form.get('name')
            student.email = request.form.get('email')
            student.phone = request.form.get('phone')

            # to update/ modify attributes on model objects
            student.verified = True
            db.session.commit()

            return redirect(url_for('main.get_students'))
        except Exception as e:
            # handle the exception here
            return "An error occurred: " + str(e)


# Delete Student
@main.route("/delete", methods=['GET', 'POST'])
def delete_student():

    if request.method == 'POST':
        student = Student.query.get(request.form['id'])

        if student is None:
            abort(404)

        # delete student
        db.session.delete(student)
        db.session.commit()

    return redirect(url_for('main.get_students'))


@main.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', name=current_user.username)
