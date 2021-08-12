-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE street = "Chamberlin Street" AND day = 28;

SELECT * FROM interviews WHERE day = 28 and month = 7;

SELECT * FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND month = 7;

SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND year = 2020 AND day = 28 AND month = 7;

SELECT * FROM bank_accounts JOIN people ON bank_accounts.person_id = people.id WHERE account_number = 28500762;

SELECT * FROM phone_calls WHERE year = 2020 AND day = 28 AND month = 7 AND duration <= 60;

SELECT * FROM people WHERE phone_number = "(375) 555-8161

SELECT * FROM airports WHERE city = "Fiftyville";

SELECT * FROM flights JOIN airports ON flights.origin_airport_id = airports.id WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id = 8;

SELECT * FROM passengers JOIN flights ON passengers.flight_id = flights.id WHERE passport_number = 5773159633;

SELECT * FROM people WHERE name = "Berthold";

SELECT * FROM passengers JOIN flights ON passengers.flight_id = flights.id WHERE passport_number = 2438825627;
