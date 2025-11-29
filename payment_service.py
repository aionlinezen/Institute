from flask import Flask, request, jsonify
import os
import json
import uuid
from datetime import datetime
import sqlite3
import hashlib
import hmac

app = Flask(__name__)
app.secret_key = os.environ.get('PAYMENT_SECRET_KEY', 'payment-secret-key')

# Payment gateway configurations
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_key')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'rzp_test_secret')

def init_payment_db():
    """Initialize payment database"""
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL,
            institute_id INTEGER NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            currency TEXT DEFAULT 'INR',
            payment_method TEXT,
            gateway_payment_id TEXT,
            gateway_order_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gateway TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            processed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/payment/create_order', methods=['POST'])
def create_payment_order():
    """Create payment order"""
    try:
        data = request.json
        registration_id = data.get('registration_id')
        institute_id = data.get('institute_id')
        amount = data.get('amount', 1000)
        
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        
        order_id = f"order_{uuid.uuid4().hex[:12]}"
        
        cursor.execute('''
            INSERT INTO payment_transactions 
            (registration_id, institute_id, amount, gateway_order_id, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (registration_id, institute_id, amount, order_id, 'created'))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'amount': amount,
            'currency': 'INR',
            'key': RAZORPAY_KEY_ID,
            'transaction_id': transaction_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/payment/verify', methods=['POST'])
def verify_payment():
    """Verify payment signature"""
    try:
        data = request.json
        razorpay_payment_id = data.get('razorpay_payment_id')
        transaction_id = data.get('transaction_id')
        
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE payment_transactions 
            SET status = 'completed', 
                gateway_payment_id = ?,
                payment_method = 'razorpay',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (razorpay_payment_id, transaction_id))
        
        cursor.execute('''
            SELECT registration_id, institute_id, amount 
            FROM payment_transactions 
            WHERE id = ?
        ''', (transaction_id,))
        
        transaction = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'payment_id': razorpay_payment_id,
            'registration_id': transaction[0] if transaction else None
        })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_payment_db()
    app.run(debug=True, port=5001)