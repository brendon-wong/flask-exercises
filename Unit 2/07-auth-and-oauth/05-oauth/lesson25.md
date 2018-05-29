##  OAuth with Flask

### Objectives:

By the end of this chapter, you should be able to:

*   Explain what OAuth is and diagram how a standard OAuth flow happens
*   Implement Twitter and Facebook login for an application
*   Understand how to architect a more complex schema with multiple authentication strategies

### OAuth

So far we have seen how to authenticate users through storing information in our database (username / password). Very commonly, we can delegate authentication to external providers (other websites where users have a username / password) and as long as the user successfully authenticates on another site, they will be authenticated on yours.

This type of authentication is extremely common and is used every time you see a button with a message like "Sign Up with Facebook" or "Sign In with Google." It is very common to rely on Facebook, Google, Twitter and many more providers for authentication. This type of authentication is also required if we would like to access specific information about our users on these networks.

Let's learn how this type of authentication works

1.  A user clicks a "Sign in with Facebook" button, which links to an application route, for example `/auth/facebook`.
    
2.  The server receives the request and responds with a redirect to Facebook's OAuth authorization URL. Each strategy (also called a provider) provides a URL to redirect the user to.
    
3.  The user now logs into Facebook and they are shown which permissions to give to your application (your email, access to your friends, etc.).
    
4.  If the user accepts these terms, Facebook will redirect the user back to a pre-configured URL. This is very commonly called a `callback URL` or `redirect URL`. In the query string of the callback URL, an authorization code will be included which your application uses to make authorized requests to the Facebook API on behalf of the authenticated user.
    

### Using Flask OAuthlib

To get started using OAuth, we will be using a module called `flask_oauthlib` You can read more about it [here](https://flask-oauthlib.readthedocs.io/en/latest/).

~~~~
mkvirtualenv flask-oauth
pip install flask psycopg2 flask-sqlalchemy Flask-OAuthlib ipython
~~~~

Head over to [https://apps.twitter.com/](https://apps.twitter.com/) and create a new application. make sure your callback url is `http://localhost:5000/auth/twitter/callback`. You can give the application whatever name, description, and URL you want.

~~~~
from flask import Flask, request, url_for, session, flash, redirect
from flask_oauthlib.client import OAuth

app = Flask(__name__)
oauth = OAuth()

app.config['SECRET_KEY'] = 'ill never tell' # this should be hidden as well!

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='GET YOUR OWN!',
    consumer_secret='GET YOUR OWN!'
)

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/auth/twitter/callback')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('welcome')
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    # add some information to the session
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    return redirect(next_url)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/welcome')
def welcome():
    from IPython import embed; embed() # take a look at what's in the session!
    return "WELCOME!"

# Try to add facebook now! https://flask-oauthlib.readthedocs.io/en/latest/client.html#oauth1-client

if __name__ == '__main__':
    app.run(debug=True)
~~~~

### Architecture for managing multiple social authentication strategies

As you start to include multiple strategies (providers for authentication), structuring your schema becomes a bit more challenging. As we have multiple ways of creating a user, we do not want to put all that information in a single table, we'd ideally need to normalize that information and create another table!

This association would be a 1:M and is commonly listed as one user has many identities. These identities can be from all of your providers (google, facebook, github etc). While this schema works, it is a challenge sometimes to make sure you do not create duplicate users and that one user maintains multiple identities. So how can we make sure that we get the same user with multiple identities? A common approach is to use an email address to link accounts together. This does assume that a user has signed up with the same email for all of these providers that you are using, but there is not much more you can do on their behalf. You can read more about this architecture [here](http://stackoverflow.com/questions/6666267/architecture-for-merging-multiple-user-accounts-together).

When you're ready, move on to [Flask Authentication Exercises](/courses/intermediate-flask/flask-authentication-exercise)