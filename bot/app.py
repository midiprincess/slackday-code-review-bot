#!/usr/bin/env python

import logging
import os

from beepboop import resourcer
from beepboop import bot_manager

from slack_bot import SlackBot
from slack_bot import spawn_bot

from slacker import Slacker
from messenger import Messenger
from github_event_handler import GitHubEventHandler

from flask import Flask, request, jsonify, abort

logger = logging.getLogger(__name__)

slack_token = os.getenv("SLACK_TOKEN", "")

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/crbot/api/v1.0/pr', methods=['POST'])
def pull_request():
    if not request.json or not 'pull_request' in request.json:
        logging.error('recieved bad request')
        abort(400)
    logging.debug('Received POST')
    pr_action = request.json['action']
    logging.debug('action: ' + pr_action)
    assignee = request.json['pull_request']['assignee']['login']
    logging.debug('sending DM to: ' + assignee)
    if pr_action in ['assigned', 'unassigned', 'closed']:
        logging.debug('PR was ' + pr_action)
        github_event_handler.handleNeedsReviewEvent(request.json['pull_request'])
    else:
        logging.debug('action not actionable')

    return jsonify('ok'), 200


if __name__ == "__main__":

    global msg_writer
    global event_handler
    global github_event_handler
    global slack

    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    logging.info("token: {}".format(slack_token))
    if slack_token == "":
        logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")

    slack = Slacker(slack_token)
    msg_writer = Messenger(slack)
    github_event_handler = GitHubEventHandler(slack, msg_writer)

    app.run(debug=True, port=int(os.getenv('PORT', 5000)))

    # if slack_token == "":
    #     logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")
    #     slack_token = None
    #     botManager = bot_manager.BotManager(spawn_bot)
    #     res = resourcer.Resourcer(botManager)
    #     res.start()
    # else:
    #     # only want to run a single instance of the bot in dev mode
    #     bot = SlackBot(slack_token)
    #     bot.start({})
