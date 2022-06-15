from core import app
import re
import smtplib
import cryptocode

def createModelResponseMapping(cursor, result):
    field_names = [i[0] for i in cursor.description]
    json_data = []
    for result in result:
        json_data.append(dict(zip(field_names, result)))

    return json_data


def validateEmailId(emailId):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if emailId == "":
        raise Exception("Email id missing")

    if (re.search(regex, emailId)):
        return True

    return False


def sendEmail(receiptEmailId, message):
    # Create your SMTP session
    smtp = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])

    # Use TLS to add security
    smtp.starttls()

    # User Authentication
    smtp.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    # Sending the Email
    smtp.sendmail(app.config['MAIL_USERNAME'], receiptEmailId, message)

def encryptionData(data):
    key = 'This_key_for_demo_purposes_only='
    return cryptocode.encrypt(data,key)

def decryptData(data):
    key = 'This_key_for_demo_purposes_only='
    return cryptocode.decrypt(data, key)

