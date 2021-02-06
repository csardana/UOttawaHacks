from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid


def createSession():
    cloud_config= {
        'secure_connect_bundle': './secure-connect-uottahack.zip'
    }
    auth_provider = PlainTextAuthProvider('uottahack', 'c975SKEuyvXW!pU')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('uottahack')
    return session

def retrieveLeaderboard(session):
    leaderboard = session.execute(
        """
        SELECT * FROM Leaderboard;
        """
    )
    return leaderboard

def executePreparedStatement(session, prepSt, params):
    if type(params) is not list:
        params = list(params)
    try:
        st = session.prepare(prepSt)
        data = session.execute(st, params)
    except Exception as e:
        print(e)
        return 1

    return 0

def insertNickname(session, login_info):
    try:
        st = session.prepare(
            """
            INSERT INTO Nicknames (dob, firstname, lastname, nickname) VALUES (?, ?, ?, ?)
            """
        )
        status = session.execute(st, (
                login_info['dob'], 
                login_info['firstname'], 
                login_info['lastname'], 
                login_info['nickname']
            )
        )
        st2 = session.prepare(
            """
            INSERT INTO Leaderboard (nickname, guessscore, hintscore, totalscore) VALUES (?, ?, ?, ?)
            """
        )
        status2 = session.execute(st2, (login_info['nickname'], 0, 0, 0))
        
    except Exception as e:
        print(e)
        return 1
    
    return 0

def updateScore(session, addedScore, nickname, scoreType):
    try:
        st = session.prepare(
            "SELECT " + scoreType + ", totalScore FROM Leaderboard WHERE nickname = ?"
        )
        scores = session.execute(st, (nickname,))
        score0 = scores.one()[0] + addedScore
        totScore = scores.one()[1] + addedScore
    except Exception as e:
        print(e)
        return 1

    try:
        statement = "UPDATE Leaderboard SET " + scoreType + " = ?, totalScore = ? WHERE nickname = ?"
        st = session.prepare(statement)
        status = session.execute(st, (score0, totScore, nickname))
    except Exception as e:
        print(e)
        return 1

    return 0

def resetScores(session):
    try:
        status = session.execute(
            """
            UPDATE Leaderboard SET guessScore = 0, hintScore = 0, totalScore = 0
            """
        )
    except Exception as e:
        print(e)
        return 1
    
    return 0

