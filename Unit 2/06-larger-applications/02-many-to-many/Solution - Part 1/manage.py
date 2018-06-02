from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# Configure Flask Migrate
migrate = Migrate(app, db)

# Configure Flask Script
manager = Manager(app)

# Run Flask Migrate commands: python3 solution_manage.py db [insert command]
manager.add_command('db', MigrateCommand)

# Do not run if this module is being imported
if __name__ == '__main__':
  manager.run()