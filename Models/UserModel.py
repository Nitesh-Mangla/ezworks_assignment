from config.Database import Connection
from Helpers import hepler


class User:

    def __init__(self):
        self.db = Connection.getDbInstance()
        self.cursor = self.db.cursor()

    def isEmailIdExist(self, emailId):

        sql = "select * from user_profile where email_id = '{}'".format(emailId)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if len(result) > 0:
            return True
        return False

    def isPhoneNoExist(self, phoneNo):

        sql = "select * from user_profile where phone_no = {}".format(phoneNo)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if len(result) > 0:
            return True
        return False

    def varifyPhoneNoOrEmailId(self, type, userId):
        sql = "update user_profile set " + type + " = 1 where id = {}".format(userId)
        self.cursor.execute(sql)
        self.db.commit()
        return "Successfully Verified"

    def insertUser(self, formData):
        fullName = "'" + formData['fname'] + " " + formData['lname'] + "'"

        sql = "insert into user_profile(fname, lname, full_name, dob, phone_no, email_id ,gender, ip,password,user_type) values({},{},{},{},{},{},{},{},{},{})".format(
            "'" + formData['fname'] + "'", "'" + formData['lname'] + "'",
            fullName, "'" + formData['dob'] + "'", formData['phone_no'], "'" + formData['email_id'] + "'",
            "'" + formData['gender'] + "'",
            "'" + formData['ip'] + "'", "'" + formData['password'] + "'", "'" + formData['role'] + "'"
        )

        self.cursor.execute(sql)
        lastInsertId = self.cursor.lastrowid

        self.db.commit()
        if lastInsertId:
            sql = "select * from user_profile where id = {}".format(str(lastInsertId))
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return hepler.createModelResponseMapping(self.cursor, result)

        return False

    def getUserProfile(self, type, emailId, password, columns='*', isJson=False):
        sql = "select " + columns + " from user_profile where {} = {} and password = {} limit 1".format(type,
                                                                                                        "'" + emailId + "'",
                                                                                                        "'" + password + "'")
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if isJson and result != ():
            return hepler.createModelResponseMapping(self.cursor, result)

        return result

    def getById(self, id, isJson=False, columns='*'):
        sql = "select " + columns + " from user_profile where id = {}".format(id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if isJson:
            return hepler.createModelResponseMapping(self.cursor, result)

        return result

    def saveUploadfile(self, filename, path):
        sql = "insert into media(name, path) values({},{})".format(
            "'" + filename + "'", "'" + path + "'"
        )

        self.cursor.execute(sql)
        lastInsertId = self.cursor.lastrowid

        self.db.commit()
        if lastInsertId:
            sql = "select * from media where id = {}".format(str(lastInsertId))
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return hepler.createModelResponseMapping(self.cursor, result)

        return False

    def getMediaById(self, id, isJson=False):
        sql = "select * from media where id = {}".format(id)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        if isJson and result != ():
            return hepler.createModelResponseMapping(self.cursor, result)

        return result

    def getMediaList(self, isJson=False):
        sql = "select * from media "

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        if isJson and result != ():
            return hepler.createModelResponseMapping(self.cursor, result)

        return result
