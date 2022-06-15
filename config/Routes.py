from flask import jsonify
from core import app
from Apis.Controllers import UserController as User

@app.errorhandler(404)
def pageNotFound(error):
    return jsonify(
        status=404,
        data={"error_message": "Page not found"}
    ), 404


login = User.UserController()
app.add_url_rule('/login', view_func=login.userLogin, methods=['post'])
app.add_url_rule('/verify-email', view_func=login.verifyUser, methods=['post'])
app.add_url_rule('/registration', view_func=login.registration, methods=['post'])
app.add_url_rule('/upload-doc', view_func=login.uploadDcos, methods=['post'])
app.add_url_rule('/download-file/<id>', view_func=login.downloadLink, methods=['get'])
app.add_url_rule('/file-list', view_func=login.listAllFile, methods=['get'])
