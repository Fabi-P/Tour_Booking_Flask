import requests
import json
from datetime import datetime, timedelta

# Get today's date to validate user input
today = datetime.today()


# Choose what you want to do with the API
def choose_action():
    print('What would you like to do?\n')
    options = [
        '[1] - Look at all available tour packages',
        '[2] - Check availability',
        '[3] - Book a tour package',
        '[4] - Cancel a booking',
        '[5] - Register my details',
        '[6] - Update my details',
        '[7] - Exit'
    ]
    for option in options:
        print(option)

    print('\n')

    choice = 0
    while choice < 1 or choice > len(options):
        choice_input = input('Please insert the number of the chosen option: ')
        try:
            choice = int(choice_input)
        except:
            continue

    return choice


### PACKAGES ###

# Display packages as a table
def display_packages(packages):
    # Print the columns headers
    print('{:<5} {:<25} {:<10} \n'.format('N#', 'Package', 'Daily Price'))
    # Print the results in rows
    for package in packages:
        print('{:<5} {:<25} {:<10}'.format(package[0], package[1], '£ ' + package[2]))
    print('\n')
    return len(packages)


# Retrieve all packages
def get_packages():
    result = requests.get(
        'http://127.0.0.1:5002/packages',
        headers={'content-type': 'application/json'}
    )
    return result.json()


# Ask for valid package
def choose_package():
    num_packages = display_packages(get_packages())
    print('\n')
    package = 0
    try:
        while package not in range(1, num_packages + 1):
            package = int(input('Choose the number of the package you want to book: '))
    except:
        print('Input must be an integer')
        return choose_package()
    else:
        return package



### AVAILABILITY ###

# Ask user for desired tour starting date
def ask_starting_date(duration):
    input_date = ''
    while input_date == '':
        input_date = input('When would you like the tour to start? (dd/mm/yyyy): ')
    date = validate_date(input_date, duration)
    return date


# Check availability
def get_availability_for_date(date):
    result = requests.get(
        'http://127.0.0.1:5002/availability/{}'.format(date),
        headers={'content-type': 'application/json'}
    )
    return result.json()


# Validate user input for date
def validate_date(input_date, duration):
    # expected date format
    date_format = '%d/%m/%Y'

    # create date object with the date string
    try:
        from_date = datetime.strptime(input_date, date_format)
        if from_date <= today:
            print('Date must be in the future')
            raise Exception
        date = from_date
        for day in range(duration):
            # Check availability of each date
            if not get_availability_for_date(date.strftime('%Y-%m-%d')):
                print(f'Sorry, {date} is unavailable \n')
                raise Exception
            # Check next day
            date += timedelta(days=1)

    except Exception:
        print('Error occurred with the date')
        return ask_starting_date(duration)
    else:
        print('Period chosen is available')
        return from_date.strftime('%Y-%m-%d')


# Ask for tour duration
def ask_valid_duration():
    duration = 0
    try:
        while duration < 1:
            # Prompt user for tour desired duration
            duration = int(input('How many days would you like the tour to last for? (min: 1) '))
    except:
        print('Input must be an integer')
        return ask_valid_duration()
    else:
        return duration



### BOOKINGS ###

# Create a new booking
def create_booking(from_date, duration, client_id, package_id):

    booking = {
         "from_date": from_date,
         "duration": duration,
         "client_id": client_id,
         "package_id": package_id,
    }

    result = requests.post(
        'http://127.0.0.1:5002/bookings',
        headers={'content-type': 'application/json'},
        data=json.dumps(booking)
    )

    return result.json()


# Find a booking
def find_booking():
    client_id = ask_client_details()
    detail = {"id": client_id}

    result = requests.get(
        'http://127.0.0.1:5002/bookings',
        headers={'content-type': 'application/json'},
        data=json.dumps(detail)
    )
    return result.json()


