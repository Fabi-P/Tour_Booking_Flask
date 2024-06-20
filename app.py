from flask import Flask, jsonify, request
from db_utils import (get_all_packages, check_availability, book_package,
                      find_client_bookings, delete_client_booking,
                      add_client, find_client_id, update_client_detail)

app = Flask(__name__)


# GETTING INFO ON PACKAGES AND PRICES
@app.route('/packages', methods=['GET'])
def get_packages_info():
    # Get packages options
    results = jsonify(get_all_packages())
    return results


# GET AVAILABILITY FOR A DATE
@app.route('/availability/<date>', methods=['GET'])
def get_availability(date):
    results = jsonify(check_availability(date))
    return results


# BOOK A TOUR PACKAGE
@app.route('/bookings', methods=['POST'])
def book_tour():

    # Get the json file from the post request
    new_booking = request.get_json()

    # Insert new booking into database
    booking_id = book_package(
        from_date=new_booking['from_date'],
        duration=new_booking['duration'],
        client_id=new_booking['client_id'],
        package_id=new_booking['package_id']
    )
    return jsonify(booking_id)


# GET A CLIENT'S BOOKINGS
@app.route('/bookings', methods=['GET'])
def get_client_bookings():
    client = request.get_json()
    result = find_client_bookings(client['id'])
    return jsonify(result)


# DELETE A BOOKING
@app.route('/bookings/<id>', methods=['PUT'])
def delete_booking(id):
    delete_client_booking(id)
    return


# REGISTER USER DETAILS
@app.route('/register', methods=['POST'])
def register_client():

    # Get the details of the new client
    new_client = request.get_json()

    # Insert new client into database
    add_client(
        fullname=new_client['fullname'],
        email=new_client['email'],
        phone=new_client['phone']
    )
    return new_client


# GET USER DETAILS
@app.route('/register', methods=['GET'])
def find_client():
    email = request.get_json()
    result = find_client_id(email=email['email'])
    return jsonify(result)


# UPDATE USER DETAILS
@app.route('/register', methods=['PUT'])
def update_details():
    # Get the json file from the put request
    changes = request.get_json()

    # Update new detail into database
    update_client_detail(
        client_id=changes['client_id'],
        detail=changes['detail'],
        new_value=changes['new_value']
    )

    return changes


if __name__ == '__main__':
    app.run(debug=True, port=5002)

