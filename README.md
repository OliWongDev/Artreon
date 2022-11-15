# Artreon

Welcome to Artreon! A model clone of the popular service Patreon where artists can express greater control over what content is viewable to paid and free subscribers. 

Artreon uses RESTful API practices to communicate data stored and incoming data in a relational manner, granting interactivity between the consumers of the service and the creators that populate it.

[Link to corrupted Github Repo for reviewing previous commits](https://github.com/OliWongDev/T2A2-Artreon)

[Link to Trello!](https://trello.com/b/XZPGM2wN/artreon)

## User Guide

To get Artreon up and running, these are the steps:

1. Open the terminal and git clone the Github repository mentioned above. 

```git clone git@github.com:OliWongDev/T2A2-Artreon.git```

2. Make a virtual environment inside the repository folder. Run this command in the terminal to do so when inside the folder. The virtual environment is the '.venv' folder that we set up. 

```python3 -m venv .venv```

3. Enter the virtual environment. This is so when we install the dependencies, we are not doing this on the global file system but we install what is necessary to work with what Artreon requires.

```source .venv/bin/activate```

4. Install the dependencies that are found in the requirements.txt file. This will allow you to use the libraries necessary to run Artreon.In the terminal type the following:

```pip install -r requirements.txt```

5. Rename the '.env.sample' to '.env'. This allows Artreon to find the environment variables necessary to unlock the database to be functional. This operation can be done in the command line inside the folder with:

```mv .env.sample .env```

6. Create a PostgreSQL Database. This database management system is what Artreon runs on and we need to make sure we have a database to put our future tables into. You will need to have the server running and enter into PostgreSQL first before making this command. Note that the database name can be anything but we will need it later.

```CREATE DATABASE databasename;```

7. If working correctly, the .env file should be available for you to enter code into. We need to enter in a secret JWT key that will be hidden but also a DATABASE URL that connects the application driver to the database. I have provided an example here:

```DATABASE_URL="postgresql+psycopg2://developer:1234@localhost:5432/artreon_db"```
```SECRET_KEY="Artreon"```

This would be valid to drop into your database provided the database was named "artreon_db" and there was a user with granted privileges called "developer" with a login password of '1234'.

8. Now we populate the database! Run these two commands which first creates the tables (using SQLAlchemy) and second populates with them with some fake data. 

```flask db create```

```flask db seed```

If successful, it should appear something like this!

![Successful seeded data](/docs/Seed%20success.png)

If you make changes or want to go back to the starting point, use:

```flask db drop```

This command drops all tables from the database, and then from there it is okay to create and seed again.

9. Run Flask to begin executing Artreon API requests.

```flask run```


10. Now you can send requests through POSTMAN! 

I have documented the routes in the [endpoints markdown file](/docs/endpoints.md) so that the user of the API may know what the possible endpoints they can request are. An example endpoint is:

```127.0.0.1:5000/artists```

This will take you to the artists route where a GET request in POSTMAN will find all artists on the database.

![Get artists](/docs/GET%20artists.png)

If some authentication or authorization protocols are causing ill-advised issues, please comment out the ```@jwt required``` decorator and the associated authorization function call underneath in the particular controller such as ```authorize_precise_user(id)```. This is done with CTRL + '/'.


## The Problem

For this particular problem I aimed to draw into what potential user stories for this service would look like from the three main viewpoints of the artist, the paid user and the free user. This is modelled from an AGILE framework where the user stories will dictate what the platform looks like so that the end result is something that is of actual benefit to them. 

### Free Users

"I want a service to view my favourite artist's art that they produce but I am not interested in learning how to make the art that they make"

The user story here is that the free user should be able to view the artworks and receive emails made if they have be authenticated, but they will not be able to view the walkthroughs/q&as that are associated with the artist's Artreon. By doing this, they are still a part of the in-house community to follow the artist's artistic journey. 

### Paid Users

"I want a service to view my favourite artist's art but I would also like to learn from them with walkthroughs/q&as to become a better artist myself. I would subscribe for this service."

The paid user is therefore defined as a user that is more invested in the personal learning journey side of the platform and less from a sole consumer standpoint. As such, the paid user is able to make comments, view walkthroughs/q&as and receive emails on top of the free user authorizations.

### Artist

"I want a service that allows me to handle what I allow my subscribers to view depending on their subscription. Further, I would like a service that requires authentication so that I can preserve my artwork from google searches and only for my loyal community.

The artist in this case acknowledges that with the depth of the internet, there is a need to have greater control over what is shared and publicly available for their content. It is their ultimate goal to monetise their art/knowledge and form a community of subscribers who can interact with the artist with certain privileges.

## Why do we need to solve this problem?

The problem is something that needs to be solved for a few key reasons: 

### Google Searches

As mentioned in the artist's user story, the range of access available in search engines means that it is quite easy for personal content to be taken and not credited. This is a barrier for an artist to post content on the internet, especially if their intention is for it to be preserved for certain users. 

With Artreon, the artist can post their artwork behind an authentication system so that it cannot be accessed by a public user. Further, with added tools the platform could allow the artist to properly monetise original custom pieces to people they actually want to sell to rather than attend to this service on a different platform.

### Online Community Building

Internet communities that are deeply intimate can transform a simple service into a platform of user satisfaction. We have seen many examples of social media sites that develop user access to people/ideas/content that is simply not available geographically. 

Artreon aims to develop a community of art-lovers of an individual artist into a thriving system that allows an artist to monetise their work and personally reach the people who made the decision to sign up and/or subscribe. The community is theirs, and it is not abased by what alternatives (in this case artworks) are seen on platforms such as Instagram.

### Interactive Learning

For a user who wants to not just be a consumer, but to learn skills from someone who's art you admire, Artreon is an attractive proposition. Paid users get to learn the exact methods/tools used to create awesome artwork with walkthrough videos and Q&A sessions. 

In future, added features could increase interactivity between the artist and protege such as reviews and booking 1 on 1 tutorial sessions. 

### Patreon as an alternative

The Artreon API is largely developed and inspired from Patreon (A large platform where creators and users come together to share exclusive content in exchange for a subscription). The use case for Patreon is broad, and potentially too broad for the user story. If we narrowed it down, Patreon is largely a one-way service where any type of creator releases what they would like and the subscribers remain simply consumers.

Artreon like mentioned above, identifies the need firstly to make an artist-centric platform and secondly to make sure that the space is kept intimate for buoyant communities to develop.

## Models

The models of the Atreon API are what SQLAlchemy uses to formulate the columns of the data table. In this section, I describe the 7 models that are present in the API and concisely what function they should serve. 

NOTE: If the relation to another table is (parent), this means that the model is a parent to the mentioned relation which would be a child. Put simply, this means that if a parent is deleted from the database, consequentially the child is also deleted. The models have been put in order of cascading like the seeded data where the first model is a parent and parent only. 

Syntactically, I found that using a back_populates reference would work for all relations in the database quite well and by using a cascade delete on the parent model to the child relation this process was relatively simple. I primarily used sets for one to many relations, the only exception being artworks to walkthroughs where uselist was False (one to one relation). 

Further, I condensed my models down from having a comments relation to artwork comments, walkthrough comments and Q&A comments. This enhanced my understanding of join tables as I had too many degrees of separation from an artwork comment mapping back to the user.

I also utilised Marshmallow schemas (ma) to assist with nested data from interrelated tables to my liking. For example, I wanted to show a GET route for the primary artist and with nesting the artworks/walkthroughs/q&as that they had done I was able to create a format that previewed what the artist had done without giving too much away. Marshmallow also proved valuable when validating fields such as password minimums (6) and certain characters being denied.

Here is an example of the walkthrough model which shows how the parent and child relationships are commonly defined throughout the app. The first section is the table name. The second segment is the exclusive fields related to a walkthrough with their constraints. The third section is the foreign keys held in the walkthroughs table. The final component is the relations to other tables with their parent/child criteria set up.

![walkthrough](/docs/Walkthrough%20Model.png)

### Artist

The artist model and role is the lynchpin of the API. The artist is the role that has administrative control overall as it is their platform to provide their own content. 

FIELDS:

- artreon_alias (defines the username which can be referenced in a route)
- password (used to log into the API and encrypted on get requests)
- email (email address used to log into the API)
- is_admin (A boolean to determine if the artist in question has administrative control or is simply there to post content)
- artist_bio (No word limit on how an artist can introduce their Artreon)

RELATIONS:

- Artwork (parent), Walkthrough (parent), Email (parent), Q&A (parent)

KEY NOTES/PRIVILEGES

- The artist can post artworks/walkthroughs/q&as/emails to their users.
- Only the same artist can update/delete their own content or details.
- Only the admin artist should be able to register a new user to their database.

### User

The user model is the primary consumer of the API data. They are on the platform to see what their favourite artist will produce and if they are paid, they are learners who want to see walkthroughs and Q&As to become better artists themselves. Their primary submission to the database is the ability to post comments on artworks, walkthroughs and Q&As.

FIELDS:

- user_alias (defines the username which can be referenced in a route)
- first_name
- last_name
- join_date (the datetime of today when the user is created)
- email (used to log in)
- has_subscription (Boolean to check if a user is free or paid)
- password (used to log into the API and encrypted on get requests)

RELATIONS:

- Artwork Comment (parent), Walkthrough Comment (parent), Q&A Comment (parent)

KEY NOTES/PRIVILEGES:

- The user can update/delete their own comments or account details.
- Paid users should have access to walkthroughs/Q&As.
- Free users can only view artworks and comments.

### Artwork

The artwork is the creator generated content that is the diamonds of the API. It is what the users want to be able to view and interact with. 

FIELDS:

- artwork_name
- description (allowed to be null)
- date (date posted)
- artist_id (foreign key to the artist who posted the artwork)

RELATIONS:

- Artist (child), Artwork Comment (parent), Walkthrough (child)

KEY NOTES:

- An artwork must be made by an artist so it has a foreign key to link it back.
- An artwork comment is to be deleted upon an artwork being deleted.
- A walkthrough may have a linked artwork, where the artist is showing the paid users how they made a specific artwork in the database.

### Walkthrough

FIELDS:

- description
- date (date posted)
- artist_id (foreign key linking back to the artist who posted the walkthrough)
- artwork_id (foreign key linking back to the artwork it derives from)

RELATIONS:

- Artist (child), Artwork (child), Walkthrough Comment (parent)

KEY NOTES:

- A walkthrough should only be accessed by paid users
- A walkthrough is derived from an artwork; it cannot exist without it.
- If a walkthrough is deleted, the walkthrough comments associated must also be deleted.

### Q&A

FIELDS:

- q_and_a_content
- date (date posted)
- artist_id (foreign key linking back to artist who posted q&a)

RELATIONS:

- Artist (child), Q&A Comment (parent)

KEY NOTES: 
- A Q&A should only be accessed by paid users.
- If a Q&A is deleted, the Q&A comments associated must also be deleted.

### Artwork Comment

FIELDS:

- description
- date (date posted)
- artwork_id (foreign key linking to specific artwork associated)
- user_id (foreign key linking to user who made the comment on the artwork)

RELATIONS:

- Artwork (child), User (child)

KEY NOTES:

- Serves as a join table between artworks and users with comments included.
- If either the artwork or the user are deleted, so is the comment associated.

### Walkthrough Comment

FIELDS:

- description
- date (date posted)
- walkthrough_id (foreign key linking to specific walkthrough associated)
- user_id (foreign key linking to user who made the comment on the walkthrough)

RELATIONS:

- Walkthrough (child), User (child)

KEY NOTES:

- Serves as a join table between walkthroughs and users with comments included.
- If either the walkthrough or the user are deleted, so is the comment associated.

### Q&A Comment

FIELDS:

- description
- date (date posted)
- q_and_a_id (foreign key linking to specific Q&A associated)
- user_id (foreign key linking to user who made the comment on the Q&A)

RELATIONS:

- Q&A (child), User (child)

KEY NOTES:

- Serves as a join table between q&as and users with comments included.
- If either the Q&A or the user are deleted, so is the comment associated.

## Relations

### Artist to Artwork/Walkthrough/Q&A/Emails

ASSOCIATION: One Artist to Many Artworks/Q&As/Emails

- One artist can make many artworks (e.g artwork1, artwork2, artwork3 are all attributed to user_id = 1)
- One artwork cannot be made by many artists

### Artwork to Artwork Comments, Walkthrough to Walkthrough Comments, Q&A to Q&A Comments

ASSOCIATION: One Artwork/Walkthrough/Q&A to Many "comments"

- One artwork/walkthrough/Q&A can hold many comments (e.g artwork_comment1, artwork_comment2, artwork_comment3 are all attributed to artwork1)
- One comment cannot map to multiple artworks/walkthroughs/Q&As.

### Artwork to Walkthrough:

ASSOCIATION: One Artwork to One Walkthrough (optional relation)

- One walkthrough must be attributed to one artwork
- One artwork does not have to have an associated walkthrough.

### User to Artwork Comments, Q&A Comments, Walkthrough Comments

ASSOCIATION: One User to Many "comments"

- One user can make many comments.
- Comments can only be attributed to one user.

## Entity Relation Diagram

![Entity Relation Diagram](/docs/ERD%20Artreon%20FINAL.drawio.png)

## Implementation of Relations

The relations are implemented directly mapping from both the models and the ERD. This means that there are 8 tables each holding data that makes up our database. 

![Database Tables](/docs/tables.png)

Inside the tables, we now have the seeded data. I've used the example of the users table which shows the primary key to differentiate the specific users as well as their details. This matches the fields designated in the ERD that have been run through our models constraints to check that they are valid.

![User Table](/docs/user_table.png)

### Implementation Example

Foreign keys are what makes our database relational. Without them, how will we be able to link our data to what it is writing to?

To directly show how the ERD matches the implementation relations we can use the example of a Q&A comment posted to a Q&A by a user. We know that a Q&A to a Q&A comment has a One to Many relationship as per the ERD, and the User to a Q&A comment relation is also One to Many. This means that an appropriate foreign key should be generated on Q&A Comments for both the user who made the comment, and the Q&A that now holds the comment. We will be taking user 4's (paid) bearer token by logging in, and then POSTing a comment on Q&A 1. As you will see, the POSTMAN return verifies that the user is mapped to the comment, and the comment is mapped to the Q&A.

BEFORE:

![q_and_a psql before](/docs/qandacommentsbefore.png)

![postman_before](/docs/q_and_a_comment_new.png)



AFTER:

![q_and_a psql after](/docs/qandapsqlafter.png)

![q_and_a postman after](/docs/qandacommentpostmanafter.png)

## PostgreSQL - The Database Management System of Choice

For this API, I have chosen PostgreSQL as my database management system (DBMS) for handling the queries of data that may be performed on the platform.

### Components of PostgreSQL

PostgresQL is a object-relational database that utilises structured query language (SQL) to make queries on the data that we have set up in our API. It is largely open-source would be able to scale my data to large lengths if the platform were to increase its artists and user information. It has a long history dating back since 1996, and has been proven to be an industry standard for large relational databases.

### Why for this project?

The reasons for why PostgreSQL was learned for my project are: relational database, JSON data acceptance, open-source, no license required, an industry standard and a personal desire to enhance my learning of it.

#### Relational Database

The API that I have built intends to take certain data and relate this to other data in the database. For that, our solution is a relational database that sets up rules to help preserve the integrity of our data. In a relational database, tables can be linked by foreign keys that help to set up the rules for new and seeded data being entered into our database. For example, in Artreon we cannot have an artwork being posted without an artist attached to it. Postgres makes these simple rules easy to actually implement and this is most useful for tracking bugs in our source code. 

Further, the ability to categorise our relations into simple tables initially means that we can handle complex interrelated queries depending on what the end users desire.

#### JSON Data

My API project will utilise JSON data as a return result in its skeleton format as of 14/11/22 and likely moving forward. As such, PostgreSQL handles this nicely when returning queries inside the code and from POSTMAN when requests are made. Because of this flexible data handling, PostgreSQL serves as a great tool for holding the API's data as well as its future potential to be adapted with different structured data objects.

#### Open Source

PostgreSQL is open-source meaning that it is licensed to users to use freely and change what they need to in order for their potential app to work the way they would like. Again, this proves that PostgreSQL is adaptable to future problems or solutions that arise for my API. Further, this means it is more likely to have a community behind that can help collaborate on this project or offer insight that might not be publicly available otherwise.

#### No License Required

Under PostgreSQL currently, there is no license required to use the service meaning that it is free for a beginner user such as myself to attempt to implement a RESTful API. This is unlike certain other DBMSs such as Oracle which require fees for a license. This is not a large issue for me as good software is always worth paying for, but to be able to use an industry standard DBMS with a low barrier to entry is a preferable choice before moving into different DBMSs for a more specific solution.

#### Industry Standard/Personal Interest

For my personal growth as a junior software developer, I am thrilled to have learnt how PostgreSQL handles relations and data to underpin a RESTful API. Through much diligence and occassionally frustration, I am proud to say that I feel comfortable working with PostgreSQL and working through all its idiosynchrasies.

Further, PostgreSQL is an industry standard tool for database management on relational databases. It has brought me a lot of confidence knowing that I can work with a relational database and bring that skillset to my future career.

### Drawbacks

There are some drawbacks to using PostgreSQL such as speed and 

### Low speed in certain cases

Compared to another relational DBMS MySQL, PostgreSQL has a lower reading speed (which is how long it takes to open files). Particularly in cases where the data is complex and/or long to read, PostgreSQL can struggle to keep up with other databases. Further, when compared to another DBMS Oracle it is "less productive" with the amount of transactions it can deal with per second. There are however workarounds that are available especially considering how it is open-source.

REFERENCES:

[PostgreSQL](https://www.ionos.com/digitalguide/server/know-how/postgresql/)
[PostgreSQL vs Oracle](https://hevodata.com/learn/postgresql-vs-oracle/#differences)

### Flexibility

PostgreSQL is a favourable solution for a wide range of database problems. However, it is possible that there are times where a simpler relational database would be preferable. MySQL offers a cloud-ready, beginner friendly, flexible with different data storage engines to integrate from and can be speedy for low-level queries. 

[PostgreSQL vs MySQL](https://www.integrate.io/blog/postgresql-vs-mysql-which-one-is-better-for-your-use-case/#whichprogramminglanguagesdotheysupport)

## SQLAlchemy - Object Relational Mapper

For this API, I have opted to use SQLAlchemy as the object relational mapper for my Python-coded query elements in order to work with my PostgreSQL database management system. 

### What is an Object Relational Mapper (ORM)

Firstly, we need to understand what an ORM is!

An ORM (Object Relational Mapper) is a database abstraction layer that permits source code objects (in this case Python) to be translated into SQL queries. If we are able to access the Flask application's database queries from Python, this is likely to be simpler and safer than utilising SQL queries directly. 

On top of this, we are able to define our models and schemas inside Python that will map to our database but also can be accessed when needed. This ultimately makes our code DRYer because we are able to make fundamental changes to our database structures when needed within the source code exclusively.

### How does SQLAlchemy work?

In the SQLAlchemy documentation, the developers describe two distinct components underneath the hood. 

The first is the Core which allows the expression of SQL in an object-oriented fashion meaning that we are able to use our Python code in Artreon in order to express the queries we want. The core also grants us the use of schemas which can be taken as the blueprints of how the data will appear. This part within our Flask application is taken care of within the core engine. This component is largely responsible for the DML (Data Manipulation Language) such as INSERT/UPDATE/DELETE that would equate to posting an artist, deleting a comment or updating a user's details.

Finally, SQLAlchemy has an in-built but optional object relational mapper library that is used primarily to work with any object models that are mapped to the schema. We have primarily used this package for our smaller scale application. 

REFERENCES:

[SQLAlchemy Features](https://www.sqlalchemy.org/features.html)

[SQLAlchemy Docs](https://docs.sqlalchemy.org/en/14/intro.html)

### Functionality of SQLAlchemy in Artreon

SQLAlchemy is used consistently within Artreon to define the models (db.model), map the relations to other tables (db.relationships), controllers (db.select), command line functionality to populate the database (db_commands.cli.command) and instantiate sessions to commit data to the database (db.commit, db.delete, db.add).

#### Models

SQLAlchemy models allow us to use Python classes to set what our tables of data should contain in our database. For example, the User class is a SQLAlchemy model that has columns detailing the user information in various datatypes that are applicable to both Python and SQL. The interoperability makes it simple for us to query a future table. This includes a low-level way to mark what foreign tables we will map our data to with the db.ForeignKeys utility. The models are also useful in allowing simple convertable constraints to our data such as not accepting a nullable entry for a row or imposing that a unit of data must be unique.

#### Relationships

Using the db.relationships function, we are able to define on the models what relations our table will map to and how it will handle the removal of data upon this relationship. For example, an artist if deleted should have their artworks removed. We are able to simply define what a parent/child relationship is with a cascade delete inside the parent model. We are also able to describe through our code what association each relation has to each other (One to Many for example) so that the database accepts that an artist can make many artworks, but one artwork cannot be made by many artists. 

#### Controller Selection Queries (DQL)

The controllers we use are essentially calling the route/request/query that we would like to perform and executing it. Inside this controller, we need to find what the query is so that we output the desired information. Using SQLAlchemy, we can call queries that return the JSON data we want, we can see if a database item exists and we can spring off of this to deny queries that do not meet the expectations. For example, authorization in Artreon relies heavily on the SQLAlchemy query to make sure that an artist is making a DML query on their manipulatable data e.g an artist cannot update another artist's details as SQLAlchemy is checking the artist id match to confirm that it is acceptable to do.

#### Command Line Seeding

In order for someone to check the functionality of the API, we have the option to manually POST data to the database. However, it is of valuable reward for us to have the ability to seed a database with fake data. This can be done through the command line interface as part of SQLAlchemy's package. If we manually make some data that can be seeded with "flask db seed" we can begin working on testing other queries that require data to be populated, particularly DML. For example, we will know if a model's fields aren't correct with this handy feature!

#### Sessions

Finally, we can use the db sessions to ensure our data is committed to the database in the event we use Pythonic Data Manipulation Language (DML). The session represents a "holding zone" for us to manipulate the data and the new data is flushed into the database when committed. In Artreon, we use db.commit to upload new data to the database when a user updates their comment on an artwork and it takes either the changed description or holds the old description under the session.

REFERENCES:

[SQLAlchemy Docs ORM Sessions](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#what-does-the-session-do)

### What are the advantages of SQLAlchemy? Why is it implemented in Artreon?

The advantages in particular that are relevant to Artreon are sanitisation, DRY code and compatibility:

#### Sanitisation/SQL Injections:

SQLAlchemy offers Artreon a simple-to-implement way of protecting against an SQL injection. An SQL injection is a common hacker technique of importing SQL language into an unintended field that can override the database's structure maliciously to where there is a risk of all data being deleted. This could have grave consequences for Artreon, particularly where an artist's entire collection of content is deleted.

By using Python objects to pass these queries, the window for this sort of attack to occur is contained within the Python code provided the API is set up correctly. 

REFERENCES:

[SQL Injections](https://www.w3schools.com/sql/sql_injection.asp)
[Essential SQLAlchemy (O'Reilly)](https://www.oreilly.com/library/view/essential-sqlalchemy-2nd/9781491916544/preface02.html)

#### DRY Code:

As we have used an MVC (Model, View, Controller) model in a modularised format, the fundamental structure of our data is largely located in one place. This promotes a simple system where repetition is minimized if we have to add new fields to our models that will roll out across the program. This is assisted by SQLAlchemy's use of python objects to define the models that integrate the backbone of our program.

#### Compatibility:

SQLAlchemy provides adaptable compatability with PostgreSQL, Python language and Marshmallow to create an API that is RESTful in Artreon. In future commits, it would be very possible to migrate this logic to other backend frameworks (e.g Django), DBMSs, deserializer integrators or other languages. Further, within the ORM itself SQLAlchemy can unintentionally assist to set up other n functions such as the authentication of users/artists and the authorization of paid users/free users

REFERENCES:

[Deploying with SQLAlchemy](https://towardsdatascience.com/building-and-deploying-a-login-system-backend-using-flask-sqlalchemy-and-heroku-8b2aa6cc9ec3)

### What are the key drawbacks to SQLAlchemy's ORM?

The key drawbacks to SQLAlchemy are that there is not much scope for complex data queries involving numerous tables however for the purposes of this relatively small Flask application these are not necessary.

There are also some concerns about efficiency in the official documentation for querying large data sets as the unit of work (synchronizing pattern in an SQLAlchemy session that stores the list of changes made to a series of objects before flushing to db) is inclusive of attributes on objects (e.g artwork.artwork_title) and for each row they must acquire a "last inserted id". This is described as a "large degree of automation" and that using the SQLAlchemy ORM is "not intended for high-bulk inserts".

REFERENCES:

[Educative.io](https://www.educative.io/courses/quick-start-full-stack-web-development/xoqE7wqKk93)
[SQLAlchemy Docs: Unit of Work](https://docs.sqlalchemy.org/en/14/glossary.html#term-unit-of-work)
[SQL Alchemy Docs: FAQ Question](https://docs.sqlalchemy.org/en/14/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow)

## Endpoints

[Check out the endpoints!](/docs/endpoints.md)

## Services Utilised

For the purposes of this particular criteria, I have not used any third-party services as far as I know beyond the "in-house" services that were demonstrated in the Coder Academy lectures. I have listed what I have used here but in the ![Minimum Viable Product Omissions section] I have mentioned services that I would like to use such as Mailtrap for when I return to this project.

### Flask

Flask is a web application microframework for Python that is paradigm-agnostic and allows us to run the Artreon API. It is helpful for us to run in Flask for a relatively small project as it connects well to the ORM (SQLAlchemy), builds routes with ease and is quite lightweight with little boilerplate code to get up and running. 

A useful feature has been operating in debug mode, where I can make changes and have the server reset automatically. The other great feature has been using the decorator "app" to set up routes that were simple to accept with POSTMAN requests.

Flask is appropriate for a smaller project such as this, however on a larger scale there could be difficulties that arise such as migration issues with more complex applications.

REFERENCES:

[Flask Pros and Cons](https://dev.to/detimo/python-flask-pros-and-cons-1mlo)

### BCrypt

BCrypt is a password hashing function that applies hashing to passwords on the Artist and User model. This is so that in the event of a malicious event like an SQL injection, where the PostgreSQL view can be accessed (otherwise I have hidden the passwords within the SQLAlchemy models/nested schemas) the user and artist passwords are largely unidentifiable.

This could be improved with salting, however it was a would-be-nice feature for the application I intended to develop.

### PostgreSQL

PostgreSQL is the relational database management system I have opted to use for Artreon. You can find more information about how it works and how it has been implemented [above](#postgresql---the-database-management-system-of-choice).

### POSTMAN

POSTMAN is an API platform that I used largely to review my endpoints. POSTMAN's simple request bar allowed me to enter in the route, the type of request I wanted to submit (e.g POST) as well as testing whether the bearer token I was using would allow authorization/authentication on certain routes.

### SQLAlchemy

SQLAlchemy is the ORM that was used to build the models and relations that make up the API. You can read more about the service generally and how it was used in Artreon [above](#sqlalchemy---object-relational-mapper).

In the Artreon source code, it is designated with the "db" object.

### Marshmallow

For the purposes of this project, the Marshmallow layer works to nest my schemas so that unnecessary information is removed (partnering with the SQLAlchemy models), return the JSON strings that appear in Postman by serializing and deserializing the objects and to do some basic validation on user and artist passwords (e.g a user password must be a minimum length of 6 characters, only containing numbers, letters and spaces) 

In the Artreon source code, it is designated by the 'ma' object.

REFERENCES:

[Marshmallow Official Docs](https://flask-marshmallow.readthedocs.io/en/latest/)

### Flask-JWT

For authentication/authorization, I used JSON web tokens with Flask-JWT to authenticate users/artists as part of the database as well as making authorizations on these two roles.

A token can be generated in POSTMAN from the login routes that is able to be used on other routes that require authorization/authentication, which allowed for a simple understanding as to whether my Python logic was working as intended or not.

### Trello

Whilst not part of the application itself, I should mention that a Trello board was created to track my progress in an agile manner by using cards, tasks, labels, checklists and due dates to help keep myself accountable during the project.

It was nice to have something to work through automatically and made the task of remembering what I had to do and when a lot easier. I look forward to continuing my use of it in the future. 

You can view the [Software Management Process](#software-management-process) below.

## Software Management Process

[Trello Board Link](https://trello.com/b/XZPGM2wN/artreon)

[Software Development Plan](/docs/software_development_plan.md)

## Minimum Viable Product Omissions

Under the time constraints and my limited knowledge with a new topic, I have made the following omissions from my original plan.

### Proper Authorization

Unfortunately, I could not work out how to authorize 8 different quantities of authorization due to time constraints and my inability to solve the problems. The particular issues were cross-allowing authorizations between the categories and having a function that located the id, but could not discern between artists and users. I made some left-field attempts at quickly learning Flask-Login + Flask-Authorization and learnt a lot from non-Coder Academy learning but ultimately I had to walk away from it for now. I hope to come back to this again when I have time and some new ideas. I'm listing the 8 here so that I can come back to it and pick up where I left off.

1. No authentication/authorization
2. Basic authentication ("Any free or paid user can access this content")
3. Paid user authorization ("Any paid user can access this content")
4. Precise user authorization ("The user who made the comment can delete it")
5. Artist authorization ("A registered artist can post an artwork to the Artreon")
6. Precise artist authorization ("A specific artist who made the artwork is permitted to update it")
7. Admin artist authorization ("The original artist can post walkthroughs/emails/Q&As)

I have mentioned what the end result of this is in my [Endpoints section](/docs/endpoints.md) so that what is working can be viewed accordingly.

I do think Flask-Login and Flask-Authorization from my basic research is what I'm looking for. Defining the roles and groups models to distinguish the paid/free user and the admin/non-admin artist seems within the scope of these extensions.

### Mailtrap

I wanted to implement a MailTrap.io email confirmation route that showed I post emails to the email addresses of the users. As my config was already deeply set up it would've be a lot of changes to make on an already late project. As such I have left that as an extra challenge for future me.

### Questions asked by users

I made the decision to chop off a potential "questions" table that could be populated by the users and that would log whether it had been answered in the Q&A. I realized this was a much more complex problem than I had initially thought and decided the project I have already done was sufficient feature-wise.

## Review

Overall, I am stoked to have put out what I have in the time given and I cannot say I didn't give it my all to try to work on these bonus features. Whilst I am disappointed that I will be taking a penalty for the late mark, I am appreciative of what the learning experience has been over a variety of new tools.

I could've picked a "simple" (relational databases aren't simple ;) ) project that would've met the RESTful conditions of the assignment in a minimal way however I think I have proven to myself that I am capable of launching into the deep end and I don't want to set a limit on what I am able to learn especially whilst I'm at Coder Academy.

However, I think next time I would be paying more attention to the deadlines and making these decisions sooner rather than waiting until it is too late to roll back. I also think that whilst I was present on campus to get assistance from Iryna, I could have communicated better with educators to bring them into my issues. My bad!

Finally, I hope you enjoy my project in its current state! There's plenty more where that came from :) 

