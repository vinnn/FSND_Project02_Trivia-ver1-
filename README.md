# Full Stack API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

The application does:

1. Display questions - both all questions and by category. 
2. Delete questions.
3. Add a new question/answer.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows [PEP8 style guidelines] (https://www.python.org/dev/peps/pep-0008/)


## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have python3, pip and node installed on their local machines.

#### Backend
From the backend folder, run 'pip3 install requirements.txt', which includes all required packages.

To run the application, run the following commands:
'''
export FLASK_APP=flakr
export FLASK_ENV=development
flask run
'''

These commands put the application in development mode and directs our application to use the '__init__.py' file in our flaskr folder.
Working in development mode shaows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation] (http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on 'http://127.0.0.1:5000/' by default and is a proxy in the fronend configuration.


#### Frontend
From the frontend folder, run the following commands to start the client:
'''
npm install  // only once to install dependencies
npm start
'''

By default, the frontend will run on localhost:3000

### Tests
In order to run tests navigate to the backend folder and run the following commands:
'''
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
'''

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.


## API Reference

### Getting Started
- Base URL: at present this app can only be run locally and is not hosted as a base  URL. The backend app is hosted at the default, 'http://127.0.0.1:5000/', which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
'''
{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 404: method not allowed
- 422: unprocessable


### Endpoints

#### GET /categories
- General:
    - Returns a list of categories and a success value.
- Sample: curl http://127.0.0.1:5000/categories

'''
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
'''


#### GET /questions
- General:
    - Returns the list of categories, the list of questions, the total number of questions and a success value.
    - The list of questions returned is paginated in groups of 10. 
- Sample: curl http://127.0.0.1:5000/questions

'''
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "In England", 
      "category": 3, 
      "difficulty": 1, 
      "id": 30, 
      "question": "Where is London?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "success": true, 
  "total_questions": 23
}
'''


#### DELETE /questions/(question_id)
- General:
    - Delete the question with the id 'question_id' if it exists. Returns a deleted value, the id of the deleted question and a success value.
- Sample: curl http://127.0.0.1:5000/questions/5 -X DELETE

'''
{
  "deleted": true, 
  "question_deleted_id": 5, 
  "success": true
}
'''

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. 
    Returns a created value, the id of the created question and a success value.
- Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is Ted?", "answer": "the teacher", "category": 2, "difficulty": 1}' 

'''
{
  "created": true, 
  "created_question_id": 32, 
  "success": true
}
'''

#### POST /searched_questions
- General:
    - Searches a question that includes the searchTerm. 
    Returns the list of questions that contain the searchTerm, the total number of questions found and a success value.
- Sample: curl http://127.0.0.1:5000/searched_questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"heav"}' 

'''
{
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
'''


#### GET /categories/(category_id)/questions
- General:
    - Get all the questions for category 'category_id'
    Returns the category, the list of questions in that category, the total number of questions in the category and a success value.
- Sample: curl http://127.0.0.1:5000/categories/6/questions

'''
{
  "current_category": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
'''


#### POST /quizzes
- General:
    - Get all the questions for category 'category_id'
    Returns the category, the list of questions in that category, the total number of questions in the category and a success value.
- Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography", "id":"3"}, "previous_questions":[]}' 

'''
{
  "previousQuestions": [
    30
  ], 
  "question": {
    "answer": "In England", 
    "category": 3, 
    "difficulty": 1, 
    "id": 30, 
    "question": "Where is London?"
  }, 
  "success": true
}
'''


## Deployment 
N/A

# Authors
Udacity, with my humble student contribution

# Acknowledgements
Udacity and everybody on the Udacity forum


