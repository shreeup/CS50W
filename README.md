# shreeup


Voting System Web application
This app can be used to conduct survey. It presents users with list of questions with set of choices. 
Based on the number votes graph will be generated and displayed to the voter giving share of each vote.

Distinctiveness and Complexity

Project uses DJANGO REST framework to collect votes and persist to sqlite3 databse and html,css,javascript on front end to display polls and graph.

It uses standard authentication mechanism and 2 other model to represent Question and choice. Upon login user will be presented a survey after submit 
a chart will be displayed giving response statistics for that question.

Django-auth Registration

## Project Structure

The Project consists of 2 subfolders with main config project and another project defining porject specific models , views

### config project folder:

Here setting.py file exists.

### polls/ app:

declares name of project

#### views.py

defines api to persist, fetch data from storage

- index displaying all the questions from database.

- detail fetchs specific question by question id

- results displays overall polls results of question and graph with share for eaach choice

- vote allows user to caste their vote to choice



If user is not logged in, the loging page is displayed, inviting the user to register right away.

Register page offers to enter email/password to register.

When logged in, the user is redirected to home page where all the polls question list is displayed.
