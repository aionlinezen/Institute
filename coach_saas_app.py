from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os
import uuid
from datetime import datetime
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Institutes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            institute_name TEXT NOT NULL,
            offer_text TEXT,
            upi_id TEXT,
            email TEXT,
            amount DECIMAL(10,2) DEFAULT 1000,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Institute configurations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institute_id INTEGER,
            why_choose_us TEXT,
            pdf_title TEXT,
            pdf_filename TEXT,
            testimonials TEXT,
            FOREIGN KEY (institute_id) REFERENCES institutes (id)
        )
    ''')
    
    # Aspirant registrations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institute_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            payment_status TEXT DEFAULT 'pending',
            payment_id TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (institute_id) REFERENCES institutes (id)
        )
    ''')
    
    # PDF downloads tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institute_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (institute_id) REFERENCES institutes (id)
        )
    ''')
    
    # IT admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS it_admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default IT admin if not exists
    cursor.execute('SELECT COUNT(*) FROM it_admins')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO it_admins (username, password_hash)
            VALUES (?, ?)
        ''', ('itadmin', generate_password_hash('itadmin123')))
    
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'institute_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to_email, subject, body, institute_email=None):
    """Send email notification"""
    try:
        # Check if email credentials are configured
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            # Fallback to console output for demo
            print(f"\n=== EMAIL NOTIFICATION ===")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            print(f"========================\n")
            return True
        
        # Real email sending (when credentials are configured)
        import smtplib
        from email.mime.text import MimeText
        from email.mime.multipart import MimeMultipart
        
        msg = MimeMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MimeText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"[EMAIL SENT] To: {to_email}, Subject: {subject}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        # Still print to console as fallback
        print(f"\n=== EMAIL FALLBACK ===")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"====================\n")
        return False

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/institute/<username>')
def institute_page(username):
    """Main institute landing page for aspirants"""
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT i.id, i.username, i.password_hash, i.institute_name, i.offer_text, i.upi_id, i.email, i.amount, i.is_active, i.created_at,
               c.why_choose_us, c.pdf_title, c.pdf_filename, c.testimonials
        FROM institutes i
        LEFT JOIN configurations c ON i.id = c.institute_id
        WHERE i.username = ? AND i.is_active = TRUE
    ''', (username,))
    
    institute_data = cursor.fetchone()
    conn.close()
    
    if not institute_data:
        return "Institute not found", 404
    
    # Safe JSON parsing for testimonials
    try:
        testimonials = json.loads(institute_data[13]) if institute_data[13] else []
    except (json.JSONDecodeError, TypeError):
        testimonials = []
    
    institute = {
        'id': institute_data[0],
        'username': institute_data[1],
        'institute_name': institute_data[3],
        'offer_text': institute_data[4],
        'amount': institute_data[7],
        'why_choose_us': institute_data[10] or "Quality education, Expert faculty, Proven results",
        'pdf_title': institute_data[11] or "Download Sample Papers",
        'pdf_filename': institute_data[12],
        'testimonials': testimonials
    }
    
    return render_template('institute.html', institute=institute)

@app.route('/register/<username>', methods=['POST'])
def register_aspirant(username):
    """Handle aspirant registration"""
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Get institute details
    cursor.execute('SELECT id, institute_name, email FROM institutes WHERE username = ?', (username,))
    institute = cursor.fetchone()
    
    if not institute:
        return jsonify({'error': 'Institute not found'}), 404
    
    # Save registration
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    
    cursor.execute('''
        INSERT INTO registrations (institute_id, name, email, phone)
        VALUES (?, ?, ?, ?)
    ''', (institute[0], name, email, phone))
    
    registration_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Send notification emails
    aspirant_subject = f"Registration Confirmation - {institute[1]}"
    aspirant_body = f"""
    <h2>Thank you for registering with {institute[1]}!</h2>
    <p>Dear {name},</p>
    <p>Your registration has been received. Please complete your payment to confirm your enrollment.</p>
    <p>Registration ID: {registration_id}</p>
    """
    
    owner_subject = f"New Registration - {name}"
    owner_body = f"""
    <h2>New Student Registration</h2>
    <p>Name: {name}</p>
    <p>Email: {email}</p>
    <p>Phone: {phone}</p>
    <p>Registration ID: {registration_id}</p>
    <p>Payment Status: Pending</p>
    """
    
    # Send emails immediately
    send_email(email, aspirant_subject, aspirant_body)
    if institute[2]:
        send_email(institute[2], owner_subject, owner_body)
    
    print(f"[EMAIL] Registration emails sent for {name}")
    
    return jsonify({
        'success': True,
        'registration_id': registration_id,
        'payment_url': f'/payment/{registration_id}',
        'redirect': True
    })

@app.route('/payment/<int:registration_id>')
def payment_page(registration_id):
    """Payment page for aspirants"""
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, i.institute_name, i.upi_id, i.amount
        FROM registrations r
        JOIN institutes i ON r.institute_id = i.id
        WHERE r.id = ?
    ''', (registration_id,))
    
    registration = cursor.fetchone()
    conn.close()
    
    if not registration:
        return "Registration not found", 404
    
    payment_data = {
        'registration_id': registration_id,
        'name': registration[2],
        'email': registration[3],
        'institute_name': registration[7],
        'upi_id': registration[8] or 'payment@institute.com',
        'amount': registration[9] or 1000
    }
    
    return render_template('payment.html', payment=payment_data)

