import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

import sys

# Please change sys.path to your own directory
sys.path.insert(1, '/DOCUMENTS/Programming/Trivia-Api')
from backend.models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  
  '''
  @TODO DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_category = [category.type for category in categories]
    
    return jsonify({
        'success': True,
        'categories': formatted_category
    })
  '''
  @TODO DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]

    categories = Category.query.all()
    formatted_category = [category.type for category in categories]

    if formatted_questions[start:end] == []:
      abort(404)
    else:
      return jsonify({
          'success': True,
          'questions': formatted_questions[start:end],
          'total_questions': len(formatted_questions),
          'categories': formatted_category
      })
  '''
  @TODO DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).first()
      question.delete()

      return jsonify({
          'success': True,
          'deleted': 1
      })
    except:
      abort(404)
  '''
  @TODO DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()
    
    #route to search_question if 'searchTerm' is in request.get_json()
    if 'searchTerm' in data:
      return search_question(data)

    try:
      new_question = data.get('question', None)
      new_answer = data.get('answer', None)
      new_category = data.get('category', None)
      new_difficulty = data.get('difficulty', None)
      if(new_question == None or new_answer == None or new_category == None or new_difficulty == None):
        abort(422)  
      else:
        question = Question(question= new_question, answer= new_answer, category= new_category, difficulty= new_difficulty)
        question.insert()
        
        return jsonify({
            'success': True,
        })
    except:
      abort(422)
  '''
  @TODO DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  def search_question(data):
    searchTerm = data.get('searchTerm', None)
    questions = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
    
    formatted_questions = [question.format() for question in questions]
    
    if formatted_questions == []:
      abort(404)
    else:
      return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_question': len(formatted_questions)
      })
  '''
  @TODO DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions = Question.query.filter(Question.category == category_id).all()
    formatted_questions = [question.format() for question in questions]

    categories = Category.query.all()
    formatted_category = [category.format() for category in categories]
    if formatted_questions == []:
      abort(404)
    else:
      return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions)
      })
  '''
  @TODO DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    data = request.get_json()
    previous_questions = data.get('previous_questions', None)
    quiz_category = data.get('quiz_category', None).get('id', None)
    category_type = data.get('quiz_category', None).get('type', None)

    category = {}
    #if 'ALL' category option were taken
    if category_type == 'click':
      questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:
      questions = Question.query.filter(Question.category == quiz_category, Question.id.notin_(previous_questions)).all()

    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) == 0:
      return jsonify({'success': True}) 
    else:
      value = random.randint(0, len(formatted_questions)-1)
      return jsonify({
        'success': True,
        'question': formatted_questions[value],
      })
  '''
  @TODO DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "not found"
    })

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    })

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    })
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    })

  return app

    