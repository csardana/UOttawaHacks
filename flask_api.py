from cassandra.cluster import ResultSet
from flask import Flask, render_template, request
import random_generator as rg
import db_util as db
import json
from flask-socketio import SocketIO

scoreIncrement = 10

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app)

chats = []

@app.route('/login')
def displayLogin():
    return render_template('login/index.html')

@app.route('/chat/<chatid>')
def displayChat():
    return render_template('chatbox/index.html')

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
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
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

@socketio.on('send msg')
def sendMsg(content, methods=['GET', 'POST']):
    print('received msg: ' + str(content))
    socketio.emit('display msg', content)


if __name__ == '__main__':
    socketio.run(app, debug=True)