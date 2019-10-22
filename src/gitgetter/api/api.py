import requests
import json
import os
import datetime
from typing import Any, Dict, List, Optional

API_URL = 'https://api.github.com'
API_TOKEN = os.environ['GITHUB_TOKEN']

ACTIVE_USER_TRANGE = datetime.datetime.now() - datetime.timedelta(days=1)
DOWNWARDS_TRANGE = datetime.datetime.today() - datetime.timedelta(days=7)


def _api_call(url: str, user: str, extend_url: str = '') -> Optional[requests.models.Response]:
    """Call Github API.

    Parameters
    ----------
    url: str
        API URL to call.
    user: str
        Username from requested user.
    extend_url: str = ''
        URL extension if needed.

    Returns
    -------
    requests.models.Response
        'requests' Response.
    """
    return requests.get(url + user + extend_url, headers={'Authorization': API_TOKEN})


def _user_repo_exist(use_case: str, item: str) -> bool:
    """Check if user or repo exists.

    Parameters
    ----------
    use_case: str
        Usecase for what the call should happen.
    item: str
        User or repo name from requested usecase.

    Returns
    -------
    bool: bool
        'true' if user/repo does exist, otherwise 'false'.
    """
    re = _api_call(API_URL + '/search/' + use_case + '?q=', item)
    if json.loads(re.content).get('total_count') > 0:
        return True
    return False


def _get_user_data(user: str) -> Dict[str, List[Any]]:   # TODO refactor
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
    user_repos: Dict[str, List] = {'repos': []}
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
    last_updated: datetime.datetime
        Github-user push/repo last touched.

    Returns
    -------
    bool: bool
        'True if push/repo is within timeframe, else 'False'.
    """
    if ACTIVE_USER_TRANGE.replace(microsecond=0) <= last_updated <= datetime.datetime.now().replace(microsecond=0):
        return True
    return False


def _check_downwards(repo_stats: List[int]) -> bool:
    """Check if repo is going downwards.

    Parameters
    ----------
    repo_stats: List[int, int, int]
        Github repo stats.

    Returns
    -------
    bool: bool
        Set to 'true' if repo is going downwards, else 'false'.
    """
    for nfo in repo_stats:
        if nfo[1] != 0 and nfo[2] != 0:
            repo_nfo_time = datetime.datetime.fromtimestamp(nfo[0])
            if _check_within_time(DOWNWARDS_TRANGE, repo_nfo_time) and nfo[2] > nfo[1]:
                return True
    return False


def _error_msg(use_case: str = 'Either repo or user') -> Dict[str, str]:
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


def user_active(user: str) -> Dict[str, Any]:
    """Get last modified repo from user within 24h.

    Parameters
    ----------
    user: str
        Github-username from requested user.

    Returns
    -------
    re: Dict[str, Any]
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


def repo_downwards(user: str, repositorie: str) -> Dict[str, Any]:
    """If the specified git repo had more deletions than additions in the last 7 days.

    Parameters
    ----------
    user: str
        Github-username from requested user.
    repo: str
        Github-repo from requested user.

    Returns
    -------
    re: Dict[str, Any]
        Dict 'downwards' with bool value.
        Set to 'true' if repo had more deletions than additions within the last 7 days otherwise 'false'.
    """
    re = {'downwards': False}
    if _user_repo_exist('repositories', repositorie) and _user_repo_exist('users', user):
        repo_nfo = json.loads(_api_call(API_URL + '/repos/', user, '/' + repositorie + '/stats/code_frequency').text)
        if _check_downwards(repo_nfo):
            re = {'downwards': False}
    else:
        return _error_msg()
    return re


def repo_downwards1(repositorie: str) -> Dict[str, Any]:
    """Return same thing as 'repo_downwards' but here all every repo gets checked.

    Can empty the limited API calls from Github.

    Parameters
    ----------
    repo: str
        Github-repo from requested user.

    Returns
    -------
    re: Dict[str, Any]
        Dict 'downwards' with bool value.
        Set to 'true' if repo had more deletions than additions within the last 7 days otherwise 'false'.
    """
    re = {'downwards': False}
    if _user_repo_exist('repositories', repositorie):
        data = json.loads(_api_call(API_URL + '/search/repositories?q=', repositorie).text)
        for repo in data['items']:
            repo_nfo = json.loads(_api_call(API_URL + '/repos/', repo['owner']['login'], '/' + repo['name'] + '/stats/code_frequency').text)
            if _check_downwards(repo_nfo):
                re = {'downwards': False}
    else:
        return _error_msg(repositorie)
    return re
