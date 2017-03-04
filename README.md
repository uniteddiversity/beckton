##Installing a local development copy

Must have installed:

Node
Python + virtualenv
MongoDB


Clone this repository and then:

```
virtualenv .
source bin/activate
pip install -re requirements.txt
npm install
```


##Running a local copy

Run the web app:

```
source bin/activate
export SETTINGS='config.DevelopmentConfig'
export GOCARDLESS_ACCESS_TOKEN='ENTER YOUR GO CARDLESS ACCESS TOKEN'
python server.py
```

Run the message que (in a separate terminal):
```
source bin/activate
export SETTINGS='config.DevelopmentConfig'
export TWILLIO_SID='ENTER YOUR TWILLIO SID'
export TWILLIO_AUTH_TOKEN='ENTER YOUR TWILLIO AUTH TOKEN'
export TWILLIO_PHONE_NUMBER='ENTER YOUR TWILIO PHONE NUMBER'
celery -A beckton.celery worker
```

Run the assets compiler (in a separate terminal):

```
grunt
```

##Running tests locally

```
source bin/activate
export SETTINGS='config.TestingConfig'
python tests.py
```

##Management commands

###Reset everything
```
python manage.py reset
```




## Notes:
using older version for now:
http://foundation.zurb.com/sites/docs/v/5.5.3/javascript.html