# Description of your final project idea:
Trivia game app allowing users to play a trivia game similar to quizbowl. Users can both play their own questions that they submit as a question set, or play against pre-existing questions pulled from an API
Users can also track their statistics such as number of questions answered and accuracy which are displayed as a leaderboard globally

# Describe what functionality will only be available to logged-in users:
Question creation, statistics logging, leaderboard appearance. 

# List and describe at least 4 forms (CSRF protected):
- registration - create an account 
- login - access your account
- Question answer submission box
- Question creation page
- Profile modification page
- Category of question/ question difficulty selection - we ended up not doing this.

# List and describe routes/blueprints - at least 2 blueprints, each with at least 2 routes:
- Users
  - Registration 
  - Login
  - Profile Modification / View Profile
- Questions 
  - Gameplay screen
  - Question creation
  - List of submitted questions - moved from users blueprint
  - Leaderboard - moved from users blueprint

# Describe what will be stored/retrieved from MongoDB:
MongoDB will store things like user profile information, i.e. name. Pfp, etc. as well as gameplay statistics such as their accuracy, # of questions answered, etc.

Mongo will also store non-API, user generated questions that are linked to a player. I.E. if a user creations questions, all questions created by that user will be linked to a user profile and stored in mongo (most likely in a separate collection along with a foreign key / reference linking back to the profile, and vice versa)

# Describe what Python package or API you will use (different from projects) and how it will affect the user experience:
We will use a trivia API such as: https://opentdb.com/api_config.php to pull questions from for players to play against.
We will also use a variety of python packages d3py, seaborn, or matplotlib or other visualization tools to display details on user statistics, as well as leaderboard - didn't have time for this
