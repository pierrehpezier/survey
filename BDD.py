import schema
import os
import logging

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_or_create(model, **kwargs):
    session = schema.SESSION()
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        session.close()
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.close()
        return instance

def getQuestions():
    session = schema.SESSION()
    instance = []
    for item in session.query(schema.QUESTIONS).all():
        instance.append(item.QUESTION)
    session.close()
    return instance


def getScore(questionid):
    session = schema.SESSION()
    score = 0
    for item in session.query(schema.VOTES).filter_by(QUESTION=questionid).all():
        score += item.SCORE
    session.close()
    return score

def createUser(IP, USER_AGENT):
    session = schema.SESSION()
    instance = schema.USERS(IP=IP, USER_AGENT=USER_AGENT)
    session.add(instance)
    session.commit()
    userid = instance.id
    session.close()
    return userid

def clientExists(IP, USER_AGENT):
    session = schema.SESSION()
    result = session.query(schema.USERS).filter_by(IP=IP, USER_AGENT=USER_AGENT).count() > 0
    session.close()
    return result

def insertResponse(userid, response):
    for questionid,score in enumerate(response):
        get_or_create(schema.VOTES, USER=userid, QUESTION=questionid, SCORE=score)


def GetVotesCount():
    session = schema.SESSION()
    result = session.query(schema.USERS).count()
    session.close()
    return result

#init table
for item in open(os.path.join(CURRENT_PATH, 'questions.txt')).readlines():
    get_or_create(schema.QUESTIONS, QUESTION=item.strip())

def getScores():
    result = {}
    for id, item in enumerate(getQuestions()):
        try: result[item] += getScore(id)
        except KeyError: result[item] = getScore(id)
    return result

if __name__ == '__main__':
    print(getQuestions())
    print(GetVotesCount())
    print(getScores())
