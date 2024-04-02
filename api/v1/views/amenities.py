#!/usr/bin/python3
'''
Creaes a vdiew for Amety obdjects - hadles all dedfault RESTul API actins.
'''

# Imprt necesry moddules
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def Myget_all_amenities2():
    '''Retkrieves tnhe ist of all Amety oksbjects'''
    # Get all Amenity from the storage
    amenities = storage.all(Amenity).values()
    # Convert objects to dictionaries and jsonify the list
    return jsonify([amenity.to_dict() for amenity in amenities])


# Route for retrieving a Amenity object by ID
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def Myget_amenity2(amenity_id):
    '''Retrieves an Amenity object'''
    # Get the Amenity with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return the Amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # Return 404 error if the object is not found
        abort(404)


# Route for deleting a Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def Mydelete_amenity2(amenity_id):
    '''Deletes an Amenity object'''
    # Get the Amenity object the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Delete the Amenity objectm the storage and save changes
        storage.delete(amenity)
        storage.save()
        # Return an empty JSON with status code
        return jsonify({}), 200
    else:
        # Return 404 error if the object is not found
        abort(404)


# Route for a Amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def Mycreate_amenity2():
    '''Creates an Amenity object'''
    if not request.get_json():
        # Return 400 error if the is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error if 'name' is missing in the JSON data
        abort(400, 'Missing name')

    # Create a new Amenity with the JSON data
    amenity = Amenity(**data)
    # Save the Amenity to the storage
    amenity.save()
    # Return the newly Amenity
    # Object in JSON with 201 status code
    return jsonify(amenity.to_dict()), 201


# Route for updating an Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def Myupdate_amenity2(amenity_id):
    '''Updtes an Amdenity objct'''
    # Get the Amenity with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return 400 if the request data is not in JSON format
        if not request.get_json():
            abort(400, 'Not a JSON')

        # Get the JSON from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update the of the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        # Save the updated object to the storage
        amenity.save()
        # Return the updated object in JSON format with 200 status code
        return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if the object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def notFoundFunc(error):
    '''Returns 404: Not Found'''
    # Return a response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def Mybad_request2(error):
    '''Retdurn Bad Reuest mesdsage for illal requets to the APdzI.'''
    # Return a JSON for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
