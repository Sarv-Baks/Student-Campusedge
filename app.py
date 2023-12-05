from flask import Flask, render_template, request, redirect, flash , session , url_for ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import secrets
import datetime
import os
from flask import jsonify
from flask_session import Session
import sqlite3
import time

# from models import Course  


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crsss.db'  # SQLite database file path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mandedevesh@gmail.com'
app.config['MAIL_PASSWORD'] = 'jqelbqkpgdjvhyap'
app.config['SESSION_TYPE'] = 'filesystem' 

Session(app)


db = SQLAlchemy(app)
mail = Mail(app)

class signup(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mob = db.Column(db.String(200), nullable=False)
    reset_password_token = db.Column(db.String(255))
    reset_token_expiration = db.Column(db.DateTime)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.firstname} - {self.email}"



class course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    section = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name}, section={self.section})"


class CompletedCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"CompletedCourses(id={self.id}, user_id={self.user_id}, course_id={self.course_id}, name={self.name})"
    


@app.route('/track_course', methods=['POST'])

def track_course():
    data = request.get_json()
    course_name = data.get('courseName')

    if course_name:
        # Create a new Course object and add it to the database
        new_course = CompletedCourses(name=course_name)

        try:
            # Add the new course to the database
            db.session.add(new_course)
            db.session.commit()
            return jsonify(success=True, message="Course added successfully.")
        except Exception as e:
            # Handle database errors (e.g., integrity violation) here
            print(str(e))
            db.session.rollback()
            return jsonify(success=False, error="Failed to add course to the database.")
        finally:
            # Close the database session
            db.session.close()
    else:
        return jsonify(success=False, error="Invalid data provided.")


def add_course():
    data = request.get_json()
    course_name = data.get('courseName')
    section = data.get('section')

    if course_name and section:
        # Create a new Course object and add it to the database
        new_course = course(name=course_name, section=section)

        try:
            # Add the new course to the database
            db.session.add(new_course)
            db.session.commit()
            return jsonify(success=True, message="Course added successfully.")
        except Exception as e:
            # Handle database errors (e.g., integrity violation) here
            print(str(e))
            db.session.rollback()
            return jsonify(success=False, error="Failed to add course to the database.")
        finally:
            # Close the database session
            db.session.close()
    else:
        return jsonify(success=False, error="Invalid data provided.")



@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    try:
        # Get course_id from the request payload
        data = request.get_json()
        course_id = data.get('course_id')

        # Perform database operation to mark the course as completed
        completed_course = CompletedCourses(user_id=1, course_id=course_id, course_name=course.query.filter_by(id=course_id).first().name)
        db.session.add(completed_course)
        db.session.commit()

        # Return success response
        response = {'success': True, 'message': 'Course marked as completed!'}
    except Exception as e:
        # Log the error for server-side debugging
        print(f"Error: {e}")

        # Return error response with detailed error message
        response = {'success': False, 'error': str(e)}

    return jsonify(response)

@app.route('/get_completed_courses', methods=['GET'])
def get_completed_courses():
    try:
        user_id = 1  # You need to get the user ID from the session
        completed_courses = CompletedCourses.query.filter_by(user_id=user_id).all()
        course_names = [course.course_name for course in completed_courses]
        response = {'success': True, 'completed_courses': course_names}
    except Exception as e:
        print(e)
        response = {'success': False}
    
    return jsonify(response)



if not os.path.exists("crsss.db"):
    with app.app_context():
        db.create_all()



# # Sample data for courses (replace this with actual database queries)
# courses = [
#     {"name": "English Course 1", "section": "english"},
#     {"name": "Coding Course 1", "section": "coding"}
# ]

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/signup')
def SignUp():
    return render_template('signup.html')

