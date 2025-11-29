# Coach Institute SaaS Platform

A comprehensive multi-tenant SaaS platform for coaching institutes to manage student registrations, payments, and content delivery.

## Features

### For Students
- Institute-specific landing pages
- Online registration with payment gateway
- PDF download with lead capture
- Email notifications

### For Institute Owners
- Admin dashboard for configuration
- Student registration management
- Payment tracking
- Content management (PDFs, testimonials)
- Customizable institute settings

### For IT Administrators
- Multi-institute management
- Create/edit/disable institutes
- Centralized monitoring
- Super admin controls

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**
   ```bash
   python coach_saas_app.py
   ```

3. **Access the Platform**
   - Main page: `http://localhost:5000`
   - IT Admin: `http://localhost:5000/it/login` (itadmin/itadmin123)

## Architecture

- **Backend**: Flask with SQLite database
- **Frontend**: Bootstrap 5 with responsive design
- **Multi-tenant**: Each institute gets unique URL `/institute/{username}`
- **Email System**: SMTP with console fallback
- **File Management**: Secure PDF uploads and serving

## Database Schema

- `institutes` - Institute details and credentials
- `configurations` - Institute-specific settings
- `registrations` - Student registrations and payments
- `pdf_downloads` - Download tracking
- `it_admins` - IT administrator accounts

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- Institute isolation
- Secure file uploads

## Demo Credentials

**IT Admin**: itadmin / itadmin123

## License

MIT License