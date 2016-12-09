#!/usr/bin/env python

import logging
import os
import urllib
import json

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
        logging.error('received bad request')
        abort(400)
    logging.debug('received POST')
    pr_action = request.json['action']
    logging.debug('action: ' + pr_action)
    assignee = request.json['pull_request']['assignee']
    if not assignee:
        return jsonify('ok: no assignee'), 200
    user_name = assignee['login']
    logging.debug('sending DM to: ' + user_name)
    if pr_action == 'assigned':
        logging.debug('PR was ' + pr_action)
        github_event_handler.handleNeedsReviewEvent(request.json['pull_request'])
    else:
        logging.debug('action not actionable')

    return jsonify('ok'), 200

@app.route('/crbot/api/v1.0/pr_review', methods=['POST'])
def pr_review():
    if not request.json or not 'review' in request.json:
        logging.error('received bad request')
        logging.debug(request)
        abort(400)
    logging.debug('received POST')
    pr_action = request.json['action']
    logging.debug('action: ' + pr_action)
    if pr_action == 'submitted':
        state = request.json['review']['state']
        logging.debug('PR request was submitted with state: ' + state)
        pr_number = request.json['pull_request']['number']
        logging.debug('PR # ' + str(pr_number))
        github_event_handler.handleReviewSubmittedEvent(state, request.json['pull_request'])
    else:
        logging.debug('action not actionable')

    return jsonify('ok'), 200


@app.route('/crbot/api/v1.0/comments_addressed', methods=['POST'])
def comments_addressed():
    # if not request.json or not 'callback_id' in request.json:
    #     logging.error('received bad request')
    # logging.debug(request.json['callback_id'])
        # abort(400)
    logging.debug('received comments addressed')
    
    request.get_data()
    data = request.data
    unquoted_data = urllib.unquote(data)[8:]
    payload = json.loads(unquoted_data)
    logging.debug(payload)

    if payload['callback_id'] == 'comments_addressed':
        if payload['actions']['value'] == updated:
            github_event_handler.handleCommentsAddressedEvent(payload['original_message'])
    
    message = {
        "response_type": "ephemeral",
        "replace_original": "false",
        "text": ":white_check_mark: We've let them know that your PR is ready for another look!"
    }
    return jsonify(message), 200


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

    
    port = os.getenv('PORT', 5000)
    logging.info('PORT=' + str(port))

    app.run(debug=True, port=int(port))
