import psycopg2
from django.test import TestCase
from django.test.client import RequestFactory
import pandas as pd
from rates.models import Price, Port
from django.conf import settings
from parameterized import parameterized

from rates.views import average
from rates.utils import add_regions, add_ports, add_prices

class AverageDayPriceTest(TestCase):
    request_factory = RequestFactory()
    end_point = "/rates/"

    def setUp(self):
        regions = pd.read_csv("./rates/tests/data/regions.csv").fillna("")
        add_regions(regions=regions)
        ports = pd.read_csv("./rates/tests/data/ports.csv").fillna("")
        add_ports(ports=ports)
        prices = pd.read_csv("./rates/tests/data/prices.csv").fillna("")
        add_prices(prices=prices)
        
    def create_request(self, end_point: str, data: dict, request_method: str):
        request = getattr(self.request_factory, request_method)
        request = request(end_point)
        return request

    @parameterized.expand([
        (["2021-01-01", "2021-01-05", "CNHDG", "SESOE"], 200, {
            "2021-01-02": 100.00
        }),
        (["2021-01-01", "2021-01-05", "CNHDG", "SESO"], 400),
        (["2021-01-06", "2021-01-05", "CNHDG", "SESOE"], 400),
        (["2021-01-06", "2021-01-05", "CNHDG", "SESOE"], 400),
        (["2021-01-00", "2021-01-05", "CNHDG", "SESOE"], 400),
        (["2021-01-01", "2021-01-05", "CNHDG", "northern_europe"], 200,
        {
            "2021-01-02": 166.67
        }),
        (["2021-01-01", "2021-01-05", "china_main", "northern_europe"], 200,
        {
            "2021-01-02": 166.67
        }),
        (["2021-01-01", "2021-01-05", "northern_europe", "china_main"], 200,
        {
            "2021-01-01": 150.00,
            "2021-01-03": 100.00
        }),
    ])
    def test_average_day_price(self, query_params, status_code, expected_result=None):
        endpoint = self.end_point + "?date_from={}&date_to={}&origin={}&destination={}".format(*query_params)
        request = self.create_request(end_point=endpoint, data={}, request_method='get')
        response = average(request)
        assert response.status_code == status_code
        if response.status_code == 200:
            for row in response.data:
                day = str(row['day'])
                if day not in expected_result:
                    assert row['average_price'] is None
                else:
                    assert float(row['average_price']) == expected_result[day]