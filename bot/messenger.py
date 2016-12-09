# -*- coding: utf-8 -*-

import logging
import random

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack):
        self.slack = slack

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
        description = "You've been given the honor of reviewing: *" + pr_title + "* <" + pr_url + "|#" + str(pr_number) + ">. \n\nPlease take a look when you have time. \n\nWhen you're done reviewing the PR, please be sure to `Submit Review` and select one of `Comment`, `Approve`, or `Request Changes`."

        attachment = {
            "text": description,
            "fallback": message,
            "color": "#000000",
            "attachment_type": "default",
            "mrkdwn_in": ["text"]
        }
        self.slack.chat.post_message(dm_id, message, attachments=[attachment], as_user='true')

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
    def write_review_submitted_msg(self, dm_id, reviewer_user_id, status, pr_title, pr_url, pr_number):
        description = "*{}* <{}|#{}>".format(pr_title, pr_url, pr_number) #TODO: add summary
        if status == 'approved':
            message = "<@{}> has approved your PR! :tada:".format(reviewer_user_id)
        elif status == 'changes_requested':
            message = "<@{}> has requested changes on your PR.".format(reviewer_user_id)
            description += "\n\nPlease address their comments and let them know when you've done."
     
        merge_button = {
            "name": "merge",
            "type": "button",
            "text": "Merge",
            "style": "primary",
            "value": "merge",
        }

        ready_for_review_button = {
            "name": "updated",
            "type": "button",
            "text": "Updated",
            "style": "primary",
            "value": "updated",
        }

        attachment = {
            "text": description,
            "fallback": message,
            "color": "#000000",
            "attachment_type": "default",
            "mrkdwn_in": ["text"],
        }

        if status != "approved":
            attachment["actions"] = [ready_for_review_button]
            attachment["callback_id"] = "updated"
        else:
            attachment["actions"] = [merge_button]
            attachment["callback_id"] = "merge"

        self.slack.chat.post_message(dm_id, message, attachments=[attachment], as_user='true')


    
