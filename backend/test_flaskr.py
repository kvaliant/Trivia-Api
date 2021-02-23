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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','admin','localhost:5432', self.database_name)
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
    TODO DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    def test_error_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    '''def test_delete_questions(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)'''
    
    def test_error_delete_questions(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_add_questions(self):
        res = self.client().post('/questions',json={'question':'Test','answer':'Test','category':1,'difficulty':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_add_questions(self):
        res = self.client().post('/questions',json={'question':'Test','answer':'Test'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_search_questions(self):
        res = self.client().post('/questions',json={'searchTerm':'a'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_search_questions(self):
        res = self.client().post('/questions',json={'searchTerm':'abcdefghijklmnopqrstuvwxyz'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_get_next_question(self):
        res = self.client().post('/quizzes',json={"previous_questions":[],"quiz_category":{"type":"Art","id":"1"}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_finish_get_next_question(self):
        res = self.client().post('/quizzes',json={"previous_questions":[],"quiz_category":{"type":"None","id":"9"}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()