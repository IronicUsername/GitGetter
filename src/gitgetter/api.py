import requests
import json
import os
import datetime
from .service import
from typing import Any, Dict

USER_URL = 'https://api.github.com/users/'
REPO_URL = 'https://api.github.com/repos/'
API_TOKEN = os.environ['GITHUB_TOKEN']
USER =
ACTIVE_USER_TRANGE = datetime.datetime.today() - datetime.timedelta(days=1)
DOWNWARDS_TRANGE = datetime.datetime.today() - datetime.timedelta(days=7)


def _api_call(
              url: str,
              user: str,
              git_token: str,
              extend_url: str = ''
            ) -> requests.models.Response:
    return requests.get(url + user + extend_url,
                        headers={'Authorization': git_token})


def _get_user_data(user: str) -> Dict[str, Dict[str, Any]]:
    user_repos = {'repos': []}
    data = json.loads(_api_call(USER_URL, user, API_TOKEN, '/repos').text)
    for repo in data:
        user_repos['repos'].append({
          'name': repo['name'],
          'last_modified': repo['updated_at']
        })
    return user_repos


def user_active(user: str, t_range: datetime = ACTIVE_USER_TRANGE) -> Dict[str, bool]:
    response = {'was_active': False}
    data = _get_user_data(user)
    for repo in data['repos']:
        last_updated = datetime.datetime.strptime(
            repo['last_modified'],
            "%Y-%m-%dT%H:%M:%SZ"
        )
        if last_updated > t_range:
            response['was_active'] = True
    return response


def repo_downwards(reop: str, t_range: datetime = DOWNWARDS_TRANGE) -> Dict[str, bool]:
    response = {'downwards': False}
    data = _get_user_data(reop)
    repo_stat = {}
    for repo in data['repos']:
        last_updated = datetime.datetime.strptime(repo['last_modified'],
                                                  "%Y-%m-%dT%H:%M:%SZ")
        if last_updated > t_range:
            repo_stat[repo['name']] = _api_call(
                REPO_URL, USER, API_TOKEN,
                '/' + repo['name'] + '/stats/code_frequency').text
    print(repo_stat)
    return response