# Cancel a booking
def cancel_booking():
    # Get all the bookings for this client
    all_bookings = find_booking()

    # Print the bookings found
    bookings_nums = []
    print('\n{:<15} {:<25}\n'.format('Booking ID', 'Booking Date'))
    for result in all_bookings:
        bookings_nums.append(result[0])
        print('{:<15} {:<25}\n'.format(result[0], result[1]))

    # User chooses which booking to delete
    delete_num = -1
    while delete_num not in bookings_nums:
        try:
            delete_num = int(input('Insert booking id you want to delete: '))
        except:
            raise Exception
    print(f'Booking number {delete_num} will be deleted')

    requests.put(
        'http://127.0.0.1:5002/bookings/{}'.format(delete_num),
        headers={'content-type': 'application/json'}
    )
    return



### USER DETAILS ###

# Add new user details
def add_new_client(name, email, phone):

    user = {
         "fullname": name,
         "email": email,
         "phone": phone
    }

    result = requests.post(
        'http://127.0.0.1:5002/register',
        headers={'content-type': 'application/json'},
        data=json.dumps(user)
    )

    return result.json()


# Find a registered user's id from email
def get_registered_client(email):

    detail = {"email": email}

    result = requests.get(
        'http://127.0.0.1:5002/register',
        headers={'content-type': 'application/json'},
        data=json.dumps(detail)
    )
    return result.json()


# Ask if user is registered
def is_new_client():
    # Ask if user is registered
    while True:
        history = input('Have you booked a tour with us before? (y/n): ').lower()
        if history == 'y' or history == 'yes':
            return False
        elif history == 'n' or history == 'no':
            return True


# Ask new client details
def ask_client_details():
    # If is a new client ask for details
    if is_new_client():
        fullname = ''
        email = ''
        phone = ''
        while fullname == '':
            fullname = input('Enter your fullname: ')
        while email == '':
            email = input('Enter your email: ')
        while phone == '':
            phone = input('Enter your phone number: ')
        # Add client to DB
        add_new_client(fullname, email, phone)
    else:
        email = ''
        while email == '':
            email = input('Enter your email: ')

    try:
        client_id = get_registered_client(email)
        print('Your id number is : ', client_id)
        if client_id is None:
            print('Email not found in the database')
            raise ValueError
        else:
            return client_id
    except ValueError:
        return ask_client_details()


# Update user details
def update_detail():
    # Retrieve client id
    client_id = ask_client_details()

    # Validate user input
    details = ['fullname', 'email', 'phone']
    detail = ''
    new_value = ''
    # Handle empty values
    while detail not in details:
        detail = input('What detail would you like to update? (fullname/email/phone) ')
    while new_value == '':
        new_value = input(f'What is your new {detail}? ')
        print(f'Your new {detail} is {new_value}')
    # Create a json with the details to update
    changes = {
        'client_id': client_id,
        'detail': detail,
        'new_value': new_value
    }

    result = requests.put(
        'http://127.0.0.1:5002/register',
        headers={'content-type': 'application/json'},
        data=json.dumps(changes)
    )

    return result.json()



### MAIN FUNCTION TO RUN PROGRAM ###
def run():
    # Welcome message
    message = """
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
                    Welcome to Tour Booking API\n
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
            """
    print(message)

    # Loops allows to make multiple choices (included exiting)
    while True:
        print('\n')
        option = choose_action()

        if option == 1:
            # Show all the packages and prices
            display_packages(get_packages())
        elif option == 2 or option == 3:
            # Check availability for period
            duration = ask_valid_duration()
            from_date = ask_starting_date(duration)
            if option == 3:
                # Book a tour package
                package = choose_package()
                client_id = ask_client_details()
                booking_id = create_booking(from_date, duration, client_id, package)
                print(f'Your booking is #: {booking_id}\n')
        elif option == 4:
            cancel_booking()
        elif option == 5:
            # Register details
            client_id = ask_client_details()
            print('Details recorded. Your user id is {}\n'.format(client_id))
        elif option == 6:
            update_detail()
        elif option == 7:
            # Safely exit the program
            print('\n Thank you for using Tour Booking API. Goodbye!')
            return


if __name__ == '__main__':
    run()
