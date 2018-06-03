# OAuth

1. Before you add any kind of authentication, first answer the following questions:

- What is OAuth? 
- Why is there an OAuth 1 and OAuth 2?
- What is a client ID?
- What is a client secret?
- What is a redirect URL?
- What is an authorization code or grant?
- What is an access token?
- What is a refresh token?
- Diagram / List the steps of an OAuth flow

2. Add OAuth to your users and messages app! Allow users to log in with their email and password as well as log in through Twitter! 

### Brendon's Notes
- This article has a good description of OAuth2, including articles and helpful diagrams: https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2
- I have implemented the part 2 solution with Flask-Dance instead because Flask-OAuth is currently unmaintained
    - Flask-Dance Twitter quickstart documentation: https://flask-dance.readthedocs.io/en/latest/quickstarts/twitter.html
    - Flask-Dance requires Twitter's callback URL to be `http://localhost:5000/login/twitter/authorized
    - In order to use Flask-Migrate with Flask-Dance, the alembic migration script must be edited to `import sqlalchemy_utils` to create the token column provided by the `OAuthConsumerMixin`
    - This Github Gist provides an example of how to enable two forms of authentication, traditional password authentication and third party authentication via Flask-Dance, for each user