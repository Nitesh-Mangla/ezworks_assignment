import datetime
from flask import request
from Models.UserModel import User as UserModel
import os
import pathlib
from Helpers import hepler
from core.Event import Event
from core.Listener import Listener
import uuid
import urllib.parse
from core import app
from werkzeug.utils import secure_filename

class User:

    def __init__(self):
        self.userModel = UserModel()

    def userAuthentication(self):
        requestParams = request.form.to_dict()

        if 'email_id' not in requestParams:
            raise Exception("Email id is required")
        elif 'password' not in requestParams:
            raise Exception("password is required")

        result = self.userModel.getUserProfile(
            type='email_id',
            emailId=requestParams['email_id'],
            password=requestParams['password'],
            columns='*',
            isJson=True
        )

        if result == ():
            raise Exception("User doesn't exits")

        if result[0]['is_email_verified'] != 1 and result[0]['is_phone_no_verified'] != 1:
            raise Exception("Please verified your email to login")

        return result[0]

    def uploadFiles(self):
        fileitem = request.files['filename']

        if fileitem.filename:
            # strip the leading path from the file name
            fn = os.path.basename(fileitem.filename)
            file_extension = pathlib.Path(fn).suffix
            if file_extension not in ['.pptx', '.docx', '.xlsx']:
                raise Exception("File type is not allowed")

            filename = secure_filename(fileitem.name+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+file_extension)
            fileitem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = self.userModel.saveUploadfile(filename, app.config['UPLOAD_FOLDER'])
            return result
        else:
           raise Exception("Please Upload file")

    def registration(self):
        if request is None:
            raise Exception("Required params are missing")
        elif request.method != "POST":
            raise Exception("Invalid Request")

        formData = self.formValidation()

        formData['is_email_verified'] = False
        formData['is_phone_no_verified'] = False
        formData['ip'] = request.remote_addr

        insertedData = self.userModel.insertUser(formData=formData)
        uid = uuid.uuid4()

        encMessage = hepler.encryptionData(str(insertedData[0]['id'])+ "-" + uid.hex)
        verifyLink = request.host_url + "/verify-email?token={}".format(urllib.parse.quote(encMessage))

        if insertedData:
            Event.getInstance().fire(
                eventFunction=Listener.sendEmail,
                eventData={
                    'receipt_email_id': formData['email_id'],
                    'message': "Hey Hi {} <br> Please verify you email id <br> "
                               "<a href='{}'>Verify</a>".format(formData['fname'] + " " + formData['lname'], verifyLink)
                }
            )
            return insertedData

        raise Exception("Registration Failed")

    def formValidation(self):
        formData = request.form.to_dict()
        params = ['fname', 'lname', 'email_id', 'phone_no', 'dob', 'gender']
        format = "%d-%m-%Y"

        if formData == {}:
            raise Exception("Required params are missing")

        for key in params:
            if key not in formData:
                raise Exception(key + " is required")
            elif formData[key] == "":
                raise Exception(key + " value is missing")
            elif key == 'phone_no' and len(formData[key]) > 10:
                raise Exception("Phone no can't be greater than 10")
            elif key == 'email_id' and not hepler.validateEmailId(formData['email_id']):
                raise Exception("Invalid email")

        datetime.datetime.strptime(formData['dob'], format)

        if self.userModel.isEmailIdExist(formData['email_id']):
            raise Exception("Email id is already exist! Please different email id")

        if self.userModel.isPhoneNoExist(formData['phone_no']):
            raise Exception("Phone no is already exist! Please different PHone no")

        return formData

    def userVerified(self):
        token = request.args.get('token')
        if token == "":
            raise Exception("Invalid User")

        message = hepler.decryptData(urllib.parse.unquote(token)).split("-")
        userId = int(message[0])

        userDetails = self.userModel.getById(userId, isJson=True)
        if userDetails == ():
            raise Exception("Invalid User")
        elif userDetails[0]['is_email_verified'] == 1:
            raise Exception("User has been already verified")

        self.userModel.varifyPhoneNoOrEmailId(
            type="is_email_verified",
            userId=userId
        )

        return {
            'message': "Email successfully verified"
        }

    def getDownloadEncodeUrl(self, id):
        mediaDetails = self.userModel.getMediaById(id, True)

        if mediaDetails == ():
            raise Exception("Data not found")

        return urllib.parse.quote(mediaDetails[0]['path']+"/"+mediaDetails[0]['name'])

    def getFileList(self):
        mediaList = self.userModel.getMediaList(True)
        if mediaList == ():
            raise Exception("Data not found")

        return mediaList