@app.route('/payment/confirm', methods=['POST'])
def confirm_payment():
    """Handle payment confirmation"""
    registration_id = request.form['registration_id']
    payment_id = request.form.get('payment_id', str(uuid.uuid4()))
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Update payment status
    cursor.execute('''
        UPDATE registrations 
        SET payment_status = 'completed', payment_id = ?
        WHERE id = ?
    ''', (payment_id, registration_id))
    
    # Get registration and institute details
    cursor.execute('''
        SELECT r.*, i.institute_name, i.email
        FROM registrations r
        JOIN institutes i ON r.institute_id = i.id
        WHERE r.id = ?
    ''', (registration_id,))
    
    registration = cursor.fetchone()
    conn.commit()
    conn.close()
    
    if registration:
        # Send congratulations emails
        aspirant_subject = f"Payment Confirmed - Welcome to {registration[8]}!"
        aspirant_body = f"""
        <h2>Congratulations {registration[2]}!</h2>
        <p>Your payment has been confirmed and you are now enrolled with {registration[8]}.</p>
        <p>Payment ID: {payment_id}</p>
        <p>We will contact you soon with further details.</p>
        """
        
        owner_subject = f"Payment Received - {registration[2]}"
        owner_body = f"""
        <h2>Payment Confirmation</h2>
        <p>Student: {registration[2]}</p>
        <p>Email: {registration[3]}</p>
        <p>Phone: {registration[4]}</p>
        <p>Payment ID: {payment_id}</p>
        <p>Status: Completed</p>
        """
        
        send_email(registration[3], aspirant_subject, aspirant_body)
        if registration[9]:
            send_email(registration[9], owner_subject, owner_body)
    
    return render_template('payment_success.html', payment_id=payment_id)

