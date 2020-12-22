import logging
import getpass

try:
    import yagmail
except ImportError:
    raise SystemExit("Please run 'pipenv install' or 'pip install -r requirements.txt'")

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("automator.log", mode="w", encoding="utf-8")
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
log_format = "%(asctime)s [%(levelname)5s] %(lineno)3d: %(message)s"
formatter = logging.Formatter(log_format, datefmt="%d-%m-%Y %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def send_email(message_header, message):
    """Send email to recepients

    :type message_header: MessageHeader
    :param message_header: MessageHeader instance
    :type message: str
    :param message: HTML formatted message text
    """

    emails = message_header.emails

    try:
        user_from = message_header.from_email
        pwd = getpass.getpass("Enter mail password: ")
        mailer = yagmail.SMTP(user_from, pwd)
    except Exception as e:
        logger.debug("Failed to initialize mail client!")
        raise SystemExit(e)

    for email in emails:

        try:
            logger.info(f"Sending email to {email}...")

            mailer.send(
                to=email,
                subject=message_header.subject,
                contents=message
            )
        except Exception as e:
            logger.error(f"Failed to send mail to {email}!")
            logger.debug(f"Error: {e}")


def get_emails(filepath):
    """Get email addresses from given file

    :type filepath: str
    :param filepath: Path of the file containing emails
    :rtype: list
    :returns: List of email addresses
    """

    with open(filepath, "r") as f:
        emails = f.read().splitlines()

    return emails