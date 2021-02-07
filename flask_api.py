from cassandra.cluster import ResultSet
import flask
import random_generator as rg
import db_util as db
import json

scoreIncrement = 10

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/leaderboard', methods=['GET'])
def getLeaderboard():
    session = db.createSession()
    lb = db.retrieveLeaderboard(session)
    fulldict = dict()
    for row in lb:
        nickname = row[0]
        rowdict = dict()
        rowdict['guessScore'] = row[1]
        rowdict['hintScore'] = row[2]
        rowdict['totScore'] = row[3]

        fulldict[nickname] = rowdict

    results = json.loads(fulldict)
    return results 

@app.route('/createNickname', methods=['POST'])
def createNickname():
    firstname = flask.request.form['firstname']
    lastname = flask.request.form['lastname']
    dob = flask.request.form['dob']
    nickname = rg.generate(firstname, lastname, dob)
    return nickname

@app.route('/addGuessScore/<username>', methods=['PUT'])
def addGuessScore(username=None):
    if username is None:
        return 1
    else:
        session = db.createSession()
        status = db.updateScore(session, scoreIncrement, username, "guessScore")
        return status

@app.route('/addHintScore/<username>', methods=['PUT'])
def addHintScore(username=None):
    if username is None:
        return 1
    else:
        session = db.createSession()
        status = db.updateScore(session, scoreIncrement, username, "hintScore")
        return status

@app.route('/resetLeaderboard', methods=['PUT'])
def resetLeaderboard():
    session = db.createSession()
    status = db.resetScores(session)
    return status

@app.route('/sendMsg', methods=['POST'])
def sendMsg():
    pass