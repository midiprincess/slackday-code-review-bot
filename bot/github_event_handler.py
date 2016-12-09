import json

class GitHubEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handleNeedsReviewEvent(self, pull_request):
        # TODO: map these to slack users
        pr_author = json['user']['login']
        pr_assignee = json['assignee']['login']

        slack_author_id = 'U1223543'
        slack_reviewer_id = 'U1223543'

        im_response = self.clients.web.im.open(slack_reviewer_id)
        dm = im_response.json['channel']
        dm_id = dm['id']

        pr_title = pull_request['title']
        pr_url = json['html_url']
        pr_number = json['number']

        self.msg_writer.write_needs_review_msg(dm_id, slack_author_id, pr_title, pr_url, pr_number)