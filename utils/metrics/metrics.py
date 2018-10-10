import abc


class Constants:
    """
    Class containing constants definitions
    """
    COUNTER = 'counter'
    ERROR = 'error'
    GAUGE = 'gauge'
    METRICS = 'metrics'
    TIMER = 'timer'


class BaseMetrics:
    """
    Base metrics class containing abstract methods that must be implemented by
    child classes
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.data = {}

    @abc.abstractmethod
    def bake(self):
        """
        Method to prepare metrics
        :return:
        """
        pass

    @abc.abstractmethod
    def emit(self):
        """
        Method to emit metrics
        :return:
        """
        pass

    def context(self, ctx):
        if ctx is not None:
            self.data.update(ctx)

    def _get(self, metric, m_type):
        result = 0
        if metric in self.data and m_type in self.data[metric]:
            result = self.data[metric][m_type]
        return result

    def _set(self, metric, m_type, value):
        if metric not in self.data:
            self.data[metric] = {}
        self.data[metric][m_type] = value

    def _increment(self, metric, m_type, count):
        self._set(metric, m_type, self._get(metric, m_type) + count)

    def count(self, metric, count=1):
        self._increment(metric, Constants.COUNTER, count)

    def error(self, metric, count=1):
        self._increment(metric, Constants.ERROR, count)

    def gauge(self, metric, value):
        self._set(metric, Constants.GAUGE, value)

    def time(self, metric, value):
        self._increment(metric, Constants.TIMER, value)
        self.count(metric)


class SimpleMetrics(BaseMetrics):
    """
    Implementation of simple metrics
    """
    def bake(self):
        """
        Method to prepare metrics
        :return:
        """
        pass

    def emit(self):
        """
        Method to emit metrics
        :return:
        """
        pass
