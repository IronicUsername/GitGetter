import requests
import json
import os
import datetime
from typing import Any, Dict, Optional

API_URL = 'https://api.github.com'
API_TOKEN = os.environ['GITHUB_TOKEN']

ACTIVE_USER_TRANGE = datetime.datetime.now() - datetime.timedelta(days=1)
DOWNWARDS_TRANGE = datetime.datetime.today() - datetime.timedelta(days=7)


def _api_call(url: str, user: str, extend_url: str = '') -> Optional[requests.models.Response]:
    """Call Github API.

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


def _user_repo_exist(use_case: str, user: str) -> bool:
    """Check if user exists or repo.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    bool
        'true' if user exist, otherwise 'false'.
    """
    re = _api_call(API_URL + f'/search/{use_case}?q=', user)
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
    data = json.loads(_api_call(API_URL + '/users/', user, '/repos').text)
    for repo in data:
        user_repos['repos'].append({'name': repo['name'], 'last_modified': repo['updated_at']})
    return user_repos


def _check_within_time(deadline: datetime.datetime, last_updated: datetime.datetime) -> bool:
    """Check if stuff is within a certain time.

    Parameters
    ----------
    deadline: datetime.datetime
        End time of the timeframe.
    last_updated: str
        Github-user push/repo last touched.

    Returns
    -------
    bool: bool
        'True if push/repo is within timeframe, else 'False'.
    """
    if ACTIVE_USER_TRANGE.replace(microsecond=0) <= last_updated <= datetime.datetime.now().replace(microsecond=0):
        return True
    return False


def _error_msg(use_case: str) -> Dict[str, str]:
    """Give back faild request.

    Parameters
    ----------
    use_case: str
        Usecase for what the error message is.

    Returns
    -------
    dict: Dict[str, bool]
        Dict 'error' with string value.
    """
    return {'error': f'{use_case} does not exist'}


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
    if _user_repo_exist('users', user):
        data = _get_user_data(user)
        for repo in data['repos']:
            last_updated = datetime.datetime.strptime(repo['last_modified'], "%Y-%m-%dT%H:%M:%SZ")
            if _check_within_time(ACTIVE_USER_TRANGE, last_updated):
                re['was_active'] = True
                break
    else:
        return _error_msg(user)
    return re


def repo_downwards1(repositorie: str) -> Dict[str, bool]:
    """If the specified git repo had more deletions than additions in the last 7 days.

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
    if _user_repo_exist('repos', repositorie):
        data = json.loads(_api_call(API_URL + '/search/repositories?q=', repositorie).text)
        for repo in data['items']:
            repo_nfo = json.loads(_api_call(API_URL + '/repos/', repo['owner']['login'], '/' + repo['name'] + '/stats/code_frequency').text)
            for nfo in repo_nfo:
                if nfo[1] and nfo[2] != 0:
                    repo_nfo_time = datetime.datetime.fromtimestamp(nfo[0])
                    if _check_within_time(DOWNWARDS_TRANGE, repo_nfo_time) and nfo[2] < nfo[1]:
                        re = {'downwards': False}
    else:
        return _error_msg(repositorie)
    return re
