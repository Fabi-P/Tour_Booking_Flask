CREATE DATABASE IF NOT EXISTS tour_booking;

USE tour_booking;

CREATE TABLE IF NOT EXISTS packages(
	id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    daily_price DECIMAL (6,2)
);

CREATE TABLE IF NOT EXISTS clients(
	id INT PRIMARY KEY AUTO_INCREMENT,
    fullname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS bookings(
	id INT PRIMARY KEY AUTO_INCREMENT,
    duration INT NOT NULL,
    from_date DATE NOT NULL,
    client_id INT NOT NULL,
    package_id INT NOT NULL,
    CONSTRAINT fk_booking_client
		FOREIGN KEY (client_id)
		REFERENCES clients(id),
    CONSTRAINT fk_package
		FOREIGN KEY (package_id)
		REFERENCES packages(id)
);

CREATE TABLE IF NOT EXISTS calendar(
	id_date DATE PRIMARY KEY,
    available BOOLEAN DEFAULT 1,
    booking_id INT DEFAULT NULL,
    CONSTRAINT fk_booking
		FOREIGN KEY (booking_id)
		REFERENCES bookings(id)
);


-- Trigger that updates the calendar whenever a new booking is created
DELIMITER //
CREATE TRIGGER booked_calendar AFTER INSERT ON bookings
	FOR EACH ROW
    BEGIN
		DECLARE days INT;
        DECLARE adding_date DATE;
        SET days = NEW.duration;
        SET adding_date = NEW.from_date;

        duration: LOOP
			INSERT INTO calendar
			VALUES (adding_date, 0, NEW.id);
			SET adding_date = (SELECT DATE_ADD(adding_date, INTERVAL 1 DAY));
			SET days = days - 1;
			IF days = 0 THEN
			LEAVE duration;
			END IF;
		END LOOP;
	END //
DELIMITER ;
