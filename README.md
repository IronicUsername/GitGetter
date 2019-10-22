# GitGetter

Small little service that lets you stalk other people on Github.

## First Things First
Download GitGetter:
```
git clone https://github.com/IronicUsername/GitGetter.git
```

After that you should create a `myenv.sh` for your personal Github token (which you can get [here](https://github.com/settings/tokens/new))
```
export GITHUB_TOKEN="<YOUR-TOKEN>"
```
and than you `source myenv.sh` it in your terminal.

<b>This step is important.</b>

<br>

## Start it
1. [Install poetry](https://poetry.eustace.io/docs/#installation). After the installation, you have to install the dependencies into the virtual environment with `poetry install`.
2. Enter the virtual environment with `poetry shell`.
3. Start the service with `docker-compose up`

That's it.

## Usage
All requests have to be sent at `http://0.0.0.0:5000`.

The service has 3 endpoints:
 - [`GET`] `/active/<user>` Returns a json `{'was_active': boolean}`. If the user has pushed code within the last 24h it's set to `true`, else `false`
 - [`GET`] `/downwards/<user>/<repo>` Returns a json `{'downwards': boolean}`. If more code got deleted from a specific user repo than added, it's set to `true`, else `false`
 - [`GET`] `/downwards1/<repo>` Returns a json `{'downwards': boolean}`. If more code got deleted from a user repo than added, it's set to `true`, else `false
