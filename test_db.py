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
s3 = db.getUseridFromNickname(session, login_info['nickname'])
print(s3)
print("s4")
s4 = db.updateScore(session, 40, s3, "guessscore")
print("s5")
s5 = db.retrieveLeaderboard(session)
for row in s5:
    print (row[0], row[1], row[2], row[3])