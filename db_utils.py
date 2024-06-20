import mysql.connector
from config import USER, PASSWORD, HOST

DATABASE = 'tour_booking'


class DbConnectionError(Exception):
    pass


# Connect to the database
def _connect_to_db():
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=DATABASE
    )
    return connection


# Get available packages
def get_all_packages():
    try:
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
            SELECT id, title, daily_price
            FROM packages
            """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if cnx:
            cnx.close()

    return result


# Check date availability
def check_availability(date):
    is_available = False

    try:
        # Connect to the db
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = '''
            SELECT available FROM calendar
            WHERE id_date = '{}'
            '''.format(date)

        # Execute the query to find date
        cursor.execute(query)
        result = cursor.fetchall()
        # Close the cursor
        cursor.close()

        # Check availability
        # No entry in calendar means available, available == 1 is boolean for True
        if not result or result == 1:
            is_available = True
            print(f'{date} is available for bookings.')
        else:
            print(f'Sorry, {date} is no longer available for bookings.')

    except Exception:
        raise ConnectionError('Could not retrieve data from the database')

    finally:
        # Close existing connection
        if cnx:
            cnx.close()

    # Return the availability as Boolean value
    return is_available


# Add a booking
def book_package(from_date, duration, client_id, package_id):
    try:
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
                INSERT INTO bookings
                (from_date, duration, client_id, package_id)
                VALUES
                ('{}', '{}', '{}', '{}')
                """.format(from_date, duration, client_id, package_id)

        cursor.execute(query)
        cnx.commit()

        # Retrieve the booking just created
        query_get_booking = """
                SELECT id FROM bookings
                WHERE client_id = '{}'
                AND from_date = '{}
                """.format(client_id, from_date)
        booking_id = cursor.execute(query_get_booking)
        cursor.close()

    except Exception:
        raise DbConnectionError("Booking failed")

    finally:
        if cnx:
            cnx.close()

    return booking_id


# Find a client's bookings
def find_client_bookings(client):
    try:
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
            SELECT 
                id,
                DATE_FORMAT(from_date, '%e/%m/%Y')
            FROM bookings
            WHERE client_id = '{}'
            ORDER BY from_date ASC
            """.format(client)

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if cnx:
            cnx.close()

    return result


# Delete a client's booking
def delete_client_booking(booking_id):
    try:
        # Connect to the db
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        # Delete reference in table calendar
        query_cal = """
            DELETE FROM calendar
            WHERE booking_id = '{}'
            """.format(booking_id)

        query_book = """
            DELETE FROM bookings
            WHERE bookings.id = '{}'
            """.format(booking_id)

        # Execute and commit the query to insert new client
        cursor.execute(query_cal)
        cursor.execute(query_book)
        cnx.commit()

        # Close the cursor
        cursor.close()

    except Exception:
        raise ConnectionError('Could not retrieve data from the database')

    finally:
        # Close existing connection
        if cnx:
            cnx.close()

    return


# Add new client
def add_client(fullname, email, phone):
    try:
        # Connect to the db
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
                INSERT INTO clients 
                (fullname, email, phone)
                VALUES ('{}','{}','{}')
                """.format(fullname, email, phone)

        # Execute and commit the query to insert new client
        cursor.execute(query)
        cnx.commit()
        print(f'{fullname} has been added to clients table')
        # Close the cursor
        cursor.close()

    except Exception:
        raise ConnectionError('Could not retrieve data from the database')

    finally:
        # Close existing connection
        if cnx:
            cnx.close()

    return


# Search for client id
def find_client_id(email):
    client_id = None
    try:
        # Connect to the db
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
                SELECT id FROM clients
                WHERE email = '{}'
                """.format(email)

        # Execute the query to find id
        cursor.execute(query)
        result = cursor.fetchone()
        # Close the cursor
        cursor.close()

        # Check if client in database
        if result:
            client_id = result[0]

    except Exception:
        raise ConnectionError('Could not retrieve data from the database')

    finally:
        # Close existing connection
        if cnx:
            cnx.close()

    return client_id


# Update the details of a client
def update_client_detail(client_id, detail, new_value):
    try:
        # Connect to the db
        cnx = _connect_to_db()
        cursor = cnx.cursor()

        query = """
            UPDATE clients
            SET {detail} = '{new_value}'
            WHERE id = '{client_id}'
            """.format(detail=detail, new_value=new_value, client_id=client_id)

        # Execute and commit the query to insert new client
        cursor.execute(query)
        cnx.commit()

        # Close the cursor
        cursor.close()

    except Exception:
        raise ConnectionError('Could not retrieve data from the database')

    finally:
        # Close existing connection
        if cnx:
            cnx.close()

    return