@app.route('/download/<username>/<filename>', methods=['GET', 'POST'])
def download_file(username, filename):
    """Download PDF files with user details collection"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        # Get institute ID
        conn = sqlite3.connect('coach_saas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, institute_name, email FROM institutes WHERE username = ?', (username,))
        institute = cursor.fetchone()
        
        if institute:
            # Save download record
            cursor.execute('''
                INSERT INTO pdf_downloads (institute_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            ''', (institute[0], name, email, phone))
            conn.commit()
            
            # Send notification to admin
            admin_subject = f"PDF Download - {name}"
            admin_body = f"""
            <h2>New PDF Download</h2>
            <p>Name: {name}</p>
            <p>Email: {email}</p>
            <p>Phone: {phone}</p>
            <p>Institute: {institute[1]}</p>
            <p>File: {filename}</p>
            """
            if institute[2]:
                send_email(institute[2], admin_subject, admin_body)
        
        conn.close()
        
        # Serve the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return "File not found", 404
    
    # Show form for user details
    return render_template('download_form.html', username=username, filename=filename)

# Admin Routes
@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/authenticate', methods=['POST'])
def admin_authenticate():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash, is_active FROM institutes WHERE username = ?', (username,))
    institute = cursor.fetchone()
    conn.close()
    
    if institute and check_password_hash(institute[1], password):
        if not institute[2]:  # Check if institute is disabled
            flash('Institute account is disabled. Contact IT admin.')
            return redirect(url_for('admin_login'))
        session['institute_id'] = institute[0]
        session['username'] = username
        return redirect(url_for('admin_dashboard'))
    
    flash('Invalid credentials')
    return redirect(url_for('admin_login'))

@app.route('/it/create_institute', methods=['POST'])
def it_create_institute():
    if 'it_admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    username = request.form['username']
    password = request.form['password']
    institute_name = request.form['institute_name']
    email = request.form['email']
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO institutes (username, password_hash, institute_name, email)
            VALUES (?, ?, ?, ?)
        ''', (username, generate_password_hash(password), institute_name, email))
        
        institute_id = cursor.lastrowid
        
        # Create default configuration
        cursor.execute('''
            INSERT INTO configurations (institute_id, why_choose_us, pdf_title, testimonials)
            VALUES (?, ?, ?, ?)
        ''', (institute_id, "Quality education\nExpert faculty\nProven results", "Download Sample Papers", "[]"))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'Institute created successfully!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Username already exists'})
    finally:
        conn.close()

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Get institute data
    cursor.execute('''
        SELECT i.id, i.username, i.password_hash, i.institute_name, i.offer_text, i.upi_id, i.email, i.amount, i.is_active, i.created_at,
               c.why_choose_us, c.pdf_title, c.pdf_filename, c.testimonials
        FROM institutes i
        LEFT JOIN configurations c ON i.id = c.institute_id
        WHERE i.id = ?
    ''', (session['institute_id'],))
    
    institute_data = cursor.fetchone()
    
    # Get registrations
    cursor.execute('''
        SELECT * FROM registrations 
        WHERE institute_id = ? 
        ORDER BY registered_at DESC
    ''', (session['institute_id'],))
    
    registrations = cursor.fetchall()
    conn.close()
    
    # Safe JSON parsing for testimonials
    try:
        testimonials = json.loads(institute_data[13]) if institute_data[13] else []
    except (json.JSONDecodeError, TypeError):
        testimonials = []
    
    institute = {
        'institute_name': institute_data[3],
        'offer_text': institute_data[4] or '',
        'upi_id': institute_data[5] or '',
        'email': institute_data[6] or '',
        'amount': institute_data[7] or 1000,
        'why_choose_us': institute_data[10] or '',
        'pdf_title': institute_data[11] or '',
        'pdf_filename': institute_data[12] or '',
        'testimonials': testimonials
    }
    
    return render_template('admin_dashboard.html', institute=institute, registrations=registrations)

@app.route('/admin/update', methods=['POST'])
@login_required
def admin_update():
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Update institute details
    cursor.execute('''
        UPDATE institutes 
        SET institute_name = ?, offer_text = ?, upi_id = ?, email = ?, amount = ?
        WHERE id = ?
    ''', (
        request.form['institute_name'],
        request.form['offer_text'],
        request.form['upi_id'],
        request.form['email'],
        float(request.form['amount']),
        session['institute_id']
    ))
    
    # Update configurations
    cursor.execute('''
        UPDATE configurations 
        SET why_choose_us = ?, pdf_title = ?
        WHERE institute_id = ?
    ''', (
        request.form['why_choose_us'],
        request.form['pdf_title'],
        session['institute_id']
    ))
    
    conn.commit()
    conn.close()
    
    flash('Settings updated successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload_pdf', methods=['POST'])
@login_required
def upload_pdf():
    if 'pdf_file' not in request.files:
        flash('No file selected')
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['pdf_file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('admin_dashboard'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{session['username']}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Update database
        conn = sqlite3.connect('coach_saas.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE configurations 
            SET pdf_filename = ?
            WHERE institute_id = ?
        ''', (filename, session['institute_id']))
        conn.commit()
        conn.close()
        
        flash('PDF uploaded successfully!')
    else:
        flash('Invalid file type')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file selected'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        filename = secure_filename(f"{session['username']}_testimonial_{uuid.uuid4().hex[:8]}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Return the file URL
        image_url = f"/uploads/{filename}"
        return jsonify({'success': True, 'image_url': image_url})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/admin/update_testimonials', methods=['POST'])
@login_required
def update_testimonials():
    try:
        testimonials = request.json.get('testimonials', []) if request.json else []
        
        conn = sqlite3.connect('coach_saas.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE configurations 
            SET testimonials = ?
            WHERE institute_id = ?
        ''', (json.dumps(testimonials), session['institute_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# IT Admin Routes
@app.route('/it/login')
def it_login():
    return render_template('it_login.html')

@app.route('/it/authenticate', methods=['POST'])
def it_authenticate():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM it_admins WHERE username = ?', (username,))
    admin = cursor.fetchone()
    conn.close()
    
    if admin and check_password_hash(admin[1], password):
        session['it_admin_id'] = admin[0]
        session['it_username'] = username
        return redirect(url_for('it_dashboard'))
    
    flash('Invalid credentials')
    return redirect(url_for('it_login'))

@app.route('/it/dashboard')
def it_dashboard():
    if 'it_admin_id' not in session:
        return redirect(url_for('it_login'))
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Get all institutes
    cursor.execute('SELECT * FROM institutes ORDER BY created_at DESC')
    institutes = cursor.fetchall()
    
    conn.close()
    return render_template('it_dashboard.html', institutes=institutes)

@app.route('/it/toggle_institute/<int:institute_id>', methods=['POST'])
def toggle_institute(institute_id):
    if 'it_admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Toggle active status
    cursor.execute('UPDATE institutes SET is_active = NOT is_active WHERE id = ?', (institute_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/it/edit_institute/<int:institute_id>', methods=['POST'])
def edit_institute(institute_id):
    if 'it_admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        institute_name = request.form.get('institute_name', '').strip()
        email = request.form.get('email', '').strip()
        upi_id = request.form.get('upi_id', '').strip()
        amount = request.form.get('amount', '1000')
        
        if not institute_name:
            return jsonify({'error': 'Institute name is required'}), 400
        
        try:
            amount = float(amount)
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400
        
        conn = sqlite3.connect('coach_saas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE institutes 
            SET institute_name = ?, email = ?, upi_id = ?, amount = ?
            WHERE id = ?
        ''', (institute_name, email, upi_id, amount, institute_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Institute not found'}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Institute updated successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/it/edit/<int:institute_id>')
def it_edit_institute(institute_id):
    if 'it_admin_id' not in session:
        return redirect(url_for('it_login'))
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM institutes WHERE id = ?', (institute_id,))
    institute = cursor.fetchone()
    conn.close()
    
    if not institute:
        flash('Institute not found')
        return redirect(url_for('it_dashboard'))
    
    return render_template('it_edit_institute.html', institute=institute)

@app.route('/it/update/<int:institute_id>', methods=['POST'])
def it_update_institute(institute_id):
    if 'it_admin_id' not in session:
        return redirect(url_for('it_login'))
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE institutes 
        SET institute_name = ?, email = ?, upi_id = ?, amount = ?
        WHERE id = ?
    ''', (
        request.form['institute_name'],
        request.form['email'],
        request.form['upi_id'],
        float(request.form['amount']),
        institute_id
    ))
    
    conn.commit()
    conn.close()
    
    flash('Institute updated successfully!')
    return redirect(url_for('it_dashboard'))

@app.route('/it/logout')
def it_logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)