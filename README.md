# GitGetter
small little service that lets you stalk other people on GitHub.


## environment parameters
* `GG_GITHUB_TOKEN`: your GitHub token. if you run GitGetter with it, you have more calls to the API. you can get the token [here](https://github.com/settings/tokens/new).
* `GG_SERVICE_PORT`: the port on which the service is callable. by default the port is set to 5000.
* `GG_SERVICE_DEBUG`: debug mode is by default `True`. pass `False` in this environment variable to change it.


## install & run
download it:
```bash
git clone https://github.com/IronicUsername/GitGetter.git
```
and run it:
```bash
docker-compose up --force-recreate --build -d
```


## development
in order to develop on GitGetter you need to have [poetry](https://poetry.eustace.io/docs/#installation) installed.
after you have done that, install all dependencies
```bash
poetry install
```
and access the virtual environment
```bash
poetry shell
```


## local testing
lint the code with
```bash
flake8 . && mypy src/ && pydocstyle src/
```
and test it with
```bash
pytest -n 4 -x # -n for 4 parallel jobs & -x to stop on the first encountered error
```


## endpoints
```http
GET /active/IronicUsername
```
| parameter | type | description |
| :--- | :--- | :--- |
| `user` | `string` | **required**. the username of the person you stalking. |


### response
if the user has pushed code within the last 24h it's set to `true`, else `false`.
```javascript
{
    "was_active": bool
}

```
---
```http
GET /downwards/IronicUsername/GitGetter
```
| parameter | type | description |
| :--- | :--- | :--- |
| `user` | `string` | **required**. the username of the person you stalking. |
| `repo` | `string` | **required**. the GitHub repository in question. |

### response
if more code got deleted from a specific user repo than added, it's set to `true`, else `false`.
```javascript
{
    "downwards": bool
}
```
---
```http
GET /downwards1/GitGetter
```
| parameter | type | description |
| :--- | :--- | :--- |
| `repo` | `string` | **required**. the GitHub repository in question. |

### response
if more code got deleted from a user repo than added, it's set to `true`, else `false`.
```javascript
{
    "downwards": bool
}
```
