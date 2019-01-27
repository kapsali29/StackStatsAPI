import sys

import stackstats
from stackstats.utils import get_parser, validate_date_format


def main():
    args = get_parser().parse_args()
    since = args.since
    until = args.until
    _format = args.output_format
    if not since:
        print(" You must specify a valid Start time")
        sys.exit()
    if not validate_date_format(since):
        print("Incorrect Start date format, should be YYYY-MM-DD HH:MM:SS")
        sys.exit()
    if not until:
        print(" You must specify a valid End date")
        sys.exit()
    if not validate_date_format(until):
        print("Incorrect End date format, should be YYYY-MM-DD HH:MM:SS")
        sys.exit()

    api = stackstats.StackExchangeApi(since, until)
    print(api.results(_format))
