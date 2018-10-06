from flask_restful import Resource, reqparse


class SendMessageView(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('messageId', type=str)
        args = self.parser.parse_args()
        return args, 201
