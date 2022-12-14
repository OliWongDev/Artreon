# ENDPOINTS

## Disclaimer (Authorization):
Unfortunately, the authorization protocol I have tried to set up was unable to be completed in time. I took an extra day over the due date to see if I could get it to work because it would've been awesome but I was unable to discern between my users and artists for authorization purposes. My goal was to originally have two groups: Users (paid user & free user) who would be able to view +  comment on certain models and Artists (admin and non-admin) where the non-admin cannot post walkthroughs/emails/q&as but can post artworks. 

Upon trying to implement these authorization functions, taking a JWT identity (my only knowledge of authorization tools thus far in my career) would prove problematic. For example, if a user has the same id value as an artist, they would be able to access artist privileges such as posting an artwork; not the goal. I also struggled to access the inner values of the data which lead to me not being able to authorize a paid user over a free user despite emulating Coder Academy API examples that worked with the same logic.

My temporary but committed solution to this problem has been to set up 4 authorization functions: authorize_user, authorize_artist, authorize_precise_user, authorize_precise_artist. The first two allow any user/artist to make the request necessary and the last two allow the precise/user artist (somewhat reliably, id user and artist matching errors can occur) to make the correct adjustment on their account/comments/artwork/walkthroughs/q&as.

As such, I have left this section with a few directions so that the user of this API can view what they need to without ill-advised error codes coming up. I have sorted the routes into 4 categories Inauthenticated, Basic Authentication , User and Artist so that the person who would like to view this project can do so in a less-frustrating manner. The descriptions of the authentication/authorization are likely to be assumed for if the project was running as intended, and are going to be left as such for now.

- Inauthenticated --> No JWT tokens required to perform request.
- Basic Authentication --> JWT token required to perform request, but can be an artist or user. 
- User --> A user's JWT token is required to perform the request. Can be specific
- Artist --> An artist's JWT token is required to perform the request. Can be specific.

## Seed Helper:

This section is to assist the person using this API with easy access to credentials after seeding the database with the fake data. To log in, please enter the email and password in raw JSON format into POSTMAN with either '127.0.0.1:5000/auth/artist-login' or '127.0.0.5000/auth/user-login'. From there, use the bearer token returned in POSTMAN to properly perform the required requests.

FREE USER:
- "user_alias": "Free2View"
- "email": "free2view@gmail.com"
- "password": "freeloader"
- As a free user, they have no seeded comments or other content.

PAID USER:
- "user_alias": "BanksyInTraining"
- "email": "lucasbanks@gmail.com"
- "password": "iknowwhoheis"
- The user id is 4, they have posted artwork comments id 1 and 4 but no Q&A comments or walkthrough comments.

ARTIST:
- "artreon_alias": "GraphicGod"
- "email": "graphicgod@artreon.com"
- "password": "artist_password"
- The artist id is 1, and they have posted 4 artworks (id 1-4), 3 emails (id 1-3), 3 walkthroughs (id 1-3) and 3 Q&As (id 1-3)

## INAUTHENTICATED

### 127.0.0.1:5000/auth/register-user

*(1) Register User*

- METHODS = POST
- INPUTS = user_alias, first_name, last_name, email, has_subscription, password
- OUTPUT = user (201)
- AUTHENTICATION = NO
- AUTHORIZATION = NO
- ERROR HANDLING = Same email (409, Integrity Error), unauthorized (401)

![Image](/docs/1.png)

### 127.0.0.1:5000/auth/user-login

*(2) Login User*

- METHODS = POST
- INPUTS = email, password
- OUTPUT = email, bearer token (200)
- AUTHENTICATION = NO
- AUTHORIZATION = NO
- ERROR HANDLING = Invalid log in (404)

![Image](/docs/2.png)

### 127.0.0.1:5000/auth/artist-login

*(3) Login Artist*

- METHODS = POST
- INPUTS = email, password
- OUTPUT = email, bearer token (200)
- AUTHENTICATION = NO
- AUTHORIZATION = NO
- ERROR HANDLING = Invalid log in (404)

![Image](/docs/3.png)

## BASIC AUTHENTICATION

### 127.0.0.1:5000/users

