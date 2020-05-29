# trivia_api

The aim of this project is to test user's knowledge via some questions, the user can add new question, search for question, view questions based on their categories and play quiz which consists of 5 question of general or specific type. Follow instruction in both backend\README.md and frontend\README.md files to install project dependencies and to run the project.

Authentication: there are no credential required
Base URL: the project is running locally, so we use localhost as base url. http: http://127.0.0.1:5000

Errors: 
Basically, HTTP response codes will be used to refers to the request's status.
200 - "OK". In case if request is working as expected.
400 - "Bad request". if request is set in a particular syntax that couldn't be handled by the endpoint.
404 - "Resource not found". the subject recourse could not be found.
405 - "not allowed method". Method is not added as allowed method for requested endpoint.
401 - "Unauthorized". user is not unauthorized.
422- "Unprocessable". the request could not be processed, due to some semantic errors.
500 - "Internal Server Error". the error is raised by backend server.


The API Endpoints provided to support functionalities of this projects are listed below, the response of each is formed in json format:

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample: http://127.0.0.1:5000/categories
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Retrieves questions paginated by 10, the range of questions will be specified based on page parmeter
- Query String Parameters: 
    page[optional], it should be of type integer.
- Sample: http://127.0.0.1:5000/questions?page=1
- Returns: An object contains a list of question objects - each contains answer, category, difficulty, id, question -, total number of existing questions, categories object which contains a object of id: category_string key:value pairs.
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 18
}

DELETE '/questions/{question_id}'
- Deletes question with specific ID
- Request Arguments: 
    question ID [required], it should be of type integer.
- Sample: http://127.0.0.1:5000/questions/10
- Returns: An object of question_id as the ID of deleted question.
{
  "question_id": 25, 
  "success": true
}


POST '/questions'
- The taken action will vary based on sent parameters: if "searchTerm" is included as body parameter, it will retrieve all questions with searchTerm is substring of question. In other side, if "searchTerm" is not included, it will create a new question using values from request body parameters. 
- Request Body Parameters: 
    searchTerm [optional], it should be of type string.
    below parameters are required if searchTerm is not included
    answer [required], it should be of type string.
    question [required], it should be of type string.
    category [required], it should be of type integer.
    difficulty [required], it should be of type integer.
- Returns: only if searchTerm is included, it will return A list of question objects that match the search term, and totalQuestions as the total number of retrieved questions.
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}

GET '/categories/{category_id}/questions'
- Retrieves all questions belong to selected category.
- Request Parameters: 
    category_id[required], it should be of type integer.
- Sample: http://127.0.0.1:5000/categories/1/questions
- Returns: An object contains a list of question objects - each contains answer, category, difficulty, id, question -, total number of questions of selected category, categories object which contains a object of selected category, formed in key:value pairs(id: category_string).
{
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 3
}

post '/quizzes'
- Returns a question within particular category (optional), which is not exists in list of previous sent questions.
- Request Body Parameters: 
    category [optional], it should be of type integer.
    previous_questions [optional], a list of integers.
- Returns: returns a question object which contains answer, category, difficulty, id, question keys.
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}



