# Solution to OAuth Part I - Questions

1. Before you add any kind of authentication, first answer the following questions:

- What is OAuth?
    - OAuth is a standard that describes how users can allow a website or application, known as the "client," to access a user account on another website or application, which we will term the "service." The client uses a unique string of text called an access token to access an account on the service, which is useful because the user's password is not disclosed to the client, allowing the user or service to modify or revoke the client's access at any time. OAuth breaks the service into two roles: the "authorization server," which handles the OAuth process including the granting of access tokens, and the "resource server," which allows the client to access user accounts if they present a valid access token. Practically speaking, a service's API will perform the authorization server and resource server functionality, and having two separate servers is not necessary.
- Why is there an OAuth 1 and OAuth 2?
    - OAuth1 was the first standard for OAuth. It has been largely replaced by its successor OAuth2, which is not backwards compatible with OAuth1.
- What is a client ID?
    - A client ID is a public and unique string of text that identifies the client to the authorization server. It is required to generate an access token.
- What is a client secret?
    - The client secret is a unique string of text which is a "secret"; it should only be known to the client and the authorization server. It is required to generate an access token.
- What is a redirect URL?
    - The redirect URL is known by many names such as "redirect URI" and "callback URL/URI." It is officially called the redirection endpoint. After a user authorizes the client to access their account on the service, the authorization server will redirect the user to a URL for the client application. The URL string of the redirect will contain an string of text called the "authorization code."
- What is an authorization code or grant?
    - The authorization code is used by the client to request an access token from the authentication server.
- What is an access token?
    - An access token allows the client to access a user's account on the service via the resource server.
- What is a refresh token?
    - A refresh token is an optional token that can be issued by the authorization server to the client so that the client can generate new access tokens. This is useful from a security perspective because the authorization server can set access tokens to expire quickly so that potential attackers only have a limited window of time to abuse the access token if they acquire one. Refresh tokens can last longer, because even if attackers gain access to the refresh token, they still require the client ID and client secret to get an access token to impersonate the user.
- Diagram / List the steps of an OAuth flow
    1. The client directs the user to the service's website so the user can authorize the client to access the service
    2. If the user authorizes the client app, the service uses the redirect URI/URL string to send the authorization code to the client
    3. The client uses the authorization code to request an access token from the authorization server
    4. The authorization server sends an access code to the client
    5. The client can then use the access code to access the user's account
