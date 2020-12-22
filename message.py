import os
from utils import get_emails, logger


class MessageHeader():

    def __init__(self, from_email, to_email, subject):

        self.from_email = from_email

        if "," in to_email:
            self.to_email = to_email.split(",")
        elif os.path.isfile(to_email):
            self.to_email = get_emails(to_email)
        else:
            self.to_email = [to_email]

        self.subject = subject

    @property
    def emails(self):
        """Get email list

        :rtype: list
        :returns: List of mail addresses
        """

        return self.to_email


class MessageContent():

    def __init__(self):

        self.message = ""
        self.text_color = "white"
        self.background = "darkred"

    def construct_html_message(self):
        """Prepare the message card

        :rtype: str
        :returns: HTML for the message body
        """

        header_text = ('<!doctype html>'
        '<html>'
            '<head>'
            '<meta content="text/html; charset=UTF-8" http-equiv="content-type">'

        '<style>'
            '#container {'
                'width: 500px;'
                'height: 300px;'
                f'background-color: {self.background};'
                'display: flex;'
                'justify-content: center;'
                'align-items: center;'
            '} '

            '.message-border {'
                'width: 90%;'
                'height: 85%;'
                f'border: 2px solid {self.text_color};'
                'border-radius: 10px;'
                'display: flex;'
                'justify-content: center;'
                'align-items: center;'
            '} '

            '.message {'
                f'color: {self.text_color};'
                'font-size: 1.3rem;'
                'line-height: 1.3em;'
                'text-align: center;'
                'padding-left: 5px;'
                'padding-right: 5px;'
            '}'
        '</style>'
        '</head>')

        body_text = """<body>

        <div id="container">
            <div class="message-border">
                <p class="message">{message}</p>
            </div>
        </div>

        </body>
        </html>
        """.format(message=self.message)

        message_body = header_text + body_text

        logger.debug(f"Message body:\n{message_body}\n")

        return message_body