import json

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

    def handleCommentsAddressedEvent(self, slack_author_id, dm_id, message):
        # TODO extract below values from message. it needs to be un-escaped
        pr_title = "PR"
        pr_url = "http://myurl"
        pr_number = 1234
        dm_id = 1232

        self.msg_writer.write_needs_review_msg(dm_id, slack_author_id, pr_title, pr_url, pr_number)


    def getSlackIdFromGithubUsername(self, github_username):
        with open('resources/github.json') as data_file:    
            data = json.load(data_file)
            return data[github_username]