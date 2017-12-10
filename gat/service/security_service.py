from gat.dao import database
import os
from gat.service import io_service


def login(email, password, case_num):
    result = database.execute(
        "SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}' AND PASSWORD_HASH = crypt('{1}', PASSWORD_HASH) AND CONFIRMED = TRUE;".format(
            email, password), True)
    answer = result is not None and len(result) == 1

    if answer:
        uidpk_result = database.execute("SELECT MAX(UIDPK) FROM T_SESSION;", True)
        uidpk = int(uidpk_result[0][0]) + 1 if uidpk_result[0][0] is not None else 1
        database.execute(
            "INSERT INTO T_SESSION (UIDPK, CASE_NUM, EMAIL) VALUES ({0},'{1}','{2}');"
                .format(uidpk, case_num, result[0][1]), False)
        #io_service.loadDict(email, case_num)
    return answer


def register(email, password, confirmation_code):
    result = database.execute("SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}';".format(email), True)
    if result is not None and len(result) > 0:
        return False
    result = database.execute("SELECT MAX(UIDPK) FROM T_ACCOUNT;", True)
    uidpk = int(result[0][0]) + 1 if result[0][0] is not None else 1
    database.execute(
        "INSERT INTO T_ACCOUNT (UIDPK, EMAIL, PASSWORD_HASH, CONFIRMED, CONFIRMATION_STRING) VALUES ({0}, '{1}', crypt('{2}', gen_salt('bf', 8)), FALSE, '{3}');"
            .format(uidpk, email, password, confirmation_code), False)
    return True


def confirm(code):
    result = database.execute(
        "SELECT * FROM T_ACCOUNT WHERE CONFIRMATION_STRING = '{0}' AND CONFIRMED = FALSE;".format(code), True)
    if result is not None and len(result) < 1:
        return False
    database.execute("UPDATE T_ACCOUNT SET CONFIRMED = TRUE WHERE CONFIRMATION_STRING = '{0}';".format(code), False)
    return True


def createDirectory(uidpk):
    uidpk = str(uidpk[0])
    if not os.path.exists('data/' + uidpk):
        os.makedirs('data/' + uidpk)
def addCaseFolder(case_name, uidpk):
    uidpk = str(uidpk)
    if not os.path.exists('data/' + uidpk + '/' + case_name):
        os.makedirs('data/' + uidpk + '/' + case_name)

def getData(email):
    return database.execute("SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}';".format(email), True)


def getEmail(case_num):
    result = None
    if case_num is not None:
        result = database.execute("SELECT * FROM T_SESSION WHERE CASE_NUM = {0};".format(case_num), True)
    return result[0][2] if (result is not None and len(result) > 0) else None

def isLoggedIn(case_num):
    login = database.execute("SELECT * FROM T_SESSION WHERE CASE_NUM = {0}".format(case_num), True)
    return login is not None


def logout(case_num):
    # session id = case number
    email = getEmail(case_num)
    io_service.saveDict(email, case_num)
    database.execute("DELETE FROM T_SESSION WHERE CASE_NUM = {0};".format(case_num), False)

    # todo remove row with corresponding case number from t_session
    # todo save filedict to users directory
    pass
