from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd


app = Flask(__name__)
# Required for flashing messages
app.secret_key = 'supersecretkey'

# Hardcoded login credentials
USERNAME = 'admin'
PASSWORD = 'password'

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Capture form data
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication check
        if username == USERNAME and password == PASSWORD:
            # Redirect to the dashboard after successful login
            return redirect(url_for('dashboard'))
        else:
            # Flash an error message if login is invalid
            flash('Invalid login. Please try again.')
            return redirect(url_for('login'))
    
    # Render the login page if GET method
    return render_template('login.html')

# Route for logout, redirects to login page
@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))

# Route for the dashboard page
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/monitoring', methods=['GET'])
def monitoring():
    return render_template('monitoring.html')

# Route for the users page
@app.route('/users', methods=['GET'])
def users():
    return render_template('users.html')

# New route for the new page
@app.route('/new_page', methods=['GET'])
def new_page():
    return render_template('new_page.html')

# Route to handle form submission and save to Excel
@app.route('/register', methods=['POST'])
def register():
    # Capture form data
    phone = request.form['phone']
    email = request.form['email']
    login = request.form['login']
    password = request.form['password']
    family_name = request.form['family_name']
    first_name = request.form['first_name']
    surname = request.form['surname']

    # Create a DataFrame to hold the data
    data = {
        'Phone': [phone],
        'Email': [email],
        'Login': [login],
        'Password': [password],
        'Family Name': [family_name],
        'First Name': [first_name],
        'Surname': [surname]
    }
    df = pd.DataFrame(data)

    # Save data to an Excel file (append if file exists)
    try:
        # Try to append if the file exists
        existing_df = pd.read_excel('registered_users.xlsx')
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, it will be created
        pass

    # Save the updated data to Excel
    df.to_excel('registered_users.xlsx', index=False)

    # Redirect to a success page or the same form
    return redirect(url_for('new_page'))


if __name__ == '__main__':
    app.run(debug=True)