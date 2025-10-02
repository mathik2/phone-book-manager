from flask import Flask, render_template, request, redirect, url_for, jsonify
from processor import get_all_contacts, delete_contact, update_contact, search_contacts, add_contact
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'email' in request.form:
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        add_contact(name, phone, email)
        return redirect(url_for('home'))
    contacts = get_all_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    contacts = search_contacts(query)
    # Return as JSON
    return jsonify([
        {'name': c[0], 'phone': c[1], 'email': c[2]} for c in contacts
    ])

@app.route('/delete/<name>', methods=['POST'])
def delete(name):
    delete_contact(name)
    return redirect(url_for('home'))

@app.route('/update/<name>', methods=['POST'])
def update(name):
    phone = request.form.get('phone')
    email = request.form.get('email')
    update_contact(name, phone, email)
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)