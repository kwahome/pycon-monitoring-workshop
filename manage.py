import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Notification

environment = os.environ['ENVIRONMENT']

app = create_app(environment=environment)

app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """
    Start flask app binding to any host
    """
    app.run(host='0.0.0.0')


@manager.command
def test():
    """
    Runs the unit tests.
    """
    tests = unittest.TestLoader().discover('tests', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
