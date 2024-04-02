#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<Mystate_id2>', strict_slashes=False)
def states(Mystate_id2=None):
    """display the states and cities listed in alphabetical order"""
    states = storage.all("State")
    if Mystate_id2 is not None:
        Mystate_id2 = 'State.' + Mystate_id2
    return render_template('9-states.html', states=states, Mystate_id2=Mystate_id2)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
