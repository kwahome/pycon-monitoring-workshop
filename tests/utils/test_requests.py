import unittest
import os
import time
import requests as bare_requests
from utils.requests import RequestsWrapper
from utils.metrics import timer
from copy import deepcopy

from unittest.mock import patch

HTTPBIN_URL = os.getenv('HTTPBIN_URL', "http://localhost:8000")
requests = RequestsWrapper()


def test_wrapper(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return test_wrapper.__name__
    return wrapper


class RequestsWrapperFunctionalTest(unittest.TestCase):

    def setUp(self):

        self.httpbin = dict(
            url=HTTPBIN_URL,
            endpoints=dict(
                delete="/delete",
                get="/get",
                patch="/patch",
                post="/post",
                put="/put"
            )

        )
        self.data = dict()
        self.kwargs = dict()

    def tearDown(self):
        self.data = {}

    def test_GET(self):
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["get"]
        )

        res = requests.get(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(200, res.status_code)

    def test_PATCH(self):
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["patch"]
        )
        res = requests.patch(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(200, res.status_code)

    def test_POST(self):
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["post"]
        )
        res = requests.post(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(200, res.status_code)

    def test_PUT(self):
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["put"]
        )
        res = requests.put(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(200, res.status_code)

    def test_DELETE(self):
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["delete"]
        )
        res = requests.delete(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(200, res.status_code)

    def test_no_attribute_exception_handling(self):
        with patch.object(bare_requests, 'get') as requests_mock:
            requests_mock.side_effect = SyntaxError('Houston!')

            url = "{httpbin_url}{endpoint}".format(
                httpbin_url=self.httpbin["url"],
                endpoint=self.httpbin["endpoints"]["get"]
            )

            with self.assertRaises(SyntaxError):
                requests.get(
                    url,
                    data=self.data,
                    timeout=30,
                    verify=False,
                    **self.kwargs
                )

    def test_no_general_exception_handling(self):

        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["get"]
        )

        with self.assertRaises(AttributeError):
            requests.none(
                url,
                data=self.data,
                timeout=30,
                verify=False,
                **self.kwargs
            )

    def test_disabling_wrapping(self):
        requests.wrapper = test_wrapper
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["get"]
        )

        res = requests.get(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )
        self.assertEqual(test_wrapper.__name__, res)
        self.assertEqual(test_wrapper.__name__, requests.wrapper.__name__)

        # set wrapper to None
        requests.wrapper = None
        res = requests.get(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )
        self.assertEqual(None, requests.wrapper)
        self.assertNotEqual(test_wrapper.__name__, res)
        self.assertEqual(200, res.status_code)

    def test_bring_your_own_wrapper(self):
        requests.wrapper = test_wrapper
        url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["get"]
        )

        res = requests.get(
            url,
            data=self.data,
            timeout=30,
            verify=False,
            **self.kwargs
        )

        self.assertEqual(res, test_wrapper.__name__)


class RequestsWrapperPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.httpbin = dict(
            url=HTTPBIN_URL,
            endpoints=dict(
                delete="/delete",
                get="/get",
                patch="/patch",
                post="/post",
                put="/put"
            )

        )
        self.data = {}
        self.kwargs = dict(number=1000)

        self.url = "{httpbin_url}{endpoint}".format(
            httpbin_url=self.httpbin["url"],
            endpoint=self.httpbin["endpoints"]["get"]
        )

    @staticmethod
    def timed(fun, *args, **kwargs):
        number = 1000
        if 'number' in kwargs.keys():
            number = kwargs.pop('number')
        test_num = []
        for i in range(number):
            t0 = time.time()
            r = fun(*args, **kwargs)
            assert r.status_code == 200
            time_taken = (time.time() - t0) * number
            test_num.append(time_taken)

        average_time = sum(test_num) / len(test_num)
        print('[timer]: func `{}` execution took {} ms.'.format(fun.__name__,
                                                                average_time))
        return average_time

    def bare_requests_timed(self, number=1):
        import requests
        kwargs = deepcopy(self.kwargs)
        kwargs['number'] = number
        return self.timed(
            requests.get,
            self.url,
            data=self.data,
            timeout=30,
            verify=False,
            **kwargs
        )

    def hermes_requests_timed(self, number=1, wrapper=timer('test')):
        from utils.requests import RequestsWrapper
        requests = RequestsWrapper()
        requests.wrapper = wrapper
        kwargs = deepcopy(self.kwargs)
        kwargs['number'] = number
        return self.timed(
            requests.get,
            self.url,
            data=self.data,
            timeout=30,
            verify=False,
            **kwargs
        )

    def test_request_performance_vs_bare_requests(self):
        for number in [1, 10, 100, 500, 1000]:
            print("")
            print("RUNNING {0} TIMES".format(number))
            print("--------------------------------")
            print("1. bare requests")
            b_req_time = self.bare_requests_timed(number=number)
            print("* time = {0} ms".format(b_req_time))
            print("2. hermes requests")
            h_req_time = self.hermes_requests_timed(number=number)
            print("* time = {0} ms".format(h_req_time))
            time_diff = h_req_time - b_req_time
            print("time diff (hermes requests time - bare requests time) "
                  "= {0} ms".format(time_diff))
            print("")

        # Assert time difference not greater than 1ms
        # TODO: Find a good way to determine best benchmark
        self.assertTrue(time_diff < 5)
