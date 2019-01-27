import argparse
import datetime
import json


def time2unix(string_time):
    """
    The following function is used to transform a string to unix timestamp
    Args:
        string_time: datetime in string format
    Examples:
        >>> unix_time = time2unix('2019-01-01 00:00:00')

    Returns: unix timestamp

    """
    datetime_object = datetime.datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
    unix_time = int((datetime_object - datetime.datetime(1970, 1, 1)).total_seconds())
    return unix_time


def validate_date_format(date_string):
    """
    The following function check if the given date is has valid format or not.
    Args:
        date_string: string datetime to check its format

    Returns: True/False
    Examples:
        >>> flag = is_date('2019-01-01 00:00:00')

    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


def get_parser():
    """
    Gets an argument parser
    Returns: returns an argument parser
    Examples:
        >>> parser_object = get_parser()

    """
    arg_parser = argparse.ArgumentParser(
        description="Instructs stackstats package to manage date/time range and results output format")
    arg_parser.add_argument("--since", help="Start date")
    arg_parser.add_argument("--until", help="End date")
    arg_parser.add_argument("--output_format", help="return the calculated statistics in tabular/html/json",
                            default="json")
    return arg_parser
