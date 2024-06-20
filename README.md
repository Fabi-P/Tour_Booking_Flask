# Tour Booking API

A Flask application designed for the management of a small Tour Agency.

## Setup
- [ ] Create the database using [this file](DATABASE/create_db.sql)
- [ ] Insert your MySQL host, user and password in the [config file](config.py)
- [ ] Check the [requirements](requirements.txt) and install missing packages with `pip install <package_name>`
- [ ] Run the [app.py file](app.py) to start Flask
- [ ] Run the file [main.py](main.py) and follow the instructions in the output console


## What can you do?
This **API** allows users to perform 7 different actions through the console:
1. Look at all available tour packages
2. Check availability of a chosen period in the future
3. Book a tour package
4. Cancel a booking
5. Register my details
6. Update my details
7. Exit

The **database** keeps a record of:
- bookings
- packages offered
- clients details
- availability

## How to use the Tour Booking API?
Once you have completed the [setup steps](#setup) you will know the program is running correctly when you see a welcome message outputted.
Use the output console to type your choices.
This API has been tested with most edge cases and contains error handling.
Incorrect input is verified and should not cause errors in the program.
> [!IMPORTANT]
> Please ensure your information [config.py](config.py) is correct and your flask server is running correctly.

## Limitations
This API has been designed for a tour company with a sole tourist guide.
Creating multiple bookings for the same date is not permitted.
While some input validation has been included, email and phone numbers have fewer restrictions.
This is to facilitate the use of mock data for demo purposes.

## Future developments
A login system could be implemented in the future to make the user experience more fluid.
An interface with buttons and forms could also simplify the process and overall improve user experience.
Endpoint could be developed to facilitate the use of data from the admin perspective.