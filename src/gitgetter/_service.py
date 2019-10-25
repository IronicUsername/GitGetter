from flask import Flask
from typing import Any, Dict

from gitgetter.api import repo_downwards, user_active

app = Flask(__name__)


@app.route('/active/<user>', methods=['GET'])
def get_user_active(user: str) -> Dict[str, Any]:
    """Call '/active/' endpoint."""
    return user_active(user)


@app.route('/downwards/<user>/<repo>', methods=['GET'])
def get_downwards(user: str, repo: str) -> Dict[str, Any]:
    """Call 'downwards' endpoint."""
    return repo_downwards(user, repo)


def build() -> None:
    """Build app."""
    app.run(host='0.0.0.0', debug=True)
