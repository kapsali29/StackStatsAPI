from unittest import TestCase

from bs4 import BeautifulSoup

import stackstats
from stackstats.utils import is_json


class CheckStackStats(TestCase):
    def setUp(self):
        self.api = stackstats.StackExchangeApi(since='2018-12-05 09:00:00', until='2018-12-05 11:00:00')
        self.results_json = self.api.results(format="json")
        self.results_html = self.api.results(format="html")
        self.results_tabular = self.api.results(format="tabular")

    def test_is_tabular(self):
        if "---" in self.results_tabular:
            decision = True
        else:
            decision = False
        self.assertTrue(decision)

    def test_is_json(self):
        self.assertTrue(is_json(self.results_json))

    def test_is_html(self):
        self.assertTrue(bool(BeautifulSoup(self.results_html, "html.parser").find()))
