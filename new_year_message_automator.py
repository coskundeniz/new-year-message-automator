import sys
from argparse import ArgumentParser
from message import MessageHeader, MessageContent
from utils import send_email, logger


def ask_params(arg_parser):
    """Get parameters from user interactively

    :type arg_parser: ArgumentParser
    :param arg_parser: ArgumentParser instance
    :rtype: tuple
    :returns: (MessageHeader, MessageContent) tuple
    """

    print("\n==================================================")
    print("============ New Year Message Creator ============")
    print("==================================================\n")

    from_email = input("Sender email: ")
    to_email = input("Receiver email: ")

    if not (from_email and to_email):
        msg = f"{'Sender' if not from_email else 'Receiver'} mail address is missing!"
        print_usage_and_exit(arg_parser, msg)

    subject = input("Mail subject[Merry Christmas]: ") or "Merry Christmas"

    msg_header = MessageHeader(from_email, to_email, subject)
    msg_content = MessageContent()

    msg_content.message = input("Your message: ")

    if not msg_content.message:
        print_usage_and_exit(arg_parser, "Please type a message!")

    msg_content.background = input("Background[darkred]: ") or "darkred"
    msg_content.text_color = input("Text color[white]: ") or "white"

    return (msg_header, msg_content)


def get_arg_parser():
    """Get argument parser

    :rtype: ArgumentParser
    :returns: ArgumentParser object
    """

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--fromaddr", help="Sender mail address")
    arg_parser.add_argument("-t", "--toaddr",
                            help="Receiver mail address(es). \
                                  For multiple emails give comma separated emails \
                                  or a file with an email per line")
    arg_parser.add_argument("-s", "--subject", default="Merry Christmas",
                            help="Mail subject")
    arg_parser.add_argument("-m", "--message", help="Message to send")
    arg_parser.add_argument("-b", "--background", default="darkred",
                            help="Background color by name or color code without # sign")
    arg_parser.add_argument("-c", "--textcolor", default="white",
                            help="Message text color")

    return arg_parser


def print_usage_and_exit(arg_parser, message):
    """Print help and exit with given message

    :type arg_parser: ArgumentParser
    :param arg_parser: ArgumentParser instance
    :type message: str
    :param message: Message to print
    """

    arg_parser.print_help()
    raise SystemExit(message)


def main():

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    logger.debug(f"len(sys.argv): {len(sys.argv)}")

    if len(sys.argv) == 1:
        msg_header, msg_content = ask_params(arg_parser)
    else:
        if args.fromaddr:
            logger.debug(f"args.fromaddr: {args.fromaddr}")
            from_email = args.fromaddr
        else:
            print_usage_and_exit(arg_parser, "Sender mail address is missing!")

        if args.toaddr:
            logger.debug(f"args.toaddr: {args.toaddr}")
            to_email = args.toaddr
        else:
            print_usage_and_exit(arg_parser, "Receiver mail address is missing!")

        if args.subject:
            logger.debug(f"args.subject: {args.subject}")
            subject = args.subject

        msg_header = MessageHeader(from_email, to_email, subject)
        msg_content = MessageContent()

        if args.message:
            logger.debug(f"args.message: {args.message}")
            msg_content.message = args.message
        else:
            print_usage_and_exit(arg_parser, "Please type a message!")

        if args.background:
            logger.debug(f"args.background: {args.background}")
            msg_content.background = args.background

        if args.textcolor:
            logger.debug(f"args.textcolor: {args.textcolor}")
            msg_content.text_color = args.textcolor

    message = msg_content.construct_html_message()

    send_email(msg_header, message)


if __name__ == "__main__":

    main()