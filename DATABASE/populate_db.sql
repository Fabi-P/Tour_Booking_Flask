USE tour_booking;

-- Populate TABLE packages with data
INSERT INTO packages (title, daily_price)
VALUES
('Vikings adventures', 65.00),
('Castles and nobles', 105.50),
('Outlander locations', 58.00),
('Immerse into nature', 45.90),
('Food of the locals', 99.00),
('Sea side views', 83.20);


-- Populate with some client details
INSERT INTO clients
(fullname, email, phone)
VALUES
('Manuel Ross', 'manuel.ross@example.com', '+44 0744 389555'),
('Samantha Wright', 'samantha.wright@example.com', '+1 202 555 0192'),
('Luisa Martinez', 'luisa.martinez@example.com', '+33 6 12 34 56 78'),
('Jacob Johnson', 'jacob.johnson@example.com', '+61 412 345 678'),
('Emily Chen', 'emily.chen@example.com', '+81 80 1234 5678'),
('Daniel Thompson', 'daniel.thompson@example.com', '+49 1512 3456789'),
('Sophie Adams', 'sophie.adams@example.com', '+27 73 123 4567'),
('Maximilian Müller', 'maximilian.muller@example.com', '+39 345 678 9012');

-- Populate with bookings from the clients and packages inserted before
INSERT INTO bookings
(from_date, duration, client_id, package_id)
VALUES
('2024-04-20', 3, 1, 1),
('2024-05-10', 5, 2, 3),
('2024-06-15', 2, 3, 5),
('2024-07-08', 7, 4, 2),
('2024-08-22', 1, 5, 4),
('2024-09-05', 4, 6, 6),
('2024-10-17', 6, 7, 1),
('2024-11-30', 3, 8, 3);
