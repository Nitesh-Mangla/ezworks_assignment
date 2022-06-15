import json
from flask import request, Response, g
from flask import jsonify
from core import Constants
import jwt
import datetime


class Base:

    def __init__(self, app):
        self.app = app

    def auth(self):
        try:
            header = request.headers
            global secretKey
            secretKey = self.app.config['SECRET_KEY']

            header = self.allowedHeaders(
                headers=header
            )

            self.validateToken(
                headers=header
            )

            return {"user_id": g.user_id,'role': g.role}
        except Exception as error:
            return ("{}".format(str(error)))

    @staticmethod
    def response(attributes):

        if not attributes:
            return jsonify(
                status=200,
                data={'message': Constants.NOT_FOUND}
            )

        if 'error_message' in attributes and Constants.UNAUTHORIZED == attributes['error_message']:
            return Response(
                json.dumps({'data': attributes, 'status': 401}),
                status=401,
                mimetype='application/json'
            )
        elif 'error_message' in attributes:
            return Response(
                json.dumps({'data': attributes, 'status': 400}),
                status=400,
                mimetype='application/json'
            )

        return jsonify(
            status=200,
            data=attributes
        ), 200

    def validateToken(self, headers):
        if Constants.ACCESS_TOKEN not in headers:
            raise Exception("access token is required")

        accessToken = headers.get(Constants.ACCESS_TOKEN, None)
        date = datetime.datetime.now()
        currentTime = int(date.timestamp() * 1000)

        if accessToken is None:
            raise Exception("Token is missing")
        else:
            tokenData = jwt.decode(accessToken, secretKey)
            if tokenData['role'] == 'guest':
                raise Exception(Constants.UNAUTHORIZED)
            else:
                expireTime = tokenData['expire-time']
                if currentTime > expireTime:
                    raise Exception("Invalid Token")
                else:
                    g.user_id = tokenData['user_id']
                    g.role = tokenData['role']

    def generateJwtToken(self, userId="", role="ops"):

        try:
            date = datetime.datetime.now() + datetime.timedelta(days=30)
            currentTime = int(date.timestamp() * 1000)
            secretKey = self.app.config['SECRET_KEY']

            if userId == "":
                jwtToken = jwt.encode({
                    'role': 'guest',
                    'created-at': int(datetime.datetime.now().timestamp() * 1000),
                    'expire-time': currentTime
                }, secretKey)
            else:
                jwtToken = jwt.encode({
                    'user_id': userId,
                    'role': role,
                    'created-at': int(datetime.datetime.now().timestamp() * 1000),
                    'expire-time': currentTime
                }, secretKey)

            return jwtToken.decode('UTF-8')
        except Exception as error:
            return "{}".format(error)

    def allowedHeaders(self, headers):
        allowedHeaders = [
            "content-type", "access-token"
        ]
        result = {}

        for key, value in headers:
            if key.lower() in allowedHeaders:
                result.update({
                    key.lower(): value
                })

        return result
