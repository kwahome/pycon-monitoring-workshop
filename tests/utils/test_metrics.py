import unittest
from utils.metrics import SimpleMetrics, Constants, timer, metrics

from unittest.mock import MagicMock


class TestSimpleMetrics(unittest.TestCase):
    """
    Tests for the SimpleMetrics class
    """
    def setUp(self):
        self.metrics = SimpleMetrics()

    def tearDown(self):
        self.metrics.data.clear()

    def test_context(self):
        ctx = dict(item1='item 1', item2='item 2')
        self.metrics.context(ctx=ctx)
        for key, value in ctx.items():
            self.assertEqual(value, self.metrics.data[key])

    def test__get(self):
        metric, m_type = 'test_get', 'count'
        self.assertEqual(0, self.metrics._get(metric, m_type))
        # manually set metric
        self.metrics.data[metric] = {
            m_type: 1
        }
        self.assertEqual(1, self.metrics._get(metric, m_type),)

    def test__set(self):
        metric, m_type = 'test_set', 'count'
        self.metrics._set(metric, m_type, 1)
        self.assertEqual(1, self.metrics._get(metric, m_type))

    def test__increment(self):
        metric, m_type, count = 'test_increment', 'count', 1
        curr = self.metrics._get(metric, m_type)
        self.metrics._increment(metric, m_type, count)
        self.assertEqual(
            curr + count, self.metrics._get(metric, m_type)
        )

    def test_count(self):
        metric, m_type, count = 'test_count', Constants.COUNTER, 1
        curr = self.metrics._get(metric, m_type)
        self.metrics.count(metric, count)
        self.assertEqual(
            curr + count, self.metrics._get(metric, m_type)
        )

    def test_error(self):
        metric, m_type, count = 'test_error', Constants.ERROR, 1
        curr = self.metrics._get(metric, m_type)
        self.metrics.error(metric, count)
        self.assertEqual(
            curr + count, self.metrics._get(metric, m_type)
        )

    def test_gauge(self):
        metric, m_type, value = 'test_gauge', Constants.GAUGE, 5
        curr_value = self.metrics._get(metric, m_type)
        self.metrics.gauge(metric, value)
        self.assertEqual(
            curr_value + value, self.metrics._get(metric, m_type)
        )

    def test_time(self):
        metric, m_type, value = 'test_time', Constants.TIMER, 10
        curr_value = self.metrics._get(metric, m_type)
        curr_count = self.metrics._get(metric, Constants.COUNTER)
        self.metrics.time(metric, value)
        self.assertEqual(
            curr_value + value, self.metrics._get(metric, m_type)
        )
        self.assertEqual(
            curr_count + 1, self.metrics._get(metric, Constants.COUNTER)
        )

    def test__prepare(self):
        self.metrics._p
        pass

    def test__prepare(self):
        pass


class TestTimerDecorator(unittest.TestCase):
    """
    Tests for the `with_timer` decorator
    """
    metrics_name = 'testing_decorator'

    def setUp(self):
        self.decorated = "decorated"

    def tearDown(self):
        pass

    @timer(metrics_name)
    def decorated_func(self):
        return self.decorated

    def test_decorated_method_returns_expected(self):
        self.assertEqual(self.decorated_func(), self.decorated)

    def test_exceptions_raised(self):
        self.decorated_func = MagicMock(
            side_effect=SyntaxError('Houston! We have a problem!')
        )
        with self.assertRaises(SyntaxError):
            self.decorated_func()

    def test_metrics_collected(self):
        m = metrics()
        self.assertEqual(self.decorated, self.decorated_func())
        self.assertTrue(self.metrics_name in m.data)

        for m_type in [Constants.TIMER, Constants.COUNTER]:
            self.assertTrue(m_type in m.data[self.metrics_name])
            self.assertTrue(m.data[self.metrics_name][m_type] > 0)
