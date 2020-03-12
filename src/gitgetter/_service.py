from os import environ

from flask import Flask
from typing import Any, Dict

from gitgetter.api import repo_downwards, repo_downwards1, user_active

app = Flask(__name__)


@app.route('/active/<user>', methods=['GET'])
def get_user_active(user: str) -> Dict[str, Any]:
    """Call '/active/' endpoint."""
    return user_active(user)


@app.route('/downwards/<user>/<repo>', methods=['GET'])
def get_downwards(user: str, repo: str) -> Dict[str, Any]:
    """Call 'downwards' endpoint."""
    return repo_downwards(user, repo)


@app.route('/')
def base_dir() -> str:
    return 'hi.'

def build() -> None:
    """Build app."""
    app.run(host='0.0.0.0', port=environ.get('GG_SERVER_PORT', '5000'), debug=environ.get('GG_SERVER_DEBUG', True))
