from app import app
from flask import render_template, request, redirect, url_for, flash, session
from database import *
from datetime import datetime

@app.route("/edit_subject/<int:subject_id>" , methods = ["GET","POST"])
def edit_subject(subject_id):
    if session.get('user_role', None) == 'admin':
        subject = Subject.query.filter_by(id = subject_id).first()
        if not subject:
            flash("Subject not found")
            return redirect(url_for("home"))
        
        if request.method == "GET":
            return render_template("edit_subject.html",subject = subject)
        
        if request.method == "POST":
            name = request.form.get("name",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("edit_subject",subject_id = subject_id))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("edit_subject",subject_id = subject_id))
            
            subject.name = name
            subject.description = description

            db.session.commit()

            flash("Subject updated successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))

@app.route("/edit_chapter/<int:chapter_id>" , methods = ["GET","POST"])
def edit_chapter(chapter_id):
    if session.get('user_role', None) == 'admin':
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not chapter:
            flash("Chapter not found")
            return redirect(url_for("home"))
        
        if request.method == "GET":
            return render_template("edit_chapter.html",chapter = chapter)
        
        if request.method == "POST":
            name = request.form.get("name",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("edit_chapter",chapter_id = chapter_id))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("edit_chapter",chapter_id = chapter_id))
            
            chapter.name = name
            chapter.description = description

            db.session.commit()

            flash("Chapter updated successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/edit_quiz/<int:quiz_id>" , methods = ["GET","POST"])
def edit_quiz(quiz_id):
    if session.get("user_role",None) == "admin":
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash("Quiz not found")
            return redirect(url_for("quiz_management"))
        
        if request.method == "GET":
            chapters = Chapter.query.all()
            return render_template("edit_quiz.html",quiz = quiz, chapters = chapters)
        
        if request.method == "POST":
            chapters = Chapter.query.all()
            name = request.form.get("name",None)
            chapter_id = request.form.get("chapter_id",None)
            date_of_quiz = request.form.get("date",None)
            duration = request.form.get("duration",None)
            remarks = request.form.get("remarks",None)

            if not chapter_id:
                flash("Chapter is required")
                return redirect(url_for("edit_quiz",quiz_id = quiz_id))
            
            if not name:
                flash("Name is required")
                return redirect(url_for("edit_quiz",quiz_id = quiz_id))
            
            if not date_of_quiz:
                flash("Date is required")
                return redirect(url_for("edit_quiz",quiz_id = quiz_id))
            
            if not duration:
                flash("Duration is required")
                return redirect(url_for("edit_quiz",quiz_id = quiz_id))
            
            chapter = Chapter.query.filter_by(id = chapter_id).first()
            if not chapter:
                flash("Chapter not found")
                return redirect(url_for("edit_quiz",quiz_id = quiz_id))
            
            date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()
            duration = int(duration)

            quiz.chapter_id = chapter_id
            quiz.name = name
            quiz.date_of_quiz = date_of_quiz
            quiz.duration = duration
            quiz.remarks = remarks

            db.session.commit()

            flash("Quiz updated successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("quiz_management"))
    
@app.route("/edit_question/<int:question_id>" , methods = ["GET","POST"])
def edit_question(question_id):
    if session.get("user_role",None) == "admin":
        question = Question.query.filter_by(id = question_id).first()
        if not question:
            flash("Question not found")
            return redirect(url_for("quiz_management"))
        
        if request.method == "GET":
            return render_template("edit_question.html",question = question)
        
        if request.method == "POST":
            question_title = request.form.get("question_title",None)
            question_statement = request.form.get("question_statement",None)
            option1 = request.form.get("option1",None)
            option2 = request.form.get("option2",None)
            option3 = request.form.get("option3",None)
            option4 = request.form.get("option4",None)
            correct_option = request.form.get("correct_option",None)

            if not question_title:
                flash("Question title is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not question_statement:
                flash("Question statement is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not option1:
                flash("Option1 is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not option2:
                flash("Option2 is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not option3:
                flash("Option3 is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not option4:
                flash("Option4 is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if not correct_option:
                flash("Correct option is required")
                return redirect(url_for("edit_question",question_id = question_id))
            
            if option1 == option2 or option1 == option3 or option1 == option4 or option2 == option3 or option2 == option4 or option3 == option4:
                flash("Options should be unique")
                return redirect(url_for("edit_question",question_id = question_id))
            
            question.question_title = question_title
            question.question_statement = question_statement
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.correct_option = correct_option

            db.session.commit()

            flash("Question updated successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("quiz_management"))
    
def no_of_questions(chapter_id):
    chapter = Chapter.query.filter_by(id = chapter_id).first()

    no_of_questions = sum([len(quiz.questions) for quiz in chapter.quizzes])
    return no_of_questions

def quiz_questions(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()

    no_of_questions = len(quiz.questions)
    return no_of_questions


app.jinja_env.globals.update(no_of_questions = no_of_questions, quiz_questions = quiz_questions)


