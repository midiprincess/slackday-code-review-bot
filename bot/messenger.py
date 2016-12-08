# -*- coding: utf-8 -*-

import logging
import random

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!!!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    ############
    # This function generates the message sent to the Reviewer when the Developer creates a PR or changes it
    #
    # dm_id: the DM the bot is posting in - should be the Reviewer's DM id
    # dev_user_id: this needs to be looked up in our static github -> slack map
    # pr_title: the display title of the pull request 
    # pr_url: the URL to the pull request
    # pr_number: the #12345 number of the pull request
    ############
    def write_needs_review_msg(self, dm_id, dev_user_id, pr_title, pr_url, pr_number):
        message = "New code review request from <@" + dev_user_id + ">"
        description = " <@" + dev_user_id + "> has asked you to review their pull request: *" + pr_title + "* <" + pr_url + "|#" + pr_number + ">. Please take a look when you have time. \n\nWhen you're done reviewing the PR, please be sure to `Submit Review` and select one of `Comment`, `Approve`, or `Request Changes`."

        attachment = {
            "text": description,
            "fallback": message,
            "color": "#000000",
            "attachment_type": "default",
            "mrkdwn_in": ["text"]
        }
        self.clients.web.chat.post_message(dm_id, message, attachments=[attachment], as_user='true')

    ############
    # This function generates the message sent to the Developer after the Reviewer has submitted a review
    #
    # dm_id: the DM the bot is posting in - should be the Developer's DM id
    # reviewer_user_id: this needs to be looked up in our static github -> slack map
    # status: one of 'Approved', 'Request Changes', or 'Comment'
    # pr_title: the display title of the pull request 
    # pr_url: the URL to the pull request
    # pr_number: the #12345 number of the pull request
    ############
    def write_needs_changes_msg(self, dm_id, reviewer_user_id, status, pr_title, pr_url, pr_number):
        message = "New review from <@" + reviewer_user_id + ">: " + status
        description = "<@" + reviewer_user_id + "> has reviewed your pull request: *" + pr_title + "* <" + pr_url + "|#" + pr_number + ">\n\nPlease address their comments and let them know when you've updated the PR."
        ready_for_review_button = {
            "name": "updated",
            "type": "button",
            "text": "Updated PR",
            "style": "primary",
            "value": "updated"
        }

        attachment = {
            "text": description,
            "fallback": message,
            "color": "#000000",
            "attachment_type": "default",
            "mrkdwn_in": ["text"]
        }

        if status != "Approved":
            attachment["actions"] = [ready_for_review_button]

        self.clients.web.chat.post_message(dm_id, message, attachments=[attachment], as_user='true')


