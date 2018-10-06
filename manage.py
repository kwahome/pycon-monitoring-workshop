import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app

environment = os.environ['ENVIRONMENT']

app, db = create_app(environment=environment)

app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """
    Start flask app binding to all public IPs
    """
    app.run(host='0.0.0.0')


@manager.command
def test():
    """
    Runs the unit tests.
    """
    tests = unittest.TestLoader().discover('.', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
