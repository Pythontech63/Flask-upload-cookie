from flask import Flask, request, make_response, render_template, redirect, url_for, flash

app = Flask(__name__)

# Set the secret key for session management and flash messages
app.secret_key = 'your_secret_key'

# Home route
@app.route('/')
def index():
    # Check for username in cookies
    username = request.cookies.get('username')
    if username:
        return render_template('upload.html', username=username)  # Show upload form if username exists
    else:
        return redirect(url_for('set_username'))  # Redirect to set username if cookie is missing

# Route to set the username
@app.route('/set-username', methods=['GET', 'POST'])
def set_username():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            # Save username in cookies
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username, max_age=60 * 60 * 24)  # Valid for 1 day
            flash('Username saved in cookies!')
            return resp
        else:
            flash('Please enter a valid username!')
    return render_template('set_username.html')

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part!')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file!')
        return redirect(url_for('index'))
    if file:
        file.save(f'uploads/{file.filename}')  # Save the file in the uploads directory
        flash('File uploaded successfully!')
        return redirect(url_for('index'))

# Route to logout
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', max_age=0)  # Clear the cookie
    flash('You have been logged out!')
    return resp

if __name__ == '__main__':
    app.run(debug=True)