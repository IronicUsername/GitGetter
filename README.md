# GitGetter

Small little service that lets you stalk other people on Github.

## Installation
Download GitGetter:
```
git clone https://github.com/IronicUsername/gitgetter.git
```

After that you should create a `myenv.sh` for your personal Github token.
```
export GITHUB_TOKEN="<YOUR-TOKEN>"
```
and than you `source myenv.sh` it in your terminal.

<b>You dont have to do this step, altho I recomend it.</b>
Github only gives you 60 API calls the hour, without your API token.


## Getting Started
1. [Install poetry](https://poetry.eustace.io/docs/#installation). After the installation, you have to install the dependencies into the virtual environment with `poetry install`.
2. Enter the virtual environment with `poetry shell`.
3. Start the service with `docker-compose up`

That's it.

## Usage
All requests have to be sent at `http://0.0.0.0:5000`.

The service has 3 endpoints:
 - `/active/<user>`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Returns a json `{'was_active': boolean}`. If the user has pushed code within the last 24h it's set to `true`, else `false`
 - `/downwards/<user>/<repo>`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Returns a json `{'downwards': boolean}`. If more code got deleted from a specific user repo than added, it's set to `true`, else `false`
 - `/downwards1/<repo>`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Returns a json `{'downwards': boolean}`. If more code got deleted from a user repo than added, it's set to `true`, else `false
