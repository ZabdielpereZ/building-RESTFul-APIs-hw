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

member_schema = MembersSchema() # allows us to validate data for single customers when we send and receive
members_schema = MembersSchema(many = True)  # allow us to validate multiple rows or entries from our customer table at the same time

class WorkoutSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    duration = fields.DateTime()
    members_id = fields.Int()

class Meta:
        fields = ("id", "members_name", "email", "phone")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many = True)
#=====================================================

# CRUD Operations
# Create (POST)
# Retrieve (GET)
# Update (PUT)
# Delete (DELETE)

#======================================================
# DONE 
# Create a workout session with a POST request
@app.route("/workout_sessions", methods = ['POST'])
def create_workout_session():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            workout_data = workout_schema.load(request.json)
        except ValidationError as e:
            return jsonify(e.messages), 400
        try:
            cursor = conn.cursor()

            new_workout = (workout_data['duration'], workout_data['members_id'])

            query = "INSERT INTO workout_sessions (duration, members_id) VALUES (%s, %s);"

            cursor.execute(query, new_workout)
            conn.commit()

            return jsonify({'message': 'New session created successfully!'}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500

# DONE 
# route to Get all Workout Sessions
@app.route("/workout_sessions", methods = ['GET'])
def get_workout_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM workout_sessions"

            cursor.execute(query)

            workout_sessions = cursor.fetchall()

        except Error as e:
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workouts_schema.jsonify(workout_sessions)

# DONE
# route to Get a single Workout Session by ID
@app.route("/workout_sessions/<int:id>", methods = ['GET'])
def get_workout_session(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = "SELECT * FROM workout_sessions WHERE id = %s;"
            cursor.execute(query, (id,))
            workout = cursor.fetchone()
            if not workout:
                return jsonify({'error': 'Member not found.'}), 404

            workout_data = {
                'id': workout[0],
                'duration': workout[1],
                'member_id': workout[2],
            }

            return jsonify(workout_data), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500

# DONE
# route to update workout session using 'PUT' method
@app.route("/workout_sessions/<int:id>", methods=["PUT"])
def update_session(id):
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM workout_sessions WHERE id = %s;"
            cursor.execute(check_query, (id,))
            session = cursor.fetchone()
            if not session:
                return jsonify({'error': 'Workout session not found.'}), 404
            
            update_session = (workout_data['duration'], workout_data['members_id'], id)

            query = "UPDATE workout_sessions SET duration = %s, members_id = %s WHERE id = %s;"
            cursor.execute(query, update_session)
            conn.commit()

            return jsonify({'message': f'Workout session {id} updated successfully!'}), 200
        except Error as e:
            print("ERROR")
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500


# DONE
# Create a new member with a POST request
@app.route("/members", methods = ['POST'])
def add_member():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            member_data = member_schema.load(request.json)
        except ValidationError as e:
            return jsonify(e.messages), 400
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

# DONE
# route to GET all members
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

# DONE
# route to Get a single member by ID
@app.route("/members/<int:id>", methods = ['GET'])
def get_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({'error': 'Member not found.'}), 404

            member_data = {
                'id': member[0],
                'name': member[1],
                'email': member[2],
                'phone': member[3]
            }

            return jsonify(member_data), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed.'}), 500

# DONE
# route to POST changes based on different query parameters
@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
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

#  Done
# a routes to DELETE a customers
@app.route("/members/<int:id>", methods = ['DELETE'])
def delete_member(id):
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