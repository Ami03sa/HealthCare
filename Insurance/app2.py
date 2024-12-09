from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your username
    'password': 'Amithesh21893',  # Replace with your password
    'database': 'Insurance'  # Ensure this matches your database name
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

# Route for displaying the Insurance page and handling form submissions
@app.route('/insurance', methods=['GET', 'POST'])
def insurance():
    conn = get_db_connection()

    if not conn:
        return render_template('Information.html', error_message="Error connecting to the database"), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the list of patients to display in the dropdown
        cursor.execute("SELECT PatientID, CONCAT(FirstName, ' ', LastName) AS FullName FROM Patients")
        patients = cursor.fetchall()

        # Fetch the insurance data for displaying in the table
        cursor.execute("SELECT * FROM InsuranceInformation")
        insurance_data = cursor.fetchall()

        # Handle POST request (form submission)
        if request.method == 'POST':
            # Get data from the form
            patient_id = request.form.get('patient_id')
            insurance_provider = request.form.get('insurance_provider')
            policy_number = request.form.get('policy_number')
            copay = request.form.get('copay')
            deductible = request.form.get('deductible')
            covered_services = request.form.get('covered_services')

            # Validate patient_id
            cursor.execute("SELECT PatientID FROM Patients WHERE PatientID = %s", (patient_id,))
            patient_exists = cursor.fetchone()
            if not patient_exists:
                return render_template('Information.html', error_message="Patient ID not found in the database.")

            # Insert query to save data into the InsuranceInformation table
            insert_query = """
                INSERT INTO InsuranceInformation (PatientID, InsuranceProvider, PolicyNumber, Copay, Deductible, CoveredServices)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_id, insurance_provider, policy_number, copay, deductible, covered_services))
            conn.commit()

            # Return a success message after inserting the data
            return render_template('Information.html', insurance_data=insurance_data, message="Insurance information saved successfully.", patients=patients)

        return render_template('Information.html', insurance_data=insurance_data, patients=patients)

    except Error as e:
        return render_template('Information.html', error_message=f"Database error: {e}"), 500

    finally:
        cursor.close()
        conn.close()
        
# Route for Copay/Deductible Management page
@app.route('/copay', methods=['GET', 'POST'])
def copay():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Handle POST request to insert/update copay/deductible information
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        copay_amount = request.form['copay_amount']
        deductible_amount = request.form['deductible_amount']
        remaining_deductible = request.form['remaining_deductible']
        insurance_id = request.form['insurance_id']

        cursor.execute('''
            INSERT INTO CopayDeductible (InsuranceID, PatientID, CopayAmount, DeductibleAmount, RemainingDeductible)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            CopayAmount = %s, DeductibleAmount = %s, RemainingDeductible = %s
        ''', (insurance_id, patient_id, copay_amount, deductible_amount, remaining_deductible, copay_amount, deductible_amount, remaining_deductible))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return render_template('copay.html')  # Refresh the page after form submission
    
    # GET request to display existing copay/deductible data
    cursor.execute('''
        SELECT Patients.FirstName, Patients.LastName, InsuranceInformation.InsuranceProvider, 
               CopayDeductible.CopayAmount, CopayDeductible.DeductibleAmount, CopayDeductible.RemainingDeductible
        FROM CopayDeductible
        JOIN InsuranceInformation ON CopayDeductible.InsuranceID = InsuranceInformation.InsuranceID
        JOIN Patients ON CopayDeductible.PatientID = Patients.PatientID
    ''')
    copay_data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM Patients')  # For dropdown of patients
    patients = cursor.fetchall()
    
    cursor.execute('SELECT * FROM InsuranceInformation')  # For dropdown of insurance information
    insurance_info = cursor.fetchall()

    connection.close()
    return render_template('copay.html', copay_data=copay_data, patients=patients, insurance_info=insurance_info)

# Route for Bill Remaining page
@app.route('/bill_remaining', methods=['GET'])
def bill_remaining():
    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch all patients for the dropdown
    cursor.execute('''SELECT PatientID, CONCAT(FirstName, ' ', LastName) AS FullName FROM Patients''')
    patients = cursor.fetchall()

    # Fetch specific patient and their bill info if patient_id is passed
    patient_id = request.args.get('patient_id')
    if patient_id:
        # Fetch bills for the selected patient
        cursor.execute('''SELECT BillID, TotalAmount, InsurancePaid, AmountOwed, BillDate, BillStatus 
                          FROM Bills WHERE PatientID = %s''', (patient_id,))
        bill_data = cursor.fetchall()
    else:
        bill_data = []

    cursor.close()
    connection.close()

    return render_template('bill_remaining.html', 
                           patients=patients, 
                           bill_data=bill_data, 
                           selected_patient_id=patient_id)



# Route for payment process page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        # Fetch all patients
        cursor.execute('''SELECT PatientID, CONCAT(FirstName, ' ', LastName) AS FullName FROM Patients''')
        patients = cursor.fetchall()

        # Fetch payments for the selected patient
        patient_id = request.args.get('patient_id')  # Retrieve patient_id from query parameters
        payments = []
        if patient_id:
            cursor.execute('''SELECT PaymentID, PatientID, BillID, PaymentAmount, PaymentMethod, 
                              PaymentDate, PaymentStatus 
                              FROM Payments WHERE PatientID = %s''', (patient_id,))
            payments = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('payment.html', 
                               patients=patients, 
                               payments=payments, 
                               selected_patient_id=patient_id)

    elif request.method == 'POST':
        # Process new payment
        patient_id = request.form['patientId']
        bill_id = request.form['billId']
        payment_amount = float(request.form['paymentAmount'])
        payment_method = request.form['paymentMethod']
        payment_date = request.form['paymentDate']

        # Insert the new payment into Payments table
        cursor.execute('''INSERT INTO Payments (PatientID, BillID, PaymentAmount, PaymentMethod, PaymentDate, PaymentStatus)
                          VALUES (%s, %s, %s, %s, %s, 'Completed')''', 
                       (patient_id, bill_id, payment_amount, payment_method, payment_date))

        connection.commit()
        cursor.close()
        connection.close()

        # Redirect to payment page with selected patient
        return render_template('payment.html', selected_patient_id=patient_id)

if __name__ == '__main__':
    app.run(debug=True)
