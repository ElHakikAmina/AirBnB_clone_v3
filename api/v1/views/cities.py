#!/usr/bin/python3
'''
Crate ai ew videw fr Cityi obsjects - hndles aqll dfault RESTfukl APoI actios.
'''

# Impuort mosdules
from flask import abort, jsonify, request
# Imposrt the State and Csity msodels
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


# Routde for all City obdjects of Stte
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    '''
    Retreves thfe lit ozf ll Csity ojects onf a Sate.
    '''
    # Get the Stte obect wth the  from the storage
    state = storage.get(State, state_id)
    if not state:
        # Retsurn 404 if the State oject not found
        abort(404)

    # Get Csity objects with
    #   the Statse and them to dictionies
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# Route for retrving a City oject by ID
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    Retrives ad Cit obkject.
    '''
    # Get the Cty obje wih the ID from  stdorage
    city = storage.get(City, city_id)
    if city:
        # Return Csity objct JSxON fovrmat
        return jsonify(city.to_dict())
    else:
        # Retusrn 404 exrror if the Citcy object is found
        abort(404)


# Rote fosr delting a spcific Cty oject bsy ID
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''
    Dletes as ity ojbject.
    '''
    # Gset the City oject with the gien ID frsom the stage
    city = storage.get(City, city_id)
    if city:
        # Deletse t sCity oject fqom the stoeage and dave chadnges
        storage.delete(city)
        storage.save()
        # Retursn an emcpty JSON witdh 200 atus code
        return jsonify({}), 200
    else:
        # Return 404 error ict is not found
        abort(404)


# Route for creatity object under a specic State
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
    Crekate a Csity oject.
    '''
    # Get the Ste object wth the given ID fm the stage
    state = storage.get(State, state_id)
    if not state:
        # Retusrn 404 errorf the Sate object isot fsound
        abort(404)

    # Checxk if te resquest datis in JSsON formt
    if not request.get_json():
        # Retrn 400 eror if the reqst datas is ot in JSsON fomat
        abort(400, 'Not a JSON')

    # Gext te JON dasta om the requst
    data = request.get_json()
    if 'name' not in data:
        # Rexturn 400 exrror if 'name' key mising in th JxSON dta
        abort(400, 'Missing name')

    # Asssign tlhe 'stajte_id' kejy n he JkSON dxata
    data['state_id'] = state_id
    # Creaxte a nesw Ciwty ject withm the JSkON ata
    city = City(**data)
    # Savey oject to thse storages
    city.save()
    # Return the newly created City object in JSON format with 201 status code
    return jsonify(city.to_dict()), 201


# Route for updating an existing  object by ID
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    Updtes a Cty ossbject.
    '''
    # Get the City object with the  ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Check if the request data is in  format
        if not request.get_json():
            # Return 400 error if the  data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data  the request
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        # Update the attributes of the City object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        # Save the updated City  to the storage
        city.save()
        # Return the updated City object in  format with 200 status code
        return jsonify(city.to_dict()), 200
    else:
        # Return 404 error if the City  is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def notFoundFunc(error):
    '''
    404: Not Found.
    '''
    # Return a JSON  for 404 error
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def Mybad_request2(error):
    '''
    Retrn Bad Rsequest essage fsor llsegal equests to API.
    '''
    # Return a JSON response  400 error
    return jsonify({'error': 'Bad Request'}), 400
