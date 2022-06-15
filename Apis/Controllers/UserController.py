from core.BaseController import Base
from core import app
from Repositories.UserRepository import User
from core import Constants


class UserController(Base):

    def __init__(self):
        super().__init__(app)
        self.user = User()

    def userLogin(self):
        try:
            userDetails = self.user.userAuthentication()
            if userDetails == {}:
                return Base.response({"error_message": "{}".format(Constants.LOGIN_FAILED)})

            token = Base.generateJwtToken(
                self,
                userId=userDetails['id'],
                role=userDetails['user_type']
            )

            result = {}
            result.update({
                'message': Constants.LOGINED_IN,
                'user_details': userDetails,
                'token': token
            })

            return Base.response(result)
        except Exception as error:
            return Base.response({'error_message': "{}".format(error)})

    def uploadDcos(self):
        try:
            isAuth = Base.auth(self)
            if 'user_id' not in isAuth or 'user_id' in isAuth and isAuth['user_id'] == "":
                raise Exception(isAuth)

            result = self.user.uploadFiles()
            return Base.response({
                'message': 'file uploaded successfully',
                'data': result
            })
        except Exception as error:
            return Base.response({'error_message': "{}".format(error)})

    def registration(self):
        try:
            insertedData = self.user.registration()
            return Base.response(
                {
                    "message": "User is created successfully",
                    'user_details': insertedData
                }
            )
        except Exception as error:
            return Base.response({"error_message": "{}".format(error)})

    def verifyUser(self):
        try:
            result = self.user.userVerified()
            return Base.response(result)
        except Exception as error:
            return Base.response({'error_message': "{}".format(error)})

    def downloadLink(self, id):
        try:
            userDetails = Base.auth(self)
            if 'user_id' not in userDetails and 'role' not in userDetails['role']:
                raise Exception(Constants.UNAUTHORIZED)
            elif userDetails['role'] != 'client':
                raise Exception("You are not allowed to access")

            url = self.user.getDownloadEncodeUrl(id)
            return Base.response({
                'message': "Success",
                'download-link': url
            })
        except Exception as error:
            return Base.response({'error_message': "{}".format(error)})

    def listAllFile(self):
        try:
            userDetails = Base.auth(self)
            if 'user_id' not in userDetails and 'role' not in userDetails['role']:
                raise Exception(Constants.UNAUTHORIZED)
            elif userDetails['role'] != 'client':
                raise Exception("You are not allowed to access")

            url = self.user.getFileList()
            return Base.response({
                'message': "Success",
                'data': url
            })
        except Exception as error:
            return Base.response({'error_message': "{}".format(error)})