@app.route('/registration', methods=['POST'])
def Registration():
    if request.method == 'POST':

        email = request.form.get('email')

        existing_user = signup.query.filter_by(email=email).first()

        if existing_user:
            return """
                <script>alert("Your Account already exists, please login :)"); 
                window.location.href = '/';</script>
                """

        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        mob = request.form.get('mob')
        password = request.form.get('password')
        user = signup(firstname=firstname, lastname=lastname, mob=mob, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template('index.html')




# @app.route('/authentication', methods=["POST"])
# def authentication():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = signup.query.filter_by(email=email).first()
#         admin = signup.query.filter_by(email=email).first()  # Assuming admin_table is the table for admin users

#         if user and user.password == password:
#             if user.email == 'admin@gmail.com':
#                 # For admin, set a flag in session

#                 session['admin'] = True


#                 session['admin_firstname'] = user.firstname
#                 return render_template('adminm.html', username=f"{user.firstname}")

#             else:
#                 # For regular users, store the user's first name and last name in session
#                 session['user_firstname'] = user.firstname
#                 session['user_lastname'] = user.lastname

#             # Pass both first name and last name to the template
#             return render_template('sample.html', username=f"{user.firstname} {user.lastname}")
#         else:
#             return """
#                 <script>alert("Your Login Credentials are Incorrect. Please login again :)"); 
#                 window.location.href = '/';</script>
#                 """

@app.route('/authentication', methods=["POST"])
def authentication():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = signup.query.filter_by(email=email).first()
        admin = signup.query.filter_by(email=email).first()  # Assuming admin_table is the table for admin users

        if user and user.password == password:
            if user.email == 'admin@gmail.com':
                # For admin, set a flag in session
                session['admin'] = True
                # Fetch admin's first name and last name from the database
                session['user_firstname'] = admin.firstname
                # session['user_lastname'] = admin.lastname
                return render_template('adminm.html', username=f"{user.firstname}")

            else:
                # For regular users, store the user's name in session
                session['user_firstname'] = user.firstname
                session['user_lastname'] = user.lastname
            return render_template('sample.html', username=f"{session['user_firstname']} {session['user_lastname']}")
  
            # return render_template('sample.html', username=session['user_firstname'], )  # Pass username to the template
        else:
            return """
                <script>alert("Your Login Credentials are Incorrect. Please login again :)"); 
                window.location.href = '/';</script>
                """

@app.route('/logout')
def logout():
    
    session.pop('user', None)  # Remove 'user' key from session
    return render_template('index.html')



@app.route('/fpemail', methods=['GET', 'POST'])
def fpemail():
    if request.method == 'POST':
        email = request.form['email']
        user = signup.query.filter_by(email=email).first()
        if user:
            token = secrets.token_hex(16)
            user.reset_password_token = token
            user.reset_token_expiration = datetime.datetime.now() + datetime.timedelta(minutes=130)
            db.session.commit()

            msg = Message('Password Reset Token', sender='mandedevesh@gmail.com', recipients=[user.email])
            msg.body = f'Your reset token is - {token}'
            mail.send(msg)

            # Return a JSON response indicating success
            return """
                <script>alert("Password reset token sent to your email :)  "); 
                window.location.href = '/fpconfirm';</script>
            """

        # Return a JSON response indicating failure
        return """
                <script>alert("Invalid email address. Try again :)  "); 
                window.location.href = '/fpemail';</script>
            """ 


    # Handle GET requests (render the form)
    return render_template('fpemail.html')



@app.route('/fpconfirm',methods=['GET', 'POST'])
def fpconfirm():
    if request.method == 'POST':
        reset_token = request.form.get('reset_token')
        user = signup.query.filter_by(reset_password_token=reset_token).first()
        if user and user.reset_token_expiration > datetime.datetime.now():
            new_password = request.form['upassword']  # Get the new password from the form data
            user.password = new_password
            user.reset_password_token = None
            user.reset_token_expiration = None
            db.session.commit()

            return """
                <script>alert("Password reset successfully! You can login again :)  "); 
                window.location.href = '/';</script>
            """
        else:
            """
                <script>alert("Invalid or expired token. Please try again :)  "); 
                window.location.href = '/fpconfirm';</script>
            """

    return render_template('fpconfirm.html')


@app.route('/admin2')
def admin_page():
    return render_template('admin2.html')

@app.route('/profile')
def profile():
    # Query the database to get courses and signups data
    courses = course.query.all()
    signups = signup.query.all()
    return render_template('student_track.html', courses=courses, signups=signups)




@app.route('/profile2')
def profile2():
    # Query the database to get courses and signups data
    courses = course.query.all()
    signups = signup.query.all()
    mobs = signup.query.all()
    return render_template('student_contact.html', courses=courses, signups=signups , mobs=mobs)


# @app.route('/profile4')
# def profile4():
#     # Query the database to get courses and signups data

#     mobs = signup.query.all()
#     return render_template('student_contact.html',  mobs=mobs)



@app.route('/add_course', methods=['POST'])

def add_course():
    data = request.get_json()
    course_name = data.get('courseName')
    section = data.get('section')

    if course_name and section:
        # Create a new Course object and add it to the database
        new_course = course(name=course_name, section=section)

        try:
            # Add the new course to the database
            db.session.add(new_course)
            db.session.commit()
            return jsonify(success=True, message="Course added successfully.")
        except Exception as e:
            # Handle database errors (e.g., integrity violation) here
            print(str(e))
            db.session.rollback()
            return jsonify(success=False, error="Failed to add course to the database.")
        finally:
            # Close the database session
            db.session.close()
    else:
        return jsonify(success=False, error="Invalid data provided.")




# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_text = db.Column(db.String(500), nullable=False)
#     option_1 = db.Column(db.String(200), nullable=False)
#     option_2 = db.Column(db.String(200), nullable=False)
#     option_3 = db.Column(db.String(200), nullable=False)
#     option_4 = db.Column(db.String(200), nullable=False)
#     correct_answer = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f'<Question {self.id}>'

# @app.route('/admin/quiz', methods=['GET', 'POST'])
# def admin_quiz():
#     if request.method == 'POST':
#         questions_data = request.form.to_dict(flat=False)
#         num_questions = len(questions_data['question_text'])

#         for i in range(num_questions):
#             question = Question(
#                 question_text=questions_data['question_text'][i],
#                 option_1=questions_data['option_1'][i],
#                 option_2=questions_data['option_2'][i],
#                 option_3=questions_data['option_3'][i],
#                 option_4=questions_data['option_4'][i],
#                 correct_answer=questions_data['correct_answer'][i]
#             )
#             db.session.add(question)

#         db.session.commit()
#         return "Quiz questions added to the database!"

#     return render_template('quizs.html')


login_time = datetime.datetime.now()




# @app.route('/tracktime')
# def tracktime():
#     return render_template('tracktime.html')


@app.route('/sample')
def sample():
    return render_template('sample.html')


@app.route('/findcourse')
def findcourse():
    return render_template('findcourse.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/arithematic')
def arithematic():
    return render_template('arithematic.html')


@app.route('/aptitude')
def aptitude():
    return render_template('aptitude.html')



@app.route('/programming')
def programming():
    return render_template('programming.html')




@app.route('/dsa')
def dsa():
    return render_template('dsa.html')




@app.route('/interview')
def interview():
    return render_template('interview.html')







@app.route('/database')
def edatabase():
    return render_template('database.html')




@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quizs')
def quizs():
    return render_template('quizs.html')

@app.route('/array')
def array():
    return render_template('array.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/string')
def string():
    return render_template('string.html')


@app.route('/dp')
def dp():
    return render_template('dp.html')


@app.route('/adminprofile')
def adminprofile():
    return render_template('adminprofile.html')

@app.route('/adminm')
def adminm():
    return render_template('adminm.html')



@app.route('/aboutt')
def aboutt():
    return render_template('aboutt.html')




@app.route('/student_track')
def student_track():
    return render_template('student_track.html')




@app.route('/studentprofile')
def studentprofile():
    return render_template('studentprofile.html')




@app.route('/student1')
def student1():
    return render_template('student1.html')


@app.route('/aarraayy')
def aarraayy():
    return render_template('aarraayy.html')



@app.route('/backtracking')
def backtracking():
    return render_template('backtracking.html')


@app.route('/searching')
def searching():
    return render_template('searching.html')




# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True, port=8000)


