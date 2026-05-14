from app import app
from flask import render_template, request, redirect, url_for, flash, session
from database import *
from datetime import datetime

@app.route("/")
def home():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizs = Quiz.query.all()
    quizzes = []
    for quiz in quizs:
        if quiz.date_of_quiz >= datetime.now().date():
            quizzes.append(quiz)

    return render_template("home.html", subjects = subjects, chapters = chapters, quizzes = quizzes)

@app.route("/add_subject" , methods = ["GET","POST"])
def add_subject():
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            return render_template("add_subject.html")
        
        if request.method == "POST":
            name = request.form.get("name",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("add_subject"))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("add_subject"))
            
            subject = Subject.query.filter_by(name = name).first()
            if subject:
                flash("Subject already exists")
                return redirect(url_for("add_subject"))
            
            new_subject = Subject(
                name = name,
                description = description
            )
            db.session.add(new_subject)
            db.session.commit()

            flash("Subject added successfully")

        return redirect(url_for("home"))

    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/add_chapter/<int:subject_id>" , methods = ["GET","POST"])
def add_chapter(subject_id):
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            # subjects = Subject.query.all()
            return render_template("add_chapter.html",subject_id = subject_id)
        
        if request.method == "POST":
            name = request.form.get("name",None)
            # subject_id = request.form.get("subject_id",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            # if not subject_id:
            #     flash("Subject is required")
            #     return redirect(url_for("add_chapter"))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            subject = Subject.query.filter_by(id = subject_id).first()
            if not subject:
                flash("Subject not found")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            chapter = Chapter.query.filter_by(name = name).first()
            if chapter:
                flash("Chapter already exists")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            new_chapter = Chapter(
                name = name,
                subject_id = subject_id,
                description = description
            )

            db.session.add(new_chapter)
            db.session.commit()

            flash("Chapter added successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    

@app.route("/add_quiz" , methods = ["GET","POST"])
def add_quiz():
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            chapters = Chapter.query.all()
            return render_template("add_quiz.html",chapters = chapters)
        
        if request.method == "POST":
            chapters = Chapter.query.all()
            chapter_id = request.form.get("chapter_id",None)
            name = request.form.get("name",None)
            date_of_quiz = request.form.get("date",None)
            duration = request.form.get("duration",None)
            remarks = request.form.get("remarks",None)

            if not chapter_id:
                flash("Chapter is required")
                return redirect(url_for("add_quiz",chapters = chapters))
            
            if not name:
                flash("Name is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            if not date_of_quiz:
                flash("Date is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            if not duration:
                flash("Duration is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            chapter = Chapter.query.filter_by(id = chapter_id).first()
            if not chapter:
                flash("Chapter not found")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()
            duration = int(duration)

            new_quiz = Quiz(
                chapter_id = chapter_id,
                name = name,
                date_of_quiz = date_of_quiz,
                duration = duration,
                remarks = remarks
            )

            db.session.add(new_quiz)
            db.session.commit()

            flash("Quiz added successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/quiz_management")
def quiz_management():
    if session.get('user_role', None) == 'admin':
        quizzes = Quiz.query.all()
        questions = Question.query.all()
        return render_template("quiz_management.html", quizzes = quizzes, questions = questions)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))

@app.route("/add_question/<int:quiz_id>" , methods = ["GET","POST"])
def add_question(quiz_id):
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            return render_template("add_question.html",quiz_id = quiz_id)
        
        if request.method == "POST":
            quiz = Quiz.query.filter_by(id = quiz_id).first()
            if not quiz:
                flash("Quiz not found")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            question_title = request.form.get("question_title",None)
            question_statement = request.form.get("question_statement",None)
            option1 = request.form.get("option1",None)
            option2 = request.form.get("option2",None)
            option3 = request.form.get("option3",None)
            option4 = request.form.get("option4",None)
            correct_option = request.form.get("correct_option",None)

            if not question_title:
                flash("Question title is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not question_statement:
                flash("Question statement is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option1:
                flash("Option1 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option2:
                flash("Option2 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option3:
                flash("Option3 is required")
                return redirect(url_for("add_question", quiz_id = quiz_id))
            
            if not option4:
                flash("Option4 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not correct_option:
                flash("Correct option is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if option1 == option2 or option1 == option3 or option1 == option4 or option2 == option3 or option2 == option4 or option3 == option4:
                flash("Options should be unique")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not (correct_option == option1 or correct_option == option2 or correct_option == option3 or correct_option == option4):
                flash("Invalid correct option")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            new_question = Question(
                quiz_id = quiz_id,
                question_title = question_title,
                question_statement = question_statement,
                option1 = option1,
                option2 = option2,
                option3 = option3,
                option4 = option4,
                correct_option = correct_option
            )

            db.session.add(new_question)
            db.session.commit()

            flash("Question added successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_subject/<int:subject_id>")
def delete_subject(subject_id):
    if session.get('user_role', None) == 'admin':
        subject = Subject.query.filter_by(id = subject_id).first()
        if not subject:
            flash("Subject not found")
            return redirect(url_for("home"))
        
        db.session.delete(subject)
        db.session.commit()

        flash("Subject deleted successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    

@app.route("/delete_chapter/<int:chapter_id>")
def delete_chapter(chapter_id):
    if session.get('user_role', None) == 'admin':
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not chapter:
            flash("Chapter not found")
            return redirect(url_for("home"))
        
        db.session.delete(chapter)
        db.session.commit()

        flash("Chapter deleted successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    if session.get('user_role', None) == 'admin':
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash("Quiz not found")
            return redirect(url_for("quiz_management"))
        
        db.session.delete(quiz)
        db.session.commit()

        flash("Quiz deleted successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    if session.get('user_role', None) == 'admin':
        question = Question.query.filter_by(id = question_id).first()
        if not question:
            flash("Question not found")
            return redirect(url_for("quiz_management"))
        
        db.session.delete(question)
        db.session.commit()

        flash("Question deleted successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/users")
def users():
    if session.get('user_role', None) == 'admin':
        users = User.query.all()
        return render_template("users.html", users = users)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if session.get('user_role', None) == 'admin':
        user = User.query.filter_by(id = user_id).first()
        if not user:
            flash("User not found")
            return redirect(url_for("home"))
        
        db.session.delete(user)
        db.session.commit()

        flash("User deleted successfully")

        return redirect(url_for("users"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))

# most part of milestone 5 was done while working on quiz attempt page
    
@app.route("/attempt_quiz/<int:quiz_id>" , methods = ["GET","POST"])
def attempt_quiz(quiz_id):
    if session.get('user_role', None) == 'user':
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash("Quiz not found")
            return redirect(url_for("home"))
        
        questions = Question.query.filter_by(quiz_id = quiz_id).all()
        if not questions:
            flash("No questions found")
            return redirect(url_for("home"))
        
        if request.method == "GET":
            if datetime.now().date() == quiz.date_of_quiz:
                if 'target_time' not in session:
                    target_time = datetime.now() + timedelta(minutes = quiz.duration)
                    session["target_time"] = target_time.isoformat()
                targettime = session["target_time"]
                return render_template("attempt_quiz.html",quiz = quiz, questions = questions, target_time = targettime)
            elif datetime.now().date() < quiz.date_of_quiz:
                flash("Quiz has not started yet")
                return redirect(url_for("home"))
            else:
                flash("Quiz has already ended")
                return redirect(url_for("home"))
        
        if request.method == "POST":
            user_answers = {}
            for question in questions:
                user_answers[str(question.id)] = request.form.get(str(question.id),None)
            score = 0
            result = []
            
            for question in questions:
                if user_answers[str(question.id)] == question.correct_option:
                    score += 1
            
            for question in questions:
                result.append({
                    "question_statement": question.question_statement,
                    "option1": question.option1,
                    "option2": question.option2,
                    "option3": question.option3,
                    "option4": question.option4,
                    "user_answer": user_answers[str(question.id)],
                    "correct_answer": question.correct_option,
                    "is_correct": user_answers[str(question.id)] == question.correct_option
            })

            user_email = session.get('user_email', None)
            user = User.query.filter_by(user_email = user_email).first()

            if not user:
                flash("User not found")
                return redirect(url_for("home"))

            results = Result(
                user_id = user.id,
                quiz_id = quiz.id,
                score = score,
                time_stamp_of_attempt = datetime.now()
            )

            result1 = Result.query.filter_by(user_id = user.id, quiz_id = quiz.id).first()
            
            if result1:
                flash("The score of your first attempt will be considered for the result...You can attempt the quiz any number of times...")
                return render_template("result.html",quiz = quiz, score = score, result = result, time_stamp_of_attempt = datetime.now())

            for question in questions:
                user_answer = UserAnswers(
                    user_id = user.id,
                    question_id = question.id,
                    answer = user_answers[str(question.id)]
                )
                db.session.add(user_answer)
            
            db.session.add(results)
            db.session.commit()

        return render_template("result.html",quiz = quiz, score = score, result = result)
        
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/scores")
def scores():
    if session.get('user_role', None) == 'user':
        user_email = session.get('user_email', None)
        user = User.query.filter_by(user_email = user_email).first()
        if not user:
            flash("User not found")
            return redirect(url_for("home"))
        
        results = Result.query.filter_by(user_id = user.id).all()

        return render_template("scores.html",results = results)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/result_view/<int:quiz_id>")
def result_view(quiz_id):
    if session.get('user_role', None) == 'user':
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash("Quiz not found")
            return redirect(url_for("scores"))
        
        user_email = session.get('user_email', None)
        user = User.query.filter_by(user_email = user_email).first()
        if not user:
            flash("User not found")
            return redirect(url_for("home"))
        
        results = Result.query.filter_by(user_id = user.id, quiz_id = quiz.id).first()
        if not results:
            flash("Result not found")
            return redirect(url_for("scores"))
        
        user_answers = UserAnswers.query.filter_by(user_id = user.id).all()
        if not user_answers:
            flash("User answers not found")
            return redirect(url_for("scores"))
        
        questions = Question.query.filter_by(quiz_id = quiz.id).all()
        if not questions:
            flash("Questions not found")
            return redirect(url_for("scores"))
        
        result = []
        for question in questions:
            for user_answer in user_answers:
                if user_answer.question_id == question.id:
                    result.append({
                        "question_statement": question.question_statement,
                        "option1": question.option1,
                        "option2": question.option2,
                        "option3": question.option3,
                        "option4": question.option4,
                        "user_answer": user_answer.answer,
                        "correct_answer": question.correct_option,
                        "is_correct": user_answer.answer == question.correct_option
                    })
        
        return render_template("result.html",quiz = quiz, score = results.score, result = result, time_stamp_of_attempt = results.time_stamp_of_attempt)
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
            
@app.route("/search")
def search():
    search_type = request.args.get('search_type', None)
    search = request.args.get('search', None)
    if session.get('user_role', None):
        if search_type == "subject":
            results = Subject.query.filter_by(name = search).all()
        if search_type == "chapter":
            results = Chapter.query.filter_by(name = search ).all()
        if search_type == "quiz":
            results = Quiz.query.filter_by(name = search).all()
        if session.get('user_role',None) == 'admin':
            if search_type == "user":
                results = User.query.filter_by(username = search).all()
            if search_type == "question":
                results = Question.query.filter_by(question_title = search ).all()
                
        return render_template("search_result.html",results = results,search_type = search_type)
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/summary")
def summary():
    if session.get('user_role', None) == 'user':
        user_email = session.get('user_email', None)
        user = User.query.filter_by(user_email = user_email).first()

        quizzes = Quiz.query.all()
        data = []

        for quiz in quizzes:
            results = Result.query.filter_by(user_id = user.id, quiz_id = quiz.id).first()
            if not results:
                score = 0
            else:
                score = results.score*100/len(Question.query.filter_by(quiz_id = results.quiz.id).all())

            quizlabel = quiz.name + " - " + quiz.chapter.name
            
            data.append({
                'name': quizlabel,
                'score': score
            })

            chart = {
                'labels':[data['name'] for data in data],
                'datasets':[
                    {
                        'label': 'Percentage Score',
                        'data': [data['score'] for data in data],
                        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    }
                ]
            }

        return render_template("summary.html",chart = chart)
    
    if session.get('user_role', None) == 'admin':
        quizzes = Quiz.query.all()
        data = []

        for quiz in quizzes:
            results = Result.query.filter_by(quiz_id = quiz.id).all()
            if not results:
                score = 0
            else:
                score = sum([results.score*100/len(Question.query.filter_by(quiz_id = results.quiz.id).all()) for results in results])/len(results)

            quizlabel = quiz.name + " - " + quiz.chapter.name
            
            data.append({
                'name': quizlabel,
                'score': score
            })

            chart = {
                'labels':[data['name'] for data in data],
                'datasets':[
                    {
                        'label': 'AverageScore',
                        'data': [data['score'] for data in data],
                        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                        'borderColor': 'rgba(54, 162, 235, 1)', 
                        'borderWidth': 1
                    }
                ]
            }

        return render_template("summary.html",chart = chart)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))