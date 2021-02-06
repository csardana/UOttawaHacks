import db_util as db
import uuid

session = db.createSession()

print(session)

login_info = {
    'dob': '1999-03-02',
    'firstname': 'Mark',
    'lastname': 'Test',
    'nickname': 'RapidBadger'
}

s1 = db.insertNickname(session, login_info)
print("s2")
s2 = db.retrieveLeaderboard(session)
for row in s2:
    print (row[0], row[1], row[2], row[3])
print("s3")
s3 = db.updateScore(session, 40, login_info['nickname'], "guessscore")
print("s4")
s4 = db.retrieveLeaderboard(session)
for row in s4:
    print (row[0], row[1], row[2], row[3])