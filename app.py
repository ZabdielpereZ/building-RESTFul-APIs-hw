from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection, Error


app = Flask(__name__)
ma = Marshmallow(app)

# Create the Customer table schema, to define the structure of our data that we expect to send and receive
class MembersSchema(ma.Schema):
    id = fields.Int(dump_only=True)  # dump_only means we don't have to input data for this field
    members_name = fields.String(required=True)  # to be valid, this needs a value
    email = fields.String()
    phone = fields.String() 

    class Meta:
        fields = ("id", "members_name", "email", "phone")

members_schema = MembersSchema() # allows us to validate data for single customers when we send and receive
members_schema = MembersSchema(many = True)  # allow us to validate multiple rows or entries from our customer table at the same time

class WorkoutSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    duration = fields.DateTime()
    members_id = fields.Int()

class Meta:
        fields = ("id", "members_name", "email", "phone")

workout_schema = WorkoutSchema()
workout_schema = WorkoutSchema(many = True)
#=====================================================

# CRUD Operations
# Create (POST)
# Retrieve (GET)
# Update (PUT)
# Delete (DELETE)

#======================================================

# route to Get all Workout Sessions
@app.route("/workout_sessions", methods = ['GET'])
def get_workout_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM workout_sessions;"

            cursor.execute(query)

            workout_sessions = cursor.fetchall()

        except Error as e:
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workout_schema.jsonify(workout_sessions)

# route to Get a single Workout Session by ID
@app.route("/workout_sessions/<int:workout_id>", methods = ['GET'])
def get_workout_session(id):
    pass


# Create a new member with a POST request
@app.route("/members", methods = ['POST'])
def add_member():
    try:
        member_data = members_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            new_member = (member_data['members_name'], member_data['email'], member_data['phone'])

            query = "INSERT INTO members (members_name, email, phone) VALUES (%s, %s, %s);"

            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message': 'New member created successfully!'}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500

# route to GET all customers
@app.route('/members', methods = ['GET'])
def get_members():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)

            query = "SELECT * FROM members;"

            cursor.execute(query)
            members = cursor.fetchall()

        except Error as e:
            print(f"error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members)

# route to POST changes based on different query parameters
@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = members_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({'error': 'Member not found.'}), 404
            
            update_member = (member_data['members_name'], member_data['email'], member_data['phone'], id)

            query = "UPDATE members SET members_name = %s, email = %s, phone = %s WHERE id = %s;"
            cursor.execute(query, update_member)
            conn.commit()

            return jsonify({'message': f'Member {id} updated successfully!'}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500

# a routes to DELETE a customers
@app.route("/members/<int:id>", methods = ['DELETE'])
def delete_members(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            check_query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({'error': 'Member not found.'}), 404
            
            query = "DELETE FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({'message': f'Successfully deleted member {id}'}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500



if __name__ == '__main__':
    app.run(debug= True)