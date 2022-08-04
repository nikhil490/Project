# Environment Agency Real Time Flood-Monitoring

A simply app using python to monitor real time values of different measures per station obtained using Station ID (stationReference or notation)


## Description

* Search Using the Station ID eg: 1029TH,52207,531118,E21136,E2043
* The latest values, todays value and past 24 hours can be choosen. The default filter is past 24 hours.
* A table containing Values for each measures and Time
* Line Plots of each measures over time
* A table containing the important properties of the Station Measure is also included.

## Getting Started

### Dependencies

certifi==2022.6.15
charset-normalizer==2.1.0
click==8.1.3
colorama==0.4.5
cycler==0.11.0
Flask==2.2.0
fonttools==4.34.4
idna==3.3
itsdangerous==2.1.2
Jinja2==3.1.2
kiwisolver==1.4.4
MarkupSafe==2.1.1
packaging==21.3
Pillow==9.2.0
plotly==5.9.0
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2022.1
requests==2.28.1
six==1.16.0
tenacity==8.0.1
urllib3==1.26.11
Werkzeug==2.2.1


### Installing
After cloning the repository 
Please Run CLI commands :
* cd Projects
* pip install -r requirements.txt


### Executing program

* python -m flask --app main.py 
* Then use the link http://127.0.0.1:5000/ to access the application.
* Please see the webpage picture in the repository for a demo page.

## Authors

Contributors names and contact info

ex. Nikhil Baby   
ex. https://github.com/nikhil490/Project

## Acknowledgments

The Application uses Environment Agency flood and river level data from the real-time data API (Beta)
