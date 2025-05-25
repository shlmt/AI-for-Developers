from flask import Flask
from bson import ObjectId
from routers.students import students_router
from flask.json.provider import DefaultJSONProvider

class CustomJSONEncoder(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(self, obj)


app = Flask(__name__)

app.json = CustomJSONEncoder(app)

app.register_blueprint(students_router, url_prefix='/students')

app.run(port=8080)