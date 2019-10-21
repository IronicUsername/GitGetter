from gitgetter.api import repo_downwards, user_active
from flask import Flask

app = Flask(__name__)


# @app.route('/active/')
@app.route('/active/<user>', methods=['GET'])
def get_user_active(user: str):
    return user_active(user)


# @app.route('/downwards/')
@app.route('/downwards/<user>/<reop>', methods=['GET'])
def get_downwards(user: str, repo: str):
    return repo_downwards(user, repo)


def build():
    app.run()
