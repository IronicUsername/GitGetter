from .api import repo_downwards, user_active
from flask import Flask

app = Flask(__name__)


@app.route('/active/')
@app.route('/active/<username>', methods=['GET'])
def get_user_active(user: str):
    return user_active(user)


@app.route('/downwards/')
@app.route('/downwards/<reop>', methods=['GET'])
def get_downwards(repo: str):
    return repo_downwards(repo)


def build():
    app.run()
