from os import environ
from typing import Any, Dict

from flask import Flask

from gitgetter.api import repo_downwards, repo_downwards1, user_active

app = Flask(__name__)
set_debug = environ.get('GG_SERVICE_DEBUG', True)


@app.route('/active/<user>', methods=['GET'])
def get_user_active(user: str) -> Dict[str, Any]:
    """Call '/active/' endpoint."""
    return user_active(user)


@app.route('/downwards/<user>/<repo>', methods=['GET'])
def get_downwards(user: str, repo: str) -> Dict[str, Any]:
    """Call 'downwards' endpoint."""
    return repo_downwards(user, repo)


@app.route('/downwards1/<repo>', methods=['GET'])
def get_downwards1(repo: str) -> Dict[str, Any]:
    """Call 'downwards1' endpoint."""
    return repo_downwards1(repo)


@app.route('/')
def base_dir() -> str:
    return 'hi.'


def build() -> None:
    """Build app."""
    app.run(host='0.0.0.0', port='5000', debug=set_debug)
