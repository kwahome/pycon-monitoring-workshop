
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app


class TestDevelopmentConfig(TestCase):
    @staticmethod
    def create_app():
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret-key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    @staticmethod
    def create_app():
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret-key')
        self.assertTrue(app.config['DEBUG'])


class TestProductionConfig(TestCase):
    @staticmethod
    def create_app():
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


class TestStagingConfig(TestCase):
    @staticmethod
    def create_app():
        app.config.from_object('config.StagingConfig')
        return app

    def test_app_is_staging(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
