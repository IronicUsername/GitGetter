import requests
import json
import os
import datetime
from typing import Any, Dict, Optional

USER_URL = 'https://api.github.com/users/'
SEARCH_URL = 'https://api.github.com/search/'

API_TOKEN = os.environ['GITHUB_TOKEN']

ACTIVE_USER_TRANGE = datetime.datetime.now() - datetime.timedelta(days=1)
DOWNWARDS_TRANGE = datetime.datetime.today() - datetime.timedelta(days=7)


def _api_call(url: str, user: str, extend_url: str = '') -> Optional[requests.models.Response]:
    """Calls Github API.

    Parameters
    ----------
    url: str
        Github API URL to call.
    user: str
        Github-username from requested user.
    extend_url: str = ''
        Github API URL extension if needed.

    Returns
    -------
    requests.models.Response
        'requests' Response.
    """
    return requests.get(url + user + extend_url, headers={'Authorization': API_TOKEN})


def _user_exist(user: str) -> bool:
    """Checks if user exists.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    bool
        'true' if user exist, otherwise 'false'.
    """
    re = requests.get(SEARCH_URL + 'users?q=' + user, headers={'Authorization': API_TOKEN})
    if json.loads(re.content).get('total_count') > 0:
        return True
    return False


def _get_user_data(user: str) -> Dict[str, Dict[str, Any]]:
    """Get Github userdata.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    user_repos: Dict[str, Dict[str, Any]]
        Dict with all repos 'name' and 'last_modified'.
    """
    user_repos = {'repos': []}
    data = json.loads(_api_call(USER_URL, user, '/repos').text)
    for repo in data:
        user_repos['repos'].append({
          'name': repo['name'],
          'last_modified': repo['updated_at']
        })
    return user_repos


def _check_within_time(deadline: datetime.datetime, last_updated: datetime.datetime) -> bool:
    """Check if re.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    re: Dict[str, bool]
        Dict 'was_active' with bool value.
        Set to 'true' if user pushed within 24h into repo otherwise 'false'.
    """
    if ACTIVE_USER_TRANGE.replace(microsecond=0) <= last_updated <= datetime.datetime.now().replace(microsecond=0):
        return True
    return False


def _error_msg(user: str) -> Dict[str, str]:
    return {'error': f'{user} does not exist'}


def user_active(user: str) -> Dict[str, bool]:
    """Get last modified repo from user within 24h.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    re: Dict[str, bool]
        Dict 'was_active' with bool value.
        Set to 'true' if user pushed within 24h into repo otherwise 'false'.
    """
    re = {'was_active': False}
    if _user_exist(user):
        data = _get_user_data(user)
        for repo in data['repos']:
            last_updated = datetime.datetime.strptime(repo['last_modified'], "%Y-%m-%dT%H:%M:%SZ")
            if _check_within_time(ACTIVE_USER_TRANGE, last_updated):
                re['was_active'] = True
                break
    else:
        return _error_msg(user)
    return re


def repo_downwards(repo: str) -> Dict[str, bool]:
    """ If the specified git repo had more deletions than additions in the last 7 days

    Parameters
    ----------
    user: str
        Github-username from requested user.
    repo: str
        Github-repo from requested user.

    Returns
    -------
    re: Dict[str, bool]
        Dict 'downwards' with bool value.
        Set to 'true' if repo had more deletions than additions within the last 7 days otherwise 'false'.
    """
    re = {'downwards': False}
    data = json.loads(_api_call(SEARCH_URL + 'users?q=', repo).text)
    repo_stat = {}
    for repo in data['repos']:
        last_updated = datetime.datetime.strptime(repo['last_modified'], "%Y-%m-%dT%H:%M:%SZ")
        if _check_within_time(last_updated, DOWNWARDS_TRANGE):
            repo_stat[repo['name']] = _api_call(REPO_URL, user, API_TOKEN, '/' + repo['name'] + '/stats/code_frequency').text


    return re
