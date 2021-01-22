# Nfl Stats Site Project

Website built using the Django framework for analyzing NFL player stats based on data found in the [NFL Play Statistics 
dataset](https://www.kaggle.com/toddsteussie/nfl-play-statistics-dataset-2004-to-present) found on Kaggle.

This README primarily focuses on the contributions made by myself (Robert Arenas).

## Table of Contents

* [General Info](#general-info)
* [Demo](#demo)
* [Technologies Used](#technologies-used)
* [Setup](#setup)

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
2. Any language and platform (mobile/web/desktop for the client) may be used   
3. Use of 3rd party libraries/frameworks should be limited
   1. Database and CSV Parsers are NOT allowed
   2. JSON parsers and visualization libraries are allowed


Overall the site allows for the viewing of NFL statistics by combine, passing, rushing, receiving, and standings metrics.

My individual contribution to the site was the receiving section of the website. The receiving section allows for the viewing
and editing of an individual players total receiving yards, average receiving yards per receiving play, and total 
receiving plays metrics. Additionally, the top n players by average receiving yards per receiving play may be viewed on 
a scatter plot and table. There is also a section for adding new players or deleting existing players.

My other contribution, in collaboration with teammate Kyle Dean, was creating a custom, built from scratch, csv parser 
that converts our dataset csv files into python dictionaries. These dictionaries would serve as our in memory datastore 
for computing our data analytics.

## Demo

The following video demonstrates the features implemented by myself on the receiving statistics section of our website.

[Demo Video](https://drive.google.com/file/d/12KRO8oBZwXCXaGcKTSQImJ2CXCGJU_5s/view?usp=sharing)

## Technologies Used

1. Frameworks
   1. [Django](https://www.djangoproject.com/) - Web framework
   2. [Boostrap 3.3.7](https://getbootstrap.com/docs/3.3/) - CSS/Javascript framework
2. Languages
   1. Python
   2. HTML/CSS
   3. Javascript
3. 3rd party python libraries
   1. [Pandas](https://pypi.org/project/pandas/)
      1. Used to convert python dictionaries containing statistical information into Pandas dataframes for use with 
         plotly library
   2. [Plotly](https://plotly.com/python/getting-started/)
      1. Used to convert Pandas dataframes into visually appealing graphs
   3. Other libraries need to run site, but are not used by the receiving section of the website
      1. [numpy](https://pypi.org/project/numpy/)
      2. [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
      3. [googledrivedownloader](https://pypi.org/project/googledrivedownloader/)
   
## Setup

1. Clone repository and extract
2. Ensure the necessary 3rd party python libraries, listed above, are installed on host machine  
3. Open the outer nfl_site directory containing manage.py in a terminal
4. Run program using flowing command:
   ```{python}
   python manage.py runserver
   ```
    1. Program built using **python 3.8.3**
5. This will host our web application on host machine on a local port (default to 8000)

**NOTE**: If Not prompted or unable to download dataset when first running site perform the following steps.
1. Download dataset from [here](https://www.kaggle.com/toddsteussie/nfl-play-statistics-dataset-2004-to-present)
2. Extract all csv files from dataset and place them in the NFL-Stats-Site/nfl_site/static/archive directory.
