import requests
import json
import os
import datetime
from typing import Any, Dict, Optional

API_URL = 'https://api.github.com'

API_TOKEN = os.environ['GITHUB_TOKEN']
USR = 'IronicUsername'
REPO = 'gitgetter'

ACTIVE_USER_TRANGE = datetime.datetime.now() - datetime.timedelta(days=1)
DOWNWARDS_TRANGE = datetime.datetime.now() - datetime.timedelta(days=7)


def _api_call(url: str, user: str, extend_url: str = '') -> Optional[requests.models.Response]:
    return requests.get(url + user + extend_url, headers={'Authorization': API_TOKEN}) if _user_exist else None


def _user_exist(user: str) -> bool:
    re = requests.get(API_URL + '/search/' + 'users?q=' + user, headers={'Authorization': API_TOKEN})
    if json.loads(re.content).get('total_count') == 0:
        return False
    return True


def _get_user_data(user: str) -> Dict[str, Dict[str, Any]]:
    user_repos = {'repos': []}
    data = json.loads(_api_call(API_URL + '/users/', user, '/repos').text)
    for repo in data:
        user_repos['repos'].append({'name': repo['name'], 'last_modified': repo['updated_at']})
    return user_repos


def _check_within_time(deadline: datetime.datetime, last_updated: datetime.datetime) -> bool:
    if deadline.replace(microsecond=0) <= last_updated <= datetime.datetime.now().replace(microsecond=0):
        return True
    return False


def repo_downwards(repositorie: str) -> Dict[str, bool]:
    re = {'downwards': False}
    data = json.loads(_api_call(API_URL + '/search/repositories?q=', repositorie).text)
    for repo in data['items']:
        repo_nfo = json.loads(_api_call(API_URL + '/repos/', repo['owner']['login'], '/' + repo['name'] + '/stats/code_frequency').text)
        for nfo in repo_nfo:
            # print(nfo)
            if nfo[1] and nfo[2] != 0:
                repo_nfo_time = datetime.datetime.fromtimestamp(nfo[0])
                if _check_within_time(DOWNWARDS_TRANGE, repo_nfo_time) and nfo[2] < nfo[1]:
                    re = {'downwards': False}
    return re

        # repo_stat['repos'].append({
        #     'owner': repo['owner']['login'],
        #     'repo_stats': repo_nfo_time if _check_within_time(DOWNWARDS_TRANGE, repo_nfo_time) else None
        # })
    # print(repo_stat['repos'])
    # print(repo_stat)
    # for repo in data['repos']:
    #     last_updated = datetime.datetime.strptime(repo['last_modified'], "%Y-%m-%dT%H:%M:%SZ")
    #     if _check_within_time(DOWNWARDS_TRANGE, last_updated):
    #         repo_stat['repos'].append({
    #             'name': repo['name'],
    #             'stats': json.loads(_api_call(SEARCH_URL + 'users?q=', repo, '/' + repo['name'] + '/stats/code_frequency').text)
    #         })
    #         # repo_stat[repo['name']] = json.loads(_api_call(REPO_URL, user, '/' + repo['name'] + '/stats/code_frequency').text)
    #         print(repo_stat)
    #         print('-----------------------')

print(repo_downwards(REPO))
