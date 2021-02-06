from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra.auth import PlainTextAuthProvider
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
    user_id = uuid.uuid1()
    try:
        st = session.prepare(
            """
            INSERT INTO Nicknames (user_id, dob, firstname, lastname, nickname) VALUES (?, ?, ?, ?, ?)
            """
        )
        status = session.execute(st, (
                user_id, 
                login_info['dob'], 
                login_info['firstname'], 
                login_info['lastname'], 
                login_info['nickname']
            )
        )
        st2 = session.prepare(
            """
            INSERT INTO Leaderboard (user_id, guessscore, hintscore, totalscore) VALUES (?, ?, ?, ?)
            """
        )
        status2 = session.execute(st2, (user_id, 0, 0, 0))
        st3 = session.prepare(
            """
            INSERT INTO ids (nickname, user_id) VALUES (?, ?)
            """
        )
        status3 = session.execute(st3, (login_info['nickname'], user_id))
    except Exception as e:
        print(e)
        return 1
    
    return 0

def updateScore(session, addedScore, user_id, scoreType):
    try:
        st = session.prepare(
            "SELECT " + scoreType + ", totalScore FROM Leaderboard WHERE user_id = ?"
        )
        scores = session.execute(st, (user_id,))
        score0 = scores.one()[0] + addedScore
        totScore = scores.one()[1] + addedScore
    except Exception as e:
        print(e)
        return 1

    try:
        statement = "UPDATE Leaderboard SET " + scoreType + " = ?, totalScore = ? WHERE user_id = ?"
        st = session.prepare(statement)
        status = session.execute(st, (score0, totScore, user_id))
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

def getUseridFromNickname(session, nickname):
    #should be mainly for testing
    try:
        st = session.prepare(
            """
            SELECT user_id FROM ids WHERE nickname = ?
            """
        )
        user_id = session.execute(st, (nickname,))
    except Exception as e:
        print(e)
        return 1
    
    return user_id.one()[0]
