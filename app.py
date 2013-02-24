#! /usr/bin/env python

"""
SMS Calendar Blaster
Blasts SMS messages to people right before required events.
"""

import sys
import atexit
import time
import api_server
from argparse import ArgumentParser
from threading import Thread
from cal_thread import CalThread

calthread = None


def create_cli_parser():

    cli_parser = ArgumentParser(description='Blast some SMS.')

    # Add the CLI options
    cli_parser.add_argument('-d', '--debug', help='enable debug output',
                            action='store_true', default=False)

    cli_parser.add_argument('-a', '--api-mode',
                            help="only run HTTP API",
                            action='store_true',
                            default=False)

    return cli_parser


def main(argv):

    cli_parser = create_cli_parser()
    args = cli_parser.parse_args()

    if not args.api_mode:
        # start calendar querying and SMS sending
        calthread = CalThread()
        calthread.setDaemon(True)
        calthread.start()

        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                break

        calthread.stop = True
        calthread.join()
    else:
        api_server.main()


if __name__ == "__main__":
    main(sys.argv[1:])


@atexit.register
def goodbye():
    print "Goodbye."
