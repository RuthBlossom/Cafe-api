from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
import random

# Initialize the Flask application
app = Flask(__name__)

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


# Define the Cafe model
class Cafe(Base):
    __tablename__ = "cafes"  # Name of the table in the database

    # Define columns for the table
    id = Column(Integer, primary_key=True)  # Unique ID for each cafe
    name = Column(String(250), unique=True, nullable=False)  # Name of the cafe
    map_url = Column(String(500), nullable=False)  # URL of the cafe's location on a map
    img_url = Column(String(500), nullable=False)  # URL of an image of the cafe
    location = Column(String(250), nullable=False)  # Physical location of the cafe
    seats = Column(String(250), nullable=False)  # Number of seats available
    has_toilet = Column(Boolean, nullable=False)  # Whether the cafe has a toilet
    has_wifi = Column(Boolean, nullable=False)  # Whether the cafe has WiFi
    has_sockets = Column(Boolean, nullable=False)  # Whether the cafe has power sockets
    can_take_calls = Column(Boolean, nullable=False)  # Whether the cafe is suitable for taking calls
    coffee_price = Column(String(250), nullable=True)  # Price of a coffee

    # Method to convert the model instance to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Create the database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Render the home page
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    # Select all cafes from the database
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()

    # Select a random cafe from the list
    random_cafe = random.choice(all_cafes)

    # Return the random cafe as a JSON response
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    # Select all cafes from the database and order by name
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()

    # Return all cafes as a JSON response
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_cafe_at_location():
    # Get the location query parameter from the request
    query_location = request.args.get("loc")

    # Select all cafes with the specified location
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()

    # If cafes are found at the location, return them as a JSON response
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        # If no cafes are found, return an error message
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=["POST"])
def post_new_cafe():
    try:
        data = request.json  # Assuming JSON data is sent
        new_cafe = Cafe(
            name=data['name'],
            map_url=data['map_url'],
            img_url=data['img_url'],
            location=data['loc'],
            has_sockets=bool(data.get('sockets')),
            has_toilet=bool(data.get('toilet')),
            has_wifi=bool(data.get('wifi')),
            can_take_calls=bool(data.get('calls')),
            seats=data['seats'],
            coffee_price=data['coffee_price']
        )

        db.session.add(new_cafe)
        db.session.commit()

        return jsonify(response={"success": "Successfully added the new cafe."}), 201  # 201 Created
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify(error={"message": str(e)}), 500  # 500 Internal Server Error



# Endpoint to update the price of a cafe based on its ID
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    # Get the new price from the query parameters
    new_price = request.args.get("new_price")

    # Get the cafe by its ID
    cafe = db.session.get(Cafe, cafe_id)

    # If the cafe is found, update the price and commit the changes
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # If the cafe is not found, return an error message
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# Endpoint to delete a cafe based on its ID
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Get the API key from the query parameters
    api_key = request.args.get("api-key")

    # Check if the API key is correct
    if api_key == "TopSecretAPIKey":
        # Get the cafe by its ID
        cafe = db.session.get(Cafe, cafe_id)

        # If the cafe is found, delete it and commit the changes
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            # If the cafe is not found, return an error message
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        # If the API key is incorrect, return a forbidden error message
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






