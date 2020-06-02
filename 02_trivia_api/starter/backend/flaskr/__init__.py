import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after
    completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Alow-Hearders",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PUT, POST, PATCH, DELETE, OPTIONS")
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        try:
            categorieslist = [category.format() for category
                              in Category.query.all()]
            #  form categories as dictionay to match expected frontend result
            categories_dict = {category["id"]: category["type"]
                               for category in categorieslist}
            return jsonify({"success": True,
                            "categories": categories_dict})
        except:
            abort(400)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        try:
            page = request.args.get('page', 1, int)
            start = (page-1)*QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.all()
            categorieslist = [category.format() for category
                              in Category.query.all()]
            categories_dict = {category["id"]: category["type"]
                               for category in categorieslist}
            questionslist = [question.format() for question in questions]
            questionslist_paginated = questionslist[start:end]
            # if page is not valid
            if len(questionslist_paginated) == 0:
                abort(404)
            else:
                return jsonify({"success": True,
                                "questions": questionslist_paginated,
                                "total_questions": len(questions),
                                "categories": categories_dict,
                                "current_category": None})

        # catch type of error
        except EOFError:
            abort(400)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id ==
                                             question_id).one_or_none()
            if question is None:
                abort(404)
            # check if question is exits, otherwise raise 422 error
            try:
                question.delete()
            except:
                abort(422)
            return jsonify({
                "success": True,
                "question_id": question_id})
        except EOFError:
            abort(400)

    @app.route('/questions', methods=['POST'])
    def post_question():
        if request.data:
            data = request.get_json()
            '''
            @TODO:
            Create a POST endpoint to get questions based on a search term.
            It should return any questions for whom the search term
            is a substring of the question.

            TEST:Search by any phrase.The questions list will update to include
            only question that include that string within their question.
            Try using the word "title" to start.
            '''
            #  check if request body contains searchTerm to proceed
            #  retrieving questions based on search trerm,
            #  otherwise it wull create a new question
            if 'searchTerm' in data:
                try:
                    searchTerm = data["searchTerm"]
                    questions = Question.query.filter(Question.question.ilike(
                                                     '%'+searchTerm+'%')).all()
                    questionlist = [q.format() for q in questions]
                    categorieslist = [category.format() for category
                                      in Category.query.all()]
                    return jsonify({"success": True,
                                    "questions": questionlist,
                                    "totalQuestions": len(questionlist),
                                    "current_category": None})
                except:
                    abort(422)
            else:
                '''
                @TODO:
                Create an endpoint to POST a new question,
                which will require the question and answer text,
                category, and difficulty score.

                TEST: When you submit a question on the "Add" tab,
                the form will clear and the question will appear
                at the end of the last page
                of the questions list in the "List" tab.
                '''
                try:
                    question = data["question"]
                    answer = data["answer"]
                    difficulty = data["difficulty"]
                    category = data["category"]
                    ques = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
                    try:
                        ques.insert()
                    except:
                        abort(422)
                    return jsonify({"success": True})
                except EOFError:
                    abort(200)
        else:
            abort(400)
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=category_id).all()
            #  set the format of returned questions
            questionlist = [q.format() for q in questions]
            current_category = Category.query.get(category_id)
            return jsonify({"success": True,
                            "questions": questionlist,
                            "total_questions": len(questionlist),
                            "current_category": current_category.format()})
        except:
            abort(404)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        data = request.get_json()
        quiz_category = None
        if "quiz_category" in data and data["quiz_category"] is not None:
            quiz_category = data["quiz_category"]["id"]
        previous_questions = None
        if "previous_questions" in data:
            previous_questions = list(data["previous_questions"])
        try:
            if previous_questions is not None:
                if quiz_category is not None and quiz_category != 0:
                    question = Question.query.filter(~Question.id.in_
                                                     (previous_questions),
                                                     Question.category ==
                                                     quiz_category)\
                                                    .order_by(Question.id)\
                                                    .limit(1).one_or_none()
                else:
                    question = Question.query.filter(~Question.id.in_
                                                     (previous_questions))\
                                                     .order_by(Question.id)\
                                                     .limit(1).one_or_none()
            else:
                if quiz_category is not None and quiz_category != 0:
                    question = Question.query.filter(Question.category ==
                                                     quiz_category)\
                                                    .order_by(Question.id)\
                                                    .limit(1).one_or_none()
                else:
                    question = Question.query.order_by(Question.id)\
                                                      .limit(1).one_or_none()
            if question is None:
                return jsonify({"success": True})
            else:
                return jsonify({"success": True,
                                "question": question.format()})
        except:
            abort(400)
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    # creating error handlers to customize returned response
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Resource not found"}), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False,
                        "error": 401,
                        "message": "Unauthorized"}), 401

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({"success": False,
                        "error": 405,
                        "message": "not allowed method"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 422,
                        "message": "Unprocessable"}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False,
                        "error": 500,
                        "message": "Internal Server Error"}), 500

    return app
