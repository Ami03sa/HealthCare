from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your username
    'password': 'Amithesh21893',  # Replace with your password
    'database': 'healthcaremanagement'  # Ensure this matches your database name
}

# Database connection helper
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Index route
@app.route('/')
def index():
    return render_template('index.html')



# Route for displaying the appointments page and handling form submissions
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to the database", 500

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch all patients from the database
        cursor.execute("SELECT patient_id, patient_name FROM patients")
        patients = cursor.fetchall()

        if request.method == 'POST':
            # Retrieve form data
            patient_id = request.form.get('patient_id')  # Updated to use patient_id
            appointment_datetime = request.form.get('appointment_datetime')
            physician_id = request.form.get('physician_id')
            notes = request.form.get('notes')

            # Insert data into the database
            insert_query = """
                INSERT INTO appointments (patient_id, physician_id, appointment_datetime, notes)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_id, physician_id, appointment_datetime, notes))
            conn.commit()


            return render_template('appointments.html', patients=patients)
            
            

        # On GET request, render the appointments form with patients
        return render_template('appointments.html', patients=patients)

    except Error as e:
        return f"Error: {e}", 500
    finally:
        cursor.close()
        conn.close()


    # On GET request, render the HTML page
    return render_template('appointments.html')



# Patient profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to the database", 500

    try:
        cursor = conn.cursor()

        if request.method == 'POST':
            # Get form data
            patient_name = request.form.get('patientName')
            date_of_birth = request.form.get('patientDOB')
            contact_info = request.form.get('patientContact')
            address = request.form.get('patientAddress')

            # Insert patient data into the database
            insert_query = """
                INSERT INTO patients (patient_name, date_of_birth, contact_info, address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_name, date_of_birth, contact_info, address))
            conn.commit()

            # Redirect to the same page after successful submission
            return render_template('profile.html')

        # On GET request, render the profile form
        return render_template('profile.html')

    except Error as e:
        return f"Database error: {e}", 500

    finally:
        cursor.close()
        conn.close()

# SOAP records route
@app.route('/soap', methods=['GET', 'POST'])
def soap():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to the database", 500

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch all patients from the database
        cursor.execute("SELECT patient_id, patient_name FROM patients")
        patients = cursor.fetchall()

        # Fetch all physicians from the database
        cursor.execute("SELECT physician_id, physician_name FROM physicians")
        physicians = cursor.fetchall()

        if request.method == 'POST':
            # Retrieve form data
            patient_id = request.form.get('soapPatient')
            physician_id = request.form.get('soapPhysician')
            visit_datetime = request.form.get('visitDatetime')
            subjective_observations = request.form.get('soapSubjective')
            objective_data = request.form.get('soapObjective')
            diagnosis = request.form.get('soapDiagnosis')
            treatment_plan = request.form.get('soapTreatment')

            # Insert SOAP record into the database
            insert_query = """
                INSERT INTO soap_records (patient_id, physician_id, visit_datetime, subjective_observations, objective_data, diagnosis, treatment_plan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_id, physician_id, visit_datetime, subjective_observations, objective_data, diagnosis, treatment_plan))
            conn.commit()p

            return render_template('soap.html', patients=patients, physicians=physicians)

        # On GET request, render the SOAP form with patients and physicians
        return render_template('soap.html', patients=patients, physicians=physicians)

    except Error as e:
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        conn.close()


# Visit management route
@app.route('/visit_info', methods=['GET', 'POST'])
def visit_info():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to the database", 500

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch all patients from the database
        cursor.execute("SELECT patient_id, patient_name FROM patients")
        patients = cursor.fetchall()

        # Fetch all physicians from the database
        cursor.execute("SELECT physician_id, physician_name FROM physicians")
        physicians = cursor.fetchall()

        if request.method == 'POST':
            # Retrieve form data
            patient_id = request.form.get('visitPatient')
            physician_id = request.form.get('visitPhysician')
            visit_type = request.form.get('visitType')
            admission_date = request.form.get('admissionDate')
            discharge_date = request.form.get('dischargeDate')
            visit_notes = request.form.get('visitNotes')

            # Insert visit details into the database
            insert_query = """
                INSERT INTO visits (patient_id, physician_id, visit_type, admission_date, discharge_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_id, physician_id, visit_type, admission_date, discharge_date, visit_notes))
            conn.commit()

            return render_template('visit_info.html', patients=patients, physicians=physicians)

        # On GET request, render the visit form with patients and physicians
        return render_template('visit_info.html', patients=patients, physicians=physicians)

    except Error as e:
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        conn.close()

    # On GET request, fetch all patients to populate the dropdown and render the form
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get all patient details
        cursor.execute("SELECT patient_id, patient_name FROM patients")
        patients = cursor.fetchall()

    except Error as e:
        return f"Error retrieving patients: {e}", 500
    finally:
        cursor.close()
        conn.close()

    return render_template('visit_info.html', patients=patients)

# After visit summary route
@app.route('/visit_summary', methods=['GET', 'POST'])
def visit_summary():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to the database", 500

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch all visit IDs from the visits table
        cursor.execute("SELECT visit_id FROM visits")
        visits = cursor.fetchall()

        if request.method == 'POST':
            # Retrieve form data
            visit_id = request.form.get('summaryVisitID')
            notes_on_care = request.form.get('summaryNotes')
            patient_instructions = request.form.get('summaryInstructions')
            follow_up_details = request.form.get('summaryFollowUp')

            # Insert data into the after_visit_summary table
            insert_query = """
                INSERT INTO after_visit_summary (visit_id, notes_on_care, patient_instructions, follow_up_details)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (visit_id, notes_on_care, patient_instructions, follow_up_details))
            conn.commit()

            return render_template('visit_summary.html', visits=visits, message="After Visit Summary saved successfully.")

        # On GET request, render the visit summary form with available visits
        return render_template('visit_summary.html', visits=visits)

    except Error as e:
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

