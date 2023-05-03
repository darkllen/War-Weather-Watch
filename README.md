## War Weather Watch
War Weather Watch is an application for for predicting the probability of air alerts based on news and weather forecasts.

### Outer dependencies
* [ISW news](https://www.understandingwar.org/)
* [alarms API](https://api.ukrainealarm.com)
* [weather API](https://weather.visualcrossing.com) 
### Install

```shell
python -m venv .venv # create virtual env
. .venv/Scripts/activate
pip install -r requirements.txt
```

### Pipeline
* collect news
* collect weather data
* collect alarms data
* merge all data
* create dataset
* train model
* make predictions
* run api
* get predictions

### Modules

* db - database interaction
* ml - machine learning
* sources - working with outer dependencies
* static/ templates - UI

### Settings

For settings env file is used.
Example of such file: .env.example

### Deployment
Github actions are used for deployment.