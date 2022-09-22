# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


# ----------------------------------------------------------------------------#
# Test Class.
# ----------------------------------------------------------------------------#
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


    # Setup.
    # ----------------------------------------#
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # creates a new question object, to be used
        # in the POST question tests:
        self.new_question = {
            'question': 'Who is Titi?',
            'answer': 'Your cat',
            'difficulty': 1,
            'category': 1 
        }
        self.new_search = {
            'searchTerm': 'creator'
        }
        self.new_quiz = {
          'quiz_category': {'type': 'Geography', 'id': '3'},
          'previous_questions': []
        }

  # Teardown.
  # ----------------------------------------#    
    def tearDown(self):
        """Executed after reach test"""
        pass

  # Test. [GET NON-EXISTENT URL => ERROR ]
  # ----------------------------------------#    
    def test_404_nonexistent_url(self):
        # Get response by making client make the GET request:
        res = self.client().get('/')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

  # Test. [GET CATEGORIES => OK ]
  # ----------------------------------------#    
    def test_200_get_categories(self):
        # Get response by making client make the GET request:
        res = self.client().get('/categories')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

  # Test. [GET QUESTIONS => OK ]
  # ----------------------------------------#    
    def test_200_get_questions(self):
        # Get response by making client make the GET request:
        res = self.client().get('/questions')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])                
        self.assertTrue(data['categories'])

  # Test. [DELETE QUESTION id => OK ]
  # ----------------------------------------#    
    def test_200_delete_question(self):
        # Get response by making client make the GET request:
        res = self.client().delete('/questions/2')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], True)

  # Test. [DELETE NON-EXISTENT QUESTION => ERROR ]
  # ----------------------------------------#    
    def test_422_delete_nonexistent_question(self):
        # Get response by making client make the GET request:
        res = self.client().delete('/questions/2000')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

  # Test. [POST QUESTION id => OK ]
  # ----------------------------------------#    
    def test_200_post_question(self):
        # Get response by making client make the 
        # POST request (new_question is defined above):
        res = self.client().post('/questions', json=self.new_question)
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], True)

  # Test. [POST QUESTION WITH NO INFO => ERROR ]
  # ----------------------------------------#    
    def test_422_post_wrong_question_info(self):
        # Get response by making client make the 
        # POST request, without json input info:
        res = self.client().post('/questions')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

  # Test. [SEARCH QUESTION => OK ]
  # ----------------------------------------#    
    def test_200_search_question(self):
        # Get response by making client make the 
        # POST request (new_question is defined above):
        res = self.client().post('/searched_questions', json=self.new_search)
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


  # Test. [SEARCH WITH NO SEARCHTERM => ERROR ]
  # ----------------------------------------#    
    def test_422_search_no_searchterm(self):
        # Get response by making client make the 
        # POST request, without json input info:
        res = self.client().post('/searched_questions')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

  # Test. [QUESTION BY CATEGORY => OK ]
  # ----------------------------------------#    
    def test_200_get_question_by_category(self):
        # Get response by making client make the 
        # GET request (new_question is defined above):
        res = self.client().get('/categories/2/questions')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 2)

  # Test. [QUESTION BY CATEGORY NON-EXISTING CATEGORY => ERROR ]
  # ----------------------------------------#    
    def test_422_get_question_nonexistent_category(self):
        # Get response by making client make the 
        # GET request, without json input info:
        res = self.client().get('/categories/3000/questions')
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

  # Test. [QUIZ => OK ]
  # ----------------------------------------#    
    def test_200_get_quiz_questions(self):
        # Get response by making client make the 
        # POST request:
        res = self.client().post('/quizzes', json=self.new_quiz)

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

  # Test. [QUIZ FOR NON-EXISTING CATEGORY => ERROR ]
  # ----------------------------------------#    
    def test_422_get_quiz_nonexistent_category(self):
        # Get response by making client make the 
        # POST request:
        res = self.client().post('/quizzes', json={
          'quiz_category': {'id': 3000, 'type':'Geography'},
          'previous_questions': []
          })

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()