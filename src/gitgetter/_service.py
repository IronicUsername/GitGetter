from gitgetter.api import repo_downwards1, user_active   # noqa: D100
from flask import Flask

app = Flask(__name__)


# @app.route('/active/')
@app.route('/active/<user>', methods=['GET'])
def get_user_active(user: str):
    """Call endpoint."""
    return user_active(user)


# @app.route('/downwards/')
# @app.route('/downwards/<repo>', methods=['GET'])
# def get_downwards(repo: str):
#     return repo_downwards(repo)


@app.route('/downwards1/<repo>', methods=['GET'])
def get_downwards1(repo: str):
    """Call endpoint."""
    return repo_downwards1(repo)


def build():
    """Build app."""
    app.run()
