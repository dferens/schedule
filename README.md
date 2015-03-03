# schedule

Alternative to [rozklad.kpi.ua](http://rozklad.kpi.ua/)

## Requirements

* Python 3.x
* bower
* [Sass compiler](http://sass-lang.com/install)
* [babel](https://babeljs.io/)


## Installation
    git clone git@github.com:dferens/schedule.git && cd schedule
    virtualenv --python=`which python3` var/virtualenv && source var/virtualenv/bin/activate
    pip install -r requirements.pip
    ./manage.py bower install
    ./manage.py migrate

## Running

    $ ./manage.py runserver

## License

Copyright © 2015 Dmitriy Ferens

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
