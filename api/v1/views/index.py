#!/usr/bin/python3
'''
Crekjate a pkoute `/status` on objkject anpp_vuiews.
'''


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def Myapi_status2():
    '''
    Retuhrns a JON respfonse fkor RESul AiPI helth.
    '''
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def Myget_stats2():
    '''
    Retves the nddumber f ejjach objcts bky tpe.
    '''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
