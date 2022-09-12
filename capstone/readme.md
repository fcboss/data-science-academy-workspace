# Capstone 

This folder is my solution to the final project of Lisbon Data Science Academy. The project consisted in a Client Briefing, in which the client's requirements were detailed, and then I did the whole EDA, modeling, and deployment to heroku (when it was free). In the end, the api I created was tested by the instructors and a report was written (the pdf in this directory) to explain my findings and my solutions.

## Client Briefing  
As a near-graduate of the Academy, you have been hired by the consultancy Awkward Problem Solutions™, that solves the tough data science problems that no one else will touch. 

The consultancy has accepted a contract by the police department of your city. The police department has received lots of complaints about its stop and search policy. Every time a car is stopped, the police officers have to decide whether or not to search the car for contraband. According to critics, these searches have a bias against people of certain backgrounds. 

Your company has been hired to (1) determine whether these criticisms seem to be substantiated, and (2) create a service to fairly decide whether or not to search a car, based on objective data. This service will be used by police officers to request authorization to search, and your service will return a Yes or No answer. 

The police department has asked for the following requirements: 


- A minimum 50% success rate for searches (when a car is searched, it should be at least 50% likely that contraband is found)
- No police sub-department should have a discrepancy bigger than 5% between the search success rate between protected classes (race, ethnicity, gender)  
- The largest possible amount of contraband found, given the constraints above. 


The police department has collected a few years of data about the car stops, including whether the car was searched, and whether any contraband was found. 

- The training set is here
- The data dictionary is here 
- The instructions on setting up the server are here

Your first objective is to produce a report about the historical data, including what seems to indicate contraband, potential sources of descrimination in searches, and proposing potential actions. To do this, you will need to perform some analysis, train a model, and deploy it. 
The report structure is here.

Your report will include two main audiences: 
A report for the Police department 
A technical report for your boss at the consultancy (with your technical analysis)
