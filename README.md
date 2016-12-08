code-review-bot
=============

## Overview
A code review bot based on [Beep Boop's](https://beepboophq.com)'s starter bot.

This bot listens for new pull requests that have been assigned to users and alerts the users in Slack.

## Usage

### Run locally
Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

	pip install -r requirements.txt
	export SLACK_TOKEN=<APPS_SLACK_TOKEN>; python ./bot/app.py

Things are looking good if the console prints something like:

	Connected <your bot name> to <your slack team> team at https://<your slack team>.slack.com.

If you want change the logging level, prepend `export LOG_LEVEL=<your level>; ` to the `python ./bot/app.py` command.

### Run locally in Docker
	docker build -t starter-python-bot .
	docker run --rm -it -e SLACK_TOKEN=<YOUR SLACK API TOKEN> starter-python-bot

### Run in BeepBoop
If you have linked your local repo with the Beep Boop service (check [here](https://beepboophq.com/0_o/my-projects)), changes pushed to the remote master branch will automatically deploy.

### First Conversations
When you go through the `Add your App to Slack` flow, you'll setup a new Bot User and give them a handle (like @python-rtmbot).

You'll also need to authenticate with your GitHub account. Info incoming.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