*(4) Get all users*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All users seeded in the database and any created consequentially (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = n/a

![Image](/docs/4.png)

### 127.0.0.1:5000/users/<int:id>

*(5) Get single user*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Single user seeded in the database or any created consequentially (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = user id not in database (404, not found)

![Image](/docs/5.png)

### 127.0.0.1:5000/users/<string:user_alias>

*(6) Get user by alias*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Single user seeded in the database or any created consequentially (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = user_alias not in database (404, not found)

![Image](/docs/6.png)

### 127.0.0.1:5000/users/<string:user_alias>/comments

*(7) Get all user comments by alias*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All comments made by a specific user (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated (401)

![Image](/docs/7.png)
    
### 127.0.0.1:5000/artists

*(8) Get all artists*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All artists on database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = Inauthenticated (401)

![Image](/docs/8.png)

### 127.0.0.1:5000/artists/<int:id>

*(9) Get single artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Single artist on the database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = artist id not found in database (404, not found), inauthenticated (401)

![Image](/docs/9.png)

### 127.0.0.1:5000/artists/<string:artreon_alias>

*(10) Get admin artist (artreon_alias = GraphicGod) or single artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Single artist on database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = artist alias not found in database (404), inauthenticated (401)

![Image](/docs/10.png)

### 127.0.0.1:5000/artists/<string:artreon_alias>/artworks

*(11) Get artworks made by artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All artworks made by the artist selected (200)
- AUTHENTICATION = YES
- AUTHORIZATION = NO
- ERROR HANDLING = artist not found (404), inauthenticated (401)

![Image](/docs/11.png)

### 127.0.0.1:5000/artists/<string:artreon_alias>/qandas

*(12) Get Q&As made by artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All Q&As made by the artist (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated or free user (401), artist not found (404)

![Image](/docs/12.png)

### 127.0.0.1:5000/artists/<string:artreon_alias>/walkthroughs

*(13) Get walkthroughs made by artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All walkthroughs made by the artist (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated or free user (401), artist not found (404)

![Image](/docs/13.png)

### 127.0.0.1:5000/artists/<string:artreon_alias>/emails

*(14) Get emails sent by artist*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All emails sent by the artist (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated (401), artist not found (404)

![Image](/docs/14.png)

### 127.0.0.1:5000/artworks

*(15) Get all artworks*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All artworks on the database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated (401)

![Image](/docs/15.png)

### 127.0.0.1:5000/artworks/<int:id>

*(16) Get one artwork*
- METHODS = GET
- INPUTS = n/a
- OUTPUT = Retrieves a specific artwork in the database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = Unauthorized (401), Not found (404)

![Image](/docs/16.png)

### 127.0.0.1:5000/walkthroughs

*(17) Get all walkthroughs*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Retrieves all walkthroughs on the database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = NO
- ERROR HANDLING = Unauthorized (401)

![Image](/docs/17.png)

### 127.0.0.1:5000/walkthroughs/<int:id>

*(18) Get single walkthrough*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Retrieve all walkthroughs on database (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be paid user
- ERROR HANDLING = Unauthorized (401), walkthrough not found (404)

![Image](/docs/18.png)

### 127.0.0.1:5000/emails

*(19) Get all emails*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Returns all emails (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = inauthenticated (401)

![Image](/docs/20.png)

### 127.0.0.1:5000/emails/<int:id>

*(20) Get single email*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = Returns single email content to view (200)
- AUTHENTICATION = YES
- AUTHORIZATION = n/a
- ERROR HANDLING = unauthorized (401), email not found (404)

![Image](/docs/21.png)


## USERS

### 127.0.0.1:5000/users/<string:user_alias>

*(21) Update user details*

- METHODS = PUT/PATCH
- INPUTS = user_alias, first_name, last_name, email, has_subscription, password
- OUTPUT = New user details repeated (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same user
- ERROR HANDLING = user alias not found in database (404, not found), inauthenticated (401)

![Image](/docs/22.png)

*(22) Delete user*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Successful deletion message to repeat that the resource was deleted (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same user
- ERROR HANDLING = user alias not found in database (404, not found), inauthenticated (401)

![Image](/docs/23.png)

### 127.0.0.1:5000/artworks/<int:id>/comments

*(23) Create a comment on an artwork*

- METHODS = POST
- INPUTS = description(string)
- OUTPUT = Repeat of the comment (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be a paid user
- ERROR HANDLING = Unauthorized (401), artwork/comment not found (404)

![Image](/docs/24.png)

### 127.0.0.1:5000/artworks/<int:id>/comments/<int:artwork_comment_id>

*(24) Update own comment on an artwork*

- METHODS = PUT/PATCH
- INPUTS = description(string)
- OUTPUT = Repeat of comment (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same/paid user
- ERROR HANDLING = Unauthorized (401), artwork/comment not found (404)

![Image](/docs/25.png)

*(25) Delete own comment*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Successful deletion message(200) 
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same user
- ERROR HANDLING = Unauthorized (401), artwork/comment not found (404)

![Image](/docs/26.png)

### 127.0.0.1:5000/qandas

*(26) Get all Q&As*

- METHODS = GET
- INPUTS = n/a
- OUTPUT = All Q&As returned (200)
- AUTHENTICATION = YES
- AUTHORIZATION = Yes, must be paid user
- ERROR HANDLING = Unauthorized(401)

![Image](/docs/27.png)

### 127.0.0.1:5000/qandas/<int:id>/comments

*(27) Create comment on Q&A*

- METHODS = POST
- INPUTS = description (string)
- OUTPUT = Returned new Q&A comment (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be paid user
- ERROR HANDLING = Unauthorized(401), Q&A not found(404)

![Image](/docs/28.png)

### 127.0.0.1:5000/qandas/<int:id>/comments/<int:q_and_a_comment_id>

*(28) Update comment on Q&A*

- METHODS = PUT/PATCH
- INPUTS = description (string)
- OUTPUT = Returned updated Q&A comment (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same user
- ERROR HANDLING = Unauthorized (401), Q&A/comment not found (404)

![Image](/docs/29.png)

*(29) Delete comment on Q&A*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Returned successful delete message (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same user
- ERROR HANDLING = Unauthorized (401), Q&A/comment not found (404)

![Image](/docs/30.png)



### ARTISTS

#### 127.0.0.1:5000/auth/register-artist

*(30) Register Artist*

- METHODS = POST
- INPUTS = artreon_alias(str), password(str), email(str), artist_bio(str)
- OUTPUT = artist (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be artist
- ERROR HANDLING = same email, artreon_alias(409, Integrity Error), unauthorized(401)

![Image](/docs/36.png)

#### 127.0.0.1:5000/artists/<int:id>

*(31) Update artist details*

- METHODS = PUT/PATCH
- INPUTS = artreon_alias(string), password, email, artist_bio
- OUTPUT = Returns the new output (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = artist not same artist (401), artist not found (404), inauthenticated (401)

![Image](/docs/37.png)

*(32) Delete artist*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Returns deletion message (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = artist not same artist (401), artist not found (404)

![Image](/docs/38.png)

#### 127.0.0.1:5000/artworks

*(33) Create an artwork*

- METHODS = POST
- INPUTS = artwork_name(string), description(string)
- OUTPUT = Artwork created successfully message (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES must be an artist
- ERROR HANDLING = Unauthorized (401)

![Image](/docs/39.png)

#### 127.0.0.1:5000/artworks/<int:id>

*(34) Update an artwork*

- METHODS = PUT/PATCH
- INPUTS = artwork_name(string), description(string)
- OUTPUT = New artwork output (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = Unauthorized (401), Not found (404)

![Image](/docs/40.png)

*(35) Delete an artwork*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Successful deletion message (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = Unauthorized (401), Not found (404)

![Image](/docs/41.png)

#### 127.0.0.1:5000/qandas

*(36) Post Q&A*

- METHODS = POST
- INPUTS = q_and_a_content(string)
- OUTPUT = Returned Q&A (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be artist
- ERROR HANDLING = Unauthorized(401)

![Image](/docs/42.png)

#### 127.0.0.1:5000/qandas/<int:id>

*(37) Delete Q&A*

- METHODS = DELETE
- INPUTS = n/a
- OUTPUT = Successful delete message (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = Unauthorized(401), Q&A not found(404)

![Image](/docs/43.png)

*(38) Update Q&A*

- METHODS = PUT/PATCH
- INPUTS = q_and_a_content (string)
- OUTPUT = Returned Q&A (200)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be same artist
- ERROR HANDLING = Unauthorized(401), Q&A not found(404)

![Image](/docs/44.png)

#### 127.0.0.1:5000/emails

*(39) Create an email*

- METHODS = POST
- INPUTS = Email title (string), email content (string)
- OUTPUT = Success message for email created (201)
- AUTHENTICATION = YES
- AUTHORIZATION = YES, must be artist
- ERROR HANDLING = unauthorized (401)

![Image](/docs/45.png)