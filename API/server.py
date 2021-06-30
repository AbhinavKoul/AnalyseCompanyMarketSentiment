from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import api

app.add_url_rule('/', view_func=lambda: "Server is up!", methods=["GET"])

app.add_url_rule('/analyseCompany', view_func=api.analyse_company_tweets, methods=["GET"])



if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=4020,
    )