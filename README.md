# Cafe-api
Cafe Wi-Fi Project: A Flask-based API for managing and retrieving information about cafes, including amenities like Wi-Fi availability, seating capacity, and more.


## Features

- **Random Cafe:** Endpoint to retrieve a random cafe from the database.
- **All Cafes:** Endpoint to retrieve all cafes ordered by name.
- **Search Cafe:** Endpoint to find cafes based on location.
- **Add Cafe:** Endpoint to add a new cafe to the database.
- **Update Cafe Price:** Endpoint to update the price of a cafe based on its ID.
- **Delete Cafe:** Endpoint to delete a cafe from the database.

## Installation

1. Clone the repository:


2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the SQLite database:

   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. The application will be running at `http://127.0.0.1:5000/`.

## API Endpoints

- **GET `/random`**: Retrieve a random cafe.
- **GET `/all`**: Retrieve all cafes.
- **GET `/search?loc=<location>`**: Search cafes by location.
- **POST `/add`**: Add a new cafe.
  - Required fields in JSON body: `name`, `map_url`, `img_url`, `loc`, `sockets`, `toilet`, `wifi`, `calls`, `seats`, `coffee_price`.
- **PATCH `/update-price/<cafe_id>?new_price=<new_price>`**: Update the price of a cafe.
- **DELETE `/report-closed/<cafe_id>?api-key=<api_key>`**: Delete a cafe (requires correct API key).

## Usage

- Use tools like Postman to interact with the API endpoints.
- Ensure correct JSON format for POST requests (`Content-Type: application/json`).

