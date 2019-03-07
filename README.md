# TweetExtractor

This is a flask based web app which takes as input a Twitter UserName from the user and then extracts the tweets from the user account corresponding to it.
These tweets are then provided as an input to a machine learning model which separates out the tweets corresponding to the need and availability of resources.
This app can be quite useful during a disaster as can collect information about people in trouble during a disaster. It can identify the people in trouble and then the help can be sent to them.

Installation
1. Download the files
2. Install the packages given in requirements.txt

Procedure to Run
1. Create a python virtual environment
2. Command = "export FLASK_APP=application.py"
3. Command = "flask run"
4. The app will run on your localhost. Go to the local-host address.
5. Type username in the box
6. Click Classify
7. The tweets related to need and availability will be shown in corresponding section
