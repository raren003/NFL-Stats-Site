# Nfl Stats Site Project

Website built using the Django framework for analyzing NFL player stats based on data found on the [NFL Play Statistics 
dataset](https://www.kaggle.com/toddsteussie/nfl-play-statistics-dataset-2004-to-present) found on Kaggle.

This README primarily focuses on the contributions made by myself (Robert Arenas).

## Table of contents

## General Info

Originally created as project for CS180 - Intro to Software Engineering course at University of California Riverside. 
Project includes contributions from Robert Arenas, Eduardo Rocha, Kyle Dean, and Ford St. John under the group name 
Team 42.

The project involves the creation of an application utilizing a custom in memory data store in combination with a 
client-server architecture in order to display analytical data. The goal is to build an in-memory
data store with a layered client-server architecture. The data store will be popuated from a public dataset in csv 
format and  provide predefined data analytics, of our choice.

Project requirements/restrictions are as followed:
1. Dataset must be sufficiently large and contain multiple csv files each containing multiple columns.
2. Use of 3rd party libraries/frameworks should be limited
   1. Database and CSV Parsers are NOT allowed
   2. JSON parsers and visualization libraries are allowed
3. Any language and platform (mobile/web/desktop for the client) may be used

## Demo

## Technologies used

We are using Django as the general framework for our web application. 

## Setup

1. Clone repository and extract
2. Open the outer nfl_site directory containing manage.py in a terminal
3. Run program using flowing command:
   ```{python}
   python manage.py runserver
   ```
    1. **Note:** program built using python 3.8.3
    
This will host our web application on your local machine on a local port (default to 8000)
