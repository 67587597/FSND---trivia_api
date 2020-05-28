import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','95149514','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["categories"]))
    
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        # check returned data 
        self.assertTrue(len(data["questions"]))
        self.assertEqual(response.status_code, 200)
    
    def test_get_questions_paginated(self):
        response = self.client().get('/questions?page=2')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        # check pagination
        self.assertLessEqual(len(data["questions"]), 10)
        self.assertEqual(response.status_code, 200)
    
    def test_not_valid_page(self):
        response = self.client().get('/questions?page=200000')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        # check returned message
        self.assertEqual(data['message'], "Resource not found")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_question(self):
        id = 9
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is not None:
            response = self.client().delete('/questions/9')
            data = json.loads(response.data)
            question = Question.query.filter(Question.id == id).one_or_none()
            # self.assertIsNone(question)
            self.assertEqual(question, None)
            self.assertEqual(data['success'], True)
            self.assertEqual(response.status_code, 200)
    
    def test_delete_question_resource_not_found(self):
        id = 10
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is None:
            response = self.client().delete('/questions/10')
            data = json.loads(response.data)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "Resource not found")
            self.assertEqual(response.status_code, 404)
    
    def test_search_for_question(self):
        searchTerm = 'title'
        questions = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
        response = self.client().post('/questions', json={"searchTerm": searchTerm})
        data = json.loads(response.data)
        if len(questions) != 0:
            self.assertTrue(data["questions"])
            self.assertEqual(len(questions), data["totalQuestions"])
            self.assertEqual(data['success'], True)
            self.assertEqual(response.status_code, 200)
    
    def test_create_question(self):
        new_question = {"question": "test question?",
        "answer": "test answer.",
        "difficulty": "1",
        "category": "1" 
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
    
    def test_unprocessable_create_question(self):
        new_question = {"question": "test not valid question?",
        "answer": "test not valid answer.",
        "difficulty": "1",
        "category": "test" 
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], "Unprocessable")
        
    def test_get_questions_by_category(self):
        questions = Question.query.filter_by(category=1).all()
        response = self.client().get('categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        # check returned data 
        self.assertTrue(len(data["questions"]))
        self.assertEqual(len(questions), data["totalQuestions"])
    
    def test_failed_get_questions_by_category(self):
        response = self.client().get('categories/test/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")
        self.assertEqual(response.status_code, 404)
    
    def test_get_quiz_question(self):
        body = {"previous_questions": ['What is the heaviest organ in the human body?','Who discovered penicillin?', 'test question?']
        , "quiz_category": "1"
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['question']['question'], "Hematology is a branch of medicine involving the study of what?")
    
    def test_get_quiz_question_no_category_provided(self):
        body = {"previous_questions": ['What is the heaviest organ in the human body?','Who discovered penicillin?', 'test question?']
        , "quiz_category": None
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['question']['question'], "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?")
  

    def test_get_quiz_question(self):
        body = {"previous_questions": ['What is the heaviest organ in the human body?','Who discovered penicillin?', 'test question?']
        , "quiz_category": "test"
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Bad request")
        
        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()