# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


# ----------------------------------------------------------------------------#
# helper functions.
# ----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10

# Helper method
def paginate_questions(request, selection):
    # we take the 'request' as argument in order
    # to get the page number. Then obtain the 
    # value of the query parameter 'page', use a 
    # value of 1 by default
    # (calling URL/questions?page=2 will retrieve 
    # book records 11 to 20)
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    
    return current_questions



# ----------------------------------------------------------------------------#
# create_app.
# ----------------------------------------------------------------------------#
def create_app(test_config=None):


  # ----------------------------------------------------------------------------#
  # Configuration.
  # ----------------------------------------------------------------------------#
  app = Flask(__name__)
  # setup_db defined in XX
  setup_db(app)
  # allow CORS for all routes and all domains (*)
  CORS(app)
  # which is equivalent to:
  # cors = CORS(app, resources={r"/*": {"origins": "*"}})


  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,PUT,POST,DELETE,OPTIONS')
    return response


  # ----------------------------------------------------------------------------#
  # Controllers.
  # ----------------------------------------------------------------------------#

  # Retrieve all available categories.
  # ----------------------------------------#
  '''
  Endpoint to handle GET requests for all 
  available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    try:
      selection_categories = Category.query.all()

      all_categories = Category.query.all()
      # categories here need to be returned as a dictionary 
      # in order to be used in FormView.js:
      all_categories_formatted = {category.id: category.type for category in all_categories}

      if len(all_categories_formatted) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'categories': all_categories_formatted
      })
    except:
      abort(422)


  # Retrieve all questions.
  # ----------------------------------------#
  '''
  Endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  To return a list of questions, number of total 
  questions, current category, categories. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    try:
      selection_questions = Question.query.order_by(Question.category).all()
      current_questions = paginate_questions(request, selection_questions)

      all_categories = Category.query.all()
      # categories here need to be returned as a dictionary 
      # in order to be used in QuestionView.js:
      all_categories_formatted = {category.id: category.type for category in all_categories}

      if len(current_questions) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection_questions),
        'categories': all_categories_formatted,
        'current_category': ""
      })
    except:
      abort(422)


  # Delete a question.
  # ----------------------------------------#
  '''
  Endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      question.delete() # method defined in models.py
      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'question_deleted_id': question_id,
        'deleted': True
      })
    except:
      abort(422)


  # Post a new question.
  # ----------------------------------------#
  '''
  Endpoint to POST a new question, which will 
  require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    try:
      body = request.get_json()

      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)

      question = Question(
        question=new_question,
        answer=new_answer,
        difficulty=new_difficulty,
        category=new_category)

      question.insert() # method defined in models.py
      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': True,
        'created_question_id': question.id
      })
    except:
      abort(422)


  # Search questions.
  # ----------------------------------------#
  '''
  POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/searched_questions', methods=['POST'])
  def search_questions():
    try:
      body = request.get_json()

      search_term = body.get('searchTerm', None)

      found_questions = (Question.query
                      .filter(Question.question.ilike("%" + search_term + "%"))
                      .all()
                      )

      current_questions = paginate_questions(request, found_questions)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(found_questions),
        'current_category': ""
        })
    except:
      abort(422)


  # Questions by category.
  # ----------------------------------------#
  '''
  GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def question_by_category(cat_id):
    try:
      selection_questions = Question.query.filter(Question.category == cat_id).all()
      current_questions = paginate_questions(request, selection_questions)
 
      if len(current_questions) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection_questions),
        'current_category': cat_id
      })
    except:
      abort(422)


  # Questions for quiz.
  # ----------------------------------------#
  '''
  POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_questions():
    try:
      body = request.get_json()

      print("%%%%%%%%%%%%%%%%%%%% body")
      print(body)

      # Category selected for the quiz
      quiz_category = body.get('quiz_category', None)
      # List of id for previous questions in quiz
      previous_questions_id = body.get('previous_questions', None)

      print("%%%%%%%%%%%%%%%%%%%% previous_questions_id")
      print(previous_questions_id)

      print("%%%%%%%%%%%%%%%%%%%% quiz_category")
      print(quiz_category)

      print("%%%%%%%%%%%%%%%%%%%% quiz_category[id]")
      print(quiz_category["id"])

      # All questions of the selected category
      quiz_questions = Question.query.filter(Question.category == quiz_category["id"]).all()

      if len(quiz_questions) == 0:
        abort(404)

      print("%%%%%%%%%%%%%%%%%%%% quiz_questions")
      print(quiz_questions)

      # List of id's for question not yet asked in quiz
      question_id_remain = [q.id for q in quiz_questions if q.id not in previous_questions_id]

      #quiz_questions_remaining = [q for q in quiz_questions if q not in previous_questions]

      print("%%%%%%%%%%%%%%%%%%%% question_id_remain")
      print(question_id_remain)

      if question_id_remain == []:
        current_question = None

      else:
        # Randomly select the index of an element in question_id_remain
        random_index = random.randrange(len(question_id_remain))

        print("%%%%%%%%%%%%%%%%%%%% random_index")
        print(random_index)

        # Extract the question id for the randomly selected index
        current_question_id = question_id_remain[random_index]
        # Get the question for that id
        #current_question = quiz_questions[current_question_id]
        current_question = [q for q in quiz_questions if q.id == current_question_id][0]

        print("%%%%%%%%%%%%%%%%%%%% random_index")
        print(random_index)
        print("%%%%%%%%%%%%%%%%%%%% current_question_id")
        print(current_question_id)
        print("%%%%%%%%%%%%%%%%%%%% current_question")
        print(current_question)

        current_question = current_question.format()    

        print("%%%%%%%%%%%%%%%%%%%% current_question formatted")
        print(current_question)

        previous_questions_id.append(current_question_id)

        print("previous_questions_id")
        print(previous_questions_id)


      return jsonify({
        'success': True,
        'question': current_question,
        'previousQuestions': previous_questions_id
        })
    except:
      abort(422)



  # Error handlers.
  # ----------------------------------------#
  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422


  return app

    