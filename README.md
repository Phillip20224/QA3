# QA3

#ChatGPT pretty much came up with the entire code.

#Instructions for quiz bowl application

#Clicking run on quizapp.py will open the GUI that will allow the selection of admin or take quiz which is open for anyone.

#When take quiz is selected the user will choose the course that they want to answer 10 questions for.
#The quiz is set to randomly choose 10 questions from the course table so repeat questions are likely but may help final score.
#Once the 10 questions are answered it will return back to the main selection page where they can switch to admin or repeat the path for another quiz.

#When admin is clicked it will ask for a username and password which the dictionary in coursequestions.py provides. 
#The admin can then choose between adding questions (where if they add a question to a currently non-existing course it will create a new table), vuewing the tables containing questions and answers, deleting questions, or modifying questions. 
#The initial courses are found in a list in coursequestions.py but more can be added through the admin function.
#For each function the question ID is the number it is associated with.
#NOTE: the database has saved many of the same question before I limited it to 10 questions at a time but it still functions fine. 
#Once the admin is done they can simply close the windows until they return to the main selection page or close it too if not wanting to take a quiz. 

#checkquestionsdb.py provides another way to view what is in the database whenever a table is selected BUT doesn't seem to be needed.