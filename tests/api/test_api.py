import pytest

from gitgetter.api import user_active, repo_downwards, repo_downwards1


@pytest.mark.parametrize('user,result', [
    ('sdispater', {'was_active': True}),
    ('woksalonica', {'was_active': False}),
    ('oiewruoiwerweoiruower', {'error': 'oiewruoiwerweoiruower does not exist'}),
])
def test_user_active(user, result):
    assert user_active(user) == result


@pytest.mark.parametrize('user,repo,result', [
    ('IronicUsername', 'gitgetter', {'downwards': False}),
    # ('XY', 'xy', {'downwards': True}),   # saddly I couldn't find this case
    ('IronicUsername', 'nothing', {'downwards': False}),
    ('oiewruoiwerweoiruower', 'gitgetter', {'error': 'Either repo or user does not exist'}),
])
def test_repo_downwards(user, repo, result):
    assert repo_downwards(user, repo) == result


@pytest.mark.parametrize('repo,result', [
    ('gitgetter', {'downwards': False}),
    # ('XY', 'xy', {'downwards': True}),   # saddly I couldn't this case
    ('oiewruoiwerweoiruower', {'error': 'oiewruoiwerweoiruower does not exist'}),
])
def test_repo_downwards1(repo, result):
    assert repo_downwards1(repo) == result
