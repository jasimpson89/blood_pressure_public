# Intrdocution 

This simple plotly app plots my blood pressure as a function of other parameters I collect in a spreadsheet. It was my first practice attempt at making a data dashboard. I deployed the dashboard to Heroku. However, they have recently gotten rid of their free dyno's, which means that the dashboard still needs to be deployed to show it how it works. I have attempted to try to deploy the dashboard on AWS; however, I am having some rather annoying issues with my account verification. Once this is resolved, I will upload it there. 

# Usage 

You can still use the data dashboard if you clone this repo and run it locally or deploy it yourself. Simply clone the repo and run:

 ` ` `python 
 python app.py ` ` `

This will then start a web server in your console, and then you will need to visit the web address shown to see the dashboard running. Running it this way will use the test data in the repo. To provide your own blood pressure data (replacing the test data see below). This can be one of two ways:



1. ## Using a CSV

Within the repo there is a file called blood_pressure.csv. This has some test data in it so you can see the app working. Please fill out the data in the same format as the CSV file (and keep it saved as CSV!). 

3. ## Via onedrive - the recommended way

I created this method because I wanted my dashboard to run on the server without any intervention from myself, and I wanted the input data on my phone when I measured my blood pressure in the morning. I used an excel spreadsheet (in CSV format), which is saved on my onedrive. Within this app I download the CSV file which is then read by Pandas. Full documentation of this method is given [here](https://towardsdatascience.com/onedrive-as-data-storage-for-python-project-2ff8d2d3a0aa). Note that this method does rely on you making the CSV file in your onedrive "public" via creating a URL that in theory someone could guess, this introduces a security issue you may want to consider.

