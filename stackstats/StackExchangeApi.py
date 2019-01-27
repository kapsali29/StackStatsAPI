import json
import time

import json2html
import requests
import tabulate

from stackstats.settings import ACCESS_TOKEN, KEY, STACKEXCHANGE_URL, API_VERSION, ANSWERS_URL, QUESTIONS_URL, \
    COMMENTS_URL, \
    SECONDS_TO_SLEEP
from stackstats.utils import time2unix


class StackExchangeApi(object):
    def __init__(self, since, until):
        self.access_token = ACCESS_TOKEN
        self.key = KEY
        self.sec_to_sleep = SECONDS_TO_SLEEP
        self.since = time2unix(since)
        self.until = time2unix(until)

    def answers(self):
        """
        The following function retrieves answer data for a given date/time range
        Args:

        Returns: answers within that date/time range

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()

        """
        endpoint = "https://{}/{}/{}".format(STACKEXCHANGE_URL, API_VERSION, ANSWERS_URL)
        from_time2unix = self.since
        min_time2unix = self.until
        querystring = {"fromdate": from_time2unix, "order": "desc", "min": min_time2unix, "sort": "activity",
                       "site": "stackoverflow", "access_token": self.access_token, "key": self.key}
        response = requests.get(url=endpoint, params=querystring)
        response2json = response.json()
        response_keys = response2json.keys()
        if response.status_code == 200 and "items" in response_keys:
            items = response2json["items"]
            if "backoff" in response_keys:
                backoff_param = response2json["backoff"]
                print(" Sleep {} seconds to avoid backoff violation".format(backoff_param))
                time.sleep(backoff_param)
            return items
        else:
            print(" Sleep {} seconds due to backoff violation".format(self.sec_to_sleep))
            time.sleep(self.sec_to_sleep)
            return []

    def accepted_answers(self, all_answers):
        """
        The following function filters the answers and return all the accepted answers
        Args:
            all_answers: all answers in the provided timeframe
        Returns: accepted answers

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()
            >>> accepted_answers = api.accepted_answers(answers)

        """
        accepted_answers = []
        for answer in all_answers:
            if answer["is_accepted"]:
                accepted_answers.append(answer)
        return accepted_answers

    def get_num_of_accepted_answers(self, accepted_answers):
        """
        The following function is used to calculate the number of all accepted answers
        Args:
            accepted_answers: accepted answers
        Returns: number of accepted answers

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()
            >>> accepted_answers = api.accepted_answers(answers)
            >>> total_accepted_answers = api.get_num_of_accepted_answers(accepted_answers)

        """
        number_of_accepted_answers = len(accepted_answers)
        return number_of_accepted_answers

    def average_accepted_score(self, accepted_answers):
        """
        This function is used to return the average score of all the accepted answers between the define timeframe
        Args:
            accepted_answers: accepted answers
        Returns: average score

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()
            >>> accepted_answers = api.accepted_answers(answers)
            >>> accepted_answers_average_score = api.average_accepted_score(accepted_answers)

        """
        number_of_accepted_answers = len(accepted_answers)
        if number_of_accepted_answers:
            sum_of_scores = 0
            for answer in accepted_answers:
                sum_of_scores += answer["score"]
            average_score = float(sum_of_scores) / float(number_of_accepted_answers)
        else:
            average_score = 0
        return average_score

    def avg_count_question(self):
        """
        The following function returns the average answer count question for the given timeframe
        Returns: average count

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>>  average_answers_per_question = api.avg_count_question()

        """
        endpoint = "https://{}/{}/{}".format(STACKEXCHANGE_URL, API_VERSION, QUESTIONS_URL)
        querystring = {"fromdate": self.since, "order": "desc", "min": self.until, "sort": "activity",
                       "site": "stackoverflow", "access_token": self.access_token, "key": self.key}
        response = requests.get(url=endpoint, params=querystring)
        if response.status_code == 200 and "items" in response.json().keys():
            questions = response.json()["items"]
            number_of_questions = len(questions)
            answers_counts = 0
            if number_of_questions:
                for question in questions:
                    answers_counts += question["answer_count"]
                result = float(answers_counts) / float(number_of_questions)
            else:
                result = 0
        else:
            result = 0
        return result

    def get_answer_comments(self, answer_id):
        """
        The following function is used to retrieve the number of comments for the provided answer
        Args:
            answer_id: answer id

        Returns: number of comments

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> comments = api.get_answer_comments(answer_id="54153375")

        """
        params = {"answerID": answer_id}
        endpoint = "https://{}/{}/{}".format(STACKEXCHANGE_URL, API_VERSION, COMMENTS_URL.format(**params))
        querystring = {"order": "desc", "sort": "creation", "site": "stackoverflow", "access_token": self.access_token,
                       "key": self.key}
        response = requests.get(url=endpoint, params=querystring)
        number_of_comments = len(response.json()["items"])
        return number_of_comments

    def get_top_answers(self, all_answers):
        """
        The following function is used to get the top 10 answers with the highest score
        Args:
            all_answers: all answers in the provided timeframe

        Returns: top ten answers ids

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()
            >>> top_ten_answers_ids = api.get_top_answers(answers)

        """
        top_answer_ids = []
        if all_answers:
            sorted_answers = sorted(all_answers, key=lambda k: k['score'], reverse=True)[:10]
            for answer in sorted_answers:
                top_answer_ids.append(answer["answer_id"])
            return top_answer_ids
        else:
            return []

    def get_top_answers_comments(self, top_answers_ids):
        """
        The following function is used to retrieve the number of comments for the answers with the highest score
        Args:
            top_answers_ids: top answers ids

        Returns: number of comments per answer id

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> answers = api.answers()
            >>> top_ten_answers_ids = api.get_top_answers(answers)
            >>> top_ten_answers_comment_count = api.get_top_answers_comments(top_ten_answers_ids)

        """
        result_dict = {}
        if top_answers_ids:
            for answer_id in top_answers_ids:
                result_dict[answer_id] = self.get_answer_comments(answer_id)
        return result_dict

    def results(self, format):
        """
        The following function when is called returns the results in json or HTML format
        Args:
            format: HTML/json format
        Returns: results in json format

        Examples:
            >>> api = StackExchangeApi('2016-02-01 10:00:00', '2016-02-01 11:00:00')
            >>> output = api.results()

        """
        answers = self.answers()
        accepted_answers = self.accepted_answers(answers)
        top_answers_ids = self.get_top_answers(answers)
        total_accepted_answers = self.get_num_of_accepted_answers(accepted_answers)
        accepted_answers_average_score = self.average_accepted_score(accepted_answers)
        average_answers_per_question = self.avg_count_question()
        top_ten_answers_comment_count = self.get_top_answers_comments(top_answers_ids)
        result_dict = {
            "total_accepted_answers": total_accepted_answers,
            "accepted_answers_average_score": accepted_answers_average_score,
            "average_answers_per_question": average_answers_per_question,
            "top_ten_answers_comment_count": top_ten_answers_comment_count
        }
        if format == "json":
            output_as_json = json.dumps(result_dict)
            return output_as_json
        if format == "html":
            output_as_html = json2html.json2html.convert(json=result_dict)
            return output_as_html
        if format == "tabular":
            headers = ["Actions", "Results"]
            data = sorted([(k, v) for k, v in result_dict.items()])
            return tabulate.tabulate(data, headers=headers)
