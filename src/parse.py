import util
import re
import soupsieve
from bs4 import BeautifulSoup

class DiffParser():
    def __init__(self, handler):
        self.handler = handler

    def _handle_new_revision(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) created this revision")

        if username is not None:
            self.handler.on_diff_new(id, desc, username)

    def _handle_request_changes(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) requested changes to this revision.")

        if username is not None:
            self.handler.on_diff_request_changes(id, desc, username)
        elif 'This revision now requires changes to proceed' in body:
            self.handler.on_diff_request_changes(id, desc, None)

    def _handle_comments(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) added a comment.")

        if username is not None:
            soup = BeautifulSoup(body, 'html.parser')
            paragraphs = soup.select("div > div > p")
            comment = None

            if len(paragraphs) > 0 and len(paragraphs[0].parent.text) > 0:
                comment = paragraphs[0].parent.text

            self.handler.on_diff_comment(id, desc, username, comment)

    def _handle_inline_comments(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) added inline comments")

        if username is not None:
            soup = BeautifulSoup(body, 'html.parser')
            comment_divs = soup.select("div > strong + div > div > div > div")
            comments = []

            # try to find any actual comments
            for div in comment_divs:
                # filter out those with color - those are old comments
                new_comments = [comment.text for comment in div.select("p") if 'color' not in comment.parent['style']]
                comments += new_comments
            self.handler.on_diff_inline_comments(id, desc, username, comments)

    def _handle_ready_to_land(self, id, desc, body):
        if 'This revision is now accepted and ready to land.' in body:
            self.handler.on_diff_ready_to_land(id, desc)

    def parse(self, id, desc, body):
        self._handle_inline_comments(id, desc, body),
        self._handle_new_revision(id, desc, body),
        self._handle_comments(id, desc, body),
        self._handle_request_changes(id, desc, body),
        self._handle_ready_to_land(id, desc, body)

class TaskParser():
    def __init__(self, handler):
        self.handler = handler

    def _handle_comments(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) added a comment.")

        if username is not None:
            soup = BeautifulSoup(body, 'html.parser')
            paragraphs = soup.select("div > div > p")
            comment = None

            if len(paragraphs) > 0 and len(paragraphs[0].parent.text) > 0:
                comment = paragraphs[0].parent.text

            self.handler.on_task_comment(id, desc, username, comment)

    def _handle_task_move(self, id, desc, body):
        username = util.get_regex_match(body, ">([^>]+) moved this task")
        movement = util.get_regex_match(body, "moved this task ([^\.]+)")

        if username is not None:
            self.handler.on_task_move(id, desc, username)

    def parse(self, id, desc, body):
        self._handle_comments(id, desc, body)
        self._handle_task_move(id, desc, body)
