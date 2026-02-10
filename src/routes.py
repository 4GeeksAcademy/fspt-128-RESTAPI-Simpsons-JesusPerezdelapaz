from flask import Blueprint, jsonify, request
from models import User, Character, Location, db

api = Blueprint("api", __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"Error": "User not found"})
    return jsonify(user.serialize())


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': "email, username and password is necessary"}), 400

    new_user = User(
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201



@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"Deleted succesfully"}), 200





@api.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if characters:
        response = [character.serialize() for character in characters]
        return jsonify(response), 200
    return jsonify({"Not found":"There are no characters yet"}), 404


@api.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"Error": "Character not found"})
    return jsonify(character.serialize()), 200


@api.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': "Name is necessary"}), 400

    new_character = Character(
        name = data['name'],
        quote = data['quote'],
        img = data['img']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 200





@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    if locations:
        response = [location.serialize() for location in locations]
        return jsonify(response), 200
    return jsonify({"Not found":"There aro no locations yet"}), 404


@api.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get(id)
    if not location:
        return jsonify({"Error": "Location doesnt exist"}), 404
    return jsonify(location.serialize()), 200


@api.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    if not data.get('name') or not data.get('use') or not data.get('town'):
        return jsonify({'error': "name, use, and town is necessary"}), 400

    new_location = Location(
        name=data['name'],
        use=data['use'],
        img=data['img'],
        town=data['town'],
        
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.serialize()), 201




@api.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    return jsonify(user.serialize_favorites()), 200


@api.route('/users/<int:id>/locations/<int:loc_id>', methods=['POST'])
def add_favorite_location(id, loc_id):
    user = User.query.get(id)
    location = Location.query.get(loc_id)

    if location in user.favorites_locations:
        return ({"info": "the location is already added"}), 400
    user.favorites_locations.append(location)
    db.session.commit()
    return jsonify({"info": "location added succesfully"}), 201



@api.route('/users/<int:id>/characters/<int:char_id>', methods=['POST'])
def add_favorite_character(id, char_id):
    user = User.query.get(id)
    character = Character.query.get(char_id)

    if character in user.favorites_characters:
        return ({"info": "the character is already added"}), 400
    user.favorites_characters.append(character)
    
    db.session.commit()
    return jsonify({"info": "character added succesfully"}), 201


@api.route('/users/<int:id>/characters/<int:char_id>', methods=['DELETE'])
def eliminate_character_fav(id, char_id):
    user = User.query.get(id)
    character = Character.query.get(char_id)

    if not user or not character:
        return jsonify({"error": "user or character not found"}), 404
    
    if character in user.favorites_characters:
        user.favorites_characters.remove(character)
        db.session.commit()
        return jsonify({"msg": "deleted successfully"}), 200
    
    
@api.route('/users/<int:id>/locations/<int:location_id>', methods=['DELETE'])
def eliminate_location_fav(id, location_id):
    user = db.session.get(User, id)
    location = db.session.get(Location, location_id)

    if not user or not location:
        return jsonify({"error": "user or location not found"}), 404
    
    if location in user.favorites_locations:
        user.favorites_locations.remove(location)
        db.session.commit()
        return jsonify({"msg": "deleted successfully"}), 200





