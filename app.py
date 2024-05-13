from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

MAIL_GW_BASE_URL = "https://api.mail.gw"  # Replace with actual mail.gw base URL

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the form submission for creating an account

        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            # Perform the account creation action here
            create_account_url = f"{MAIL_GW_BASE_URL}/accounts"
            return f"Creating account with email: {email}, password: {password}.<br>POST to: {create_account_url} {request.values}"
        else:
            return "Email and password are required for creating an account."

    # Display the forms for both actions
    get_info_form = """
    <h2>Get Information</h2>
    <form action="/" method="POST">
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="text" id="typ" name="typ" value="info" hidden>
        <input type="submit" value="Get Info">
    </form>
    """

    create_account_form = """
    <h2>Create Account</h2>
    <form action="/" method="POST">  <!-- Change action to POST to '/' -->
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="text" id="typ" name="typ" value="create" hidden>
        <input type="submit" value="Create Account">
    </form>
    """

    return f"{get_info_form}<br>{create_account_form}"



@app.route('/token', methods=['POST'])
def get_token():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    response = requests.post(f"{MAIL_GW_BASE_URL}/token", json=data)
    if response.status_code == 200:
        token = response.json().get('token')
        return jsonify({'Authorization': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401


@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    response = requests.post(f"{MAIL_GW_BASE_URL}/accounts", json=data)
    if response.status_code == 201:
        return jsonify({'message': 'Account created successfully.'}), 201
    elif response.status_code == 409:
        return jsonify({'error': 'Email already exists.'}), 409
    else:
        return jsonify({'error': 'Failed to create account.'}), 500


@app.route('/me', methods=['GET'])
def get_user_info():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing.'}), 400

    headers = {'Authorization': auth_header}
    response = requests.get(f"{MAIL_GW_BASE_URL}/me", headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return jsonify(user_info), 200
    elif response.status_code == 401:
        return jsonify({'error': 'Invalid token.'}), 401
    else:
        return jsonify({'error': 'Failed to get user info.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
