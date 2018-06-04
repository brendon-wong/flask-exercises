# Flask Login

Refactor your users and messages application to use flask_login! This should not be a terribly long refactor so now is a great time to go back and add some more testing and styling to your application! 

### Brendon's Notes
- The @login_required custom decorator can be removed and replaced with Flask-Login's provided @login_required decorator
- The remaining decorators will need to be modified to use current_user instead of sessions