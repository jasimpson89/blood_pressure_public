# Generates requirements for heroku
pip freeze > requirements.txt
# this pushes to heroku and deploy
git push heroku master