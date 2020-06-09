from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# initialize a variable called responses to be an list with placeholders for each quesiton in survey
responses = ['blank'] * len(survey.questions)

@app.route('/')
def home():
  # pass in title of the survey, the instructions
  return render_template('start.html', survey = survey)

@app.route('/questions/<int:num>', methods=['GET','POST'])
def questions(num):
  # check to see if all questions are answered
  if 'blank' not in responses:
    flash(f'All questions have been answered')
    return redirect('/thankyou')

  # if num is greater than number of questions redirect to next question
  if num not in range(1,len(responses)+1):
    # find first 'blank' in responses
    unanswered = responses.index('blank')
    # set num to first unanswered
    num = unanswered
    # flash message for redirect
    flash(f'That question does not exist! Here is your next question..')
    # redirect
    return redirect('/questions/' + str(num+1))

  # handle GET request
  question = survey.questions[num-1]

  # handle POST request
  if request.method == 'POST':
    # get answer from POST vars
    answer = request.form['answer']
    # insert answer into responses
    responses[num-1] = answer
    # increment number
    num += 1
    # redirect to next quesiton
    return redirect('/questions/' + str(num))
  # render question page
  return render_template('questions.html', num=num, question = question, survey = survey)

@app.route('/thankyou')
def thankyou():
  return render_template('done.html', survey = survey)

