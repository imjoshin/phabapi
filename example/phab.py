import auth
import sys

sys.path.append('../src')
from phabapi import PhabAPI, PhabHandler

def main():
    PhabAPI(ExampleHandler(), auth.MAIL_SMTP, auth.MAIL_USER, auth.MAIL_PASS, auth.MAIL_LABEL).start()

class ExampleHandler(PhabHandler):
    def on_diff_new(self, id, desc, act_user):
        print("on_diff_new: {}: {}".format(id, desc))

    def on_diff_request_changes(self, id, desc, act_user):
        print("on_diff_request_changes: {}: {} ({})".format(id, desc, act_user))

    def on_diff_comment(self, id, desc, act_user, comment):
        print("on_diff_comment: {}: {} ({}) - {}".format(id, desc, act_user, 'comment'))

    def on_diff_inline_comments(self, id, desc, act_user, comments):
        print("on_diff_inline_comments: {}: {} ({}) - {}".format(id, desc, act_user, 'comments'))

    def on_diff_ready_to_land(self, id, desc):
        print("on_diff_ready_to_land: {}: {}".format(id, desc))

    def on_task_comment(self, id, desc, act_user, comment):
        print("on_task_comment: {}: {} ({}) - {}".format(id, desc, act_user, comment))

    def on_task_move(self, id, desc, act_user):
        print("on_task_move: {}: {} ({})".format(id, desc, act_user))

if __name__ == "__main__":
    main()
