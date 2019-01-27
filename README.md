## stackstats app
This application is developed using Python 2.7

## Dependencies
+ beautifulsoup4
+ bs4
+ certifi
+ chardet
+ idna
+ json2html
+ nose
+ python-dateutil
+ requests
+ six
+ soupsieve
+ tabulate
+ urllib3

## Installation

Unzip the `encode-python-assignment.zip` file
If you use linux, use the **unzip** command to extract the package

*Step 1: Install unzip command*

`sudo apt-get install unzip`

*Step 2: unzip the package*

`unzip encode-python-assignment.zip`

After the files extraction do the following

`cd python-assignment/`

`pip install .`

## Command line usage

Use the following command to see the command line arguments

`stats --help`

The output is:

```bash
usage: stats [-h] [--since SINCE] [--until UNTIL]
             [--output_format OUTPUT_FORMAT]

Instructs stackstats package to manage date/time range and results output
format

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE         Start date
  --until UNTIL         End date
  --output_format OUTPUT_FORMAT
                        return the calculated statistics in tabular/html/json

```

**Examples:**

the package command returns the results by default in json format
But you can define the the command to return the results in tabular or htmk format


Get the results in json format from 2018-12-03 10:00:00 until 2018-12-03 12:00:00


`stats --since '2018-12-03 12:00:00' --until '2018-12-03 10:00:00'`

```json
{"average_answers_per_question": 0.6666666666666666, "accepted_answers_average_score": 0.0, "total_accepted_answers": 1, "top_ten_answers_comment_count": {"54169541": 10, "54172039": 0, "54172037": 0, "54151440": 0, "54172084": 0, "54172088": 0, "54172026": 0, "54172092": 0, "54172093": 0, "54172090": 0}}
```

Get the results in tabular format


`stats --since '2018-12-04 13:00:00' --until '2018-12-04 14:00:00' --output_format tabular`

```bash
Actions                         Results
------------------------------  -----------------------------------------------------------------------------------------------------------------------------------
accepted_answers_average_score  0
average_answers_per_question    0.466666666667
top_ten_answers_comment_count   {54172096: 0, 54171937: 4, 54172100: 0, 54169541: 10, 54172103: 0, 54172110: 0, 54172084: 1, 54172026: 0, 54171197: 0, 54172101: 0}
total_accepted_answers          0
```

Get the results in html format

`stats --since '2018-12-05 09:00:00' --until '2018-12-05 11:00:00' --output_format html`

```html
<table border="1"><tr><th>average_answers_per_question</th><td>0.7</td></tr><tr><th>accepted_answers_average_score</th><td>0</td></tr><tr><th>total_accepted_answers</th><td>0</td></tr><tr><th>top_ten_answers_comment_count</th><td><table border="1"><tr><th>54171937</th><td>4</td></tr><tr><th>54172132</th><td>0</td></tr><tr><th>54172069</th><td>0</td></tr><tr><th>54172136</th><td>0</td></tr><tr><th>54172137</th><td>0</td></tr><tr><th>54172133</th><td>0</td></tr><tr><th>54172047</th><td>1</td></tr><tr><th>54172117</th><td>2</td></tr><tr><th>54172090</th><td>0</td></tr><tr><th>54171717</th><td>6</td></tr></table></td></tr></table>
```
## Usage

```python
import stackstats
api = stackstats.StackExchangeApi(since='2018-12-05 09:00:00', until='2018-12-05 11:00:00')

# Get all the answers since 2018-12-05 09:00:00 until 2018-12-05 11:00:00
answers = api.answers()

# Get all the accepted answers since 2018-12-05 09:00:00 until 2018-12-05 11:00:00
accepted_answers = api.accepted_answers(answers)

# Get the number of all accepted answers
total_accepted_answers = api.get_num_of_accepted_answers(accepted_answers)

# Get average score for all accepted answers since 2018-12-05 09:00:00 until 2018-12-05 11:00:00
accepted_answers_average_score = api.average_accepted_score(accepted_answers)

# Get the average answer count per question
average_answers_per_question = api.avg_count_question()

# Get the number of comments for given answer
num_of_comments = api.get_answer_comments(answer_id="54153375")

# Get the 10 answers ids with the highest score
top_ten_answers_ids = api.get_top_answers(answers)

# Get the comment count for each of the 10 answers with the highest score
number_of_comments_per_answer = api.get_top_answers_comments(top_ten_answers_ids)

# Get all statistics and return them in html/tabular/json format
statistics = api.results(format="json")
```

## Tests
To test the application you can simply do

`python2 setup.py test`