import json
import logging
import urllib

class GitHubEventHandler(object):
    def __init__(self, slack, msg_writer):
        self.slack = slack
        self.msg_writer = msg_writer

    def handleNeedsReviewEvent(self, pull_request):
        # TODO: map these to slack users
        pr_author = pull_request['user']['login']
        pr_assignee = pull_request['assignee']['login']

        slack_author_id = self.getSlackIdFromGithubUsername(pr_author)
        slack_reviewer_id = self.getSlackIdFromGithubUsername(pr_assignee)
        # slack_author_id = 'U038A6XGV'
        # slack_reviewer_id = 'U0HMHRNLT'

        im_response = self.slack.im.open(slack_reviewer_id)
        dm_id = im_response.body['channel']['id']

        pr_title = pull_request['title']
        pr_url = pull_request['html_url']
        pr_number = pull_request['number']

        self.msg_writer.write_needs_review_msg(dm_id, slack_author_id, pr_title, pr_url, pr_number)

    def handleReviewSubmittedEvent(self, pr_state, pull_request):
        # TODO: map these to slack users
        pr_author = pull_request['user']['login']
        pr_assignee = pull_request['assignee']['login']

        slack_author_id = self.getSlackIdFromGithubUsername(pr_author)
        slack_reviewer_id = self.getSlackIdFromGithubUsername(pr_assignee)
        # slack_author_id = 'U038A6XGV'
        # slack_reviewer_id = 'U0HMHRNLT'

        im_response = self.slack.im.open(slack_author_id)
        dm_id = im_response.body['channel']['id']

        pr_title = pull_request['title']
        pr_url = pull_request['html_url']
        pr_number = pull_request['number']

        self.msg_writer.write_review_submitted_msg(dm_id, slack_reviewer_id, pr_state, pr_title, pr_url, pr_number)

    def handleCommentsAddressedEvent(self, message):
        # extract below values from message. it needs to be un-escaped
        # format is *{}* <{}|#{}>
        attachment_text = message['attachments'][0]['text']
        title_start = attachment_text.find("*") + 1
        title_end = attachment_text.find("*", title_start)
        pr_title = attachment_text[title_start:title_end]

        url_start = attachment_text.find("<") + 1
        url_end = attachment_text.find("|")
        pr_url = attachment_text[url_start:url_end]

        number_start = attachment_text.find("#") + 1
        number_end = attachment_text.find(">")
        pr_number = attachment_text[number_start:number_end]

        message_text = message['text']
        id_start = message_text.find("@") + 1
        id_end = message_text.find(">")
        slack_reviewer_id = message_text[id_start:id_end]

        im_response = self.slack.im.open(slack_reviewer_id)
        dm_id = im_response.body['channel']['id']

        self.msg_writer.write_needs_review_msg(dm_id, slack_reviewer_id, pr_title, pr_url, pr_number)


    def getSlackIdFromGithubUsername(self, github_username):
        with open('resources/github.json') as data_file:    
            data = json.load(data_file)
            return data[github_username]