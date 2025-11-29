# Coach Institute SaaS Platform

A comprehensive SaaS solution for coaching institutes to create their online presence, manage student registrations, and process payments.

## Features

### For Institute Owners (Admin Panel)
- **Fully Configurable Landing Page**
  - Institute name and branding
  - Promotional offers/exam announcements
  - Why choose us section with bullet points
  - PDF download section for question papers
  - Student testimonials with images
  
- **Payment Management**
  - UPI payment integration
  - Card payment support
  - Real-time payment tracking
  - Configurable UPI details without server restart
  
- **Student Management**
  - Registration tracking
  - Payment status monitoring
  - Email notifications
  - Export capabilities

### For Students (Public Interface)
- Clean, responsive landing page
- Easy registration form
- Secure payment processing
- Email confirmations
- PDF downloads

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Frontend**: Bootstrap 5, jQuery
- **Email**: SMTP integration
- **Payments**: Razorpay/UPI integration
- **Deployment**: Render (backend), GitHub Pages (frontend)

## Quick Start

### 1. Setup New Institute
```bash
python setup_new_institute.py
```

### 2. Install Dependencies
```bash
pip install -r requirements_saas.txt
```

### 3. Run Application
```bash
python coach_saas_app.py
```

### 4. Access Admin Panel
- Go to `http://localhost:5000/admin/register`
- Create your institute account
- Configure your settings

## Deployment

### Backend (Render)
1. Fork this repository
2. Create new web service on Render
3. Connect your GitHub repo
4. Set environment variables:
   ```
   SECRET_KEY=your-secret-key
   SENDER_EMAIL=your-gmail@gmail.com
   SENDER_PASSWORD=your-app-password
   RAZORPAY_KEY_ID=your-razorpay-key
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

### Frontend (GitHub Pages)
1. Enable GitHub Pages in repository settings
2. Use `gh-pages` branch for deployment
3. Custom domain configuration available

## Configuration

### Email Setup
1. Enable 2-factor authentication on Gmail
2. Generate app password
3. Set `SENDER_EMAIL` and `SENDER_PASSWORD` environment variables

### Payment Setup
1. Create Razorpay account
2. Get API keys from dashboard
3. Configure webhook URLs
4. Set environment variables

### UPI Configuration
- Institute owners can update UPI ID anytime from admin panel
- Changes reflect immediately without restart
- Supports all major UPI providers

## Security Features

- Password hashing with Werkzeug
- Session management
- CSRF protection
- Input validation
- SQL injection prevention
- Secure file uploads

## Scaling & Multi-tenancy

### New Institute Onboarding
```bash
# Automated setup
python setup_new_institute.py

# Manual setup
1. Create new database
2. Configure environment variables
3. Deploy to new subdomain
4. Configure payment gateway
```

### Database Scaling
- SQLite for development/small institutes
- PostgreSQL for production/large scale
- Easy migration scripts provided

## API Endpoints

### Public Endpoints
- `GET /` - Landing page
- `GET /institute/<username>` - Institute page
- `POST /register/<username>` - Student registration
- `GET /payment/<registration_id>` - Payment page
- `POST /payment/confirm` - Payment confirmation

### Admin Endpoints
- `GET /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard
- `POST /admin/update` - Update configuration
- `POST /admin/upload_pdf` - Upload PDF files

### Payment Service Endpoints
- `POST /payment/create_order` - Create payment order
- `POST /payment/verify` - Verify payment
- `GET /payment/status/<id>` - Payment status
- `POST /webhook/razorpay` - Payment webhooks

## File Structure

```
coach-institute-saas/
├── coach_saas_app.py          # Main Flask application
├── payment_service.py         # Separate payment service
├── setup_new_institute.py     # Quick setup script
├── requirements_saas.txt      # Python dependencies
├── render.yaml               # Render deployment config
├── templates/                # HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── institute.html
│   ├── payment.html
│   ├── admin_login.html
│   ├── admin_register.html
│   └── admin_dashboard.html
├── uploads/                  # PDF storage
└── README_SAAS.md           # This file
```

## Environment Variables

```bash
# Application
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# Payment Gateway
RAZORPAY_KEY_ID=rzp_live_key
RAZORPAY_KEY_SECRET=rzp_live_secret
PAYMENT_SECRET_KEY=payment-secret

# Database (optional)
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Customization

### Branding
- Logo upload in admin panel
- Color scheme customization
- Custom CSS support
- White-label options

### Features
- Custom form fields
- Additional payment methods
- SMS notifications
- Advanced analytics

## Support & Maintenance

### Monitoring
- Payment transaction logs
- Registration analytics
- Error tracking
- Performance monitoring

### Backup
- Automated database backups
- File storage backups
- Configuration exports

## License

MIT License - Free for commercial use

## Support

For technical support or custom development:
- Email: support@coachsaas.com
- Documentation: https://docs.coachsaas.com
- Community: https://community.coachsaas.com

## Roadmap

- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Video course integration
- [ ] Live class scheduling
- [ ] Student progress tracking
- [ ] Automated marketing tools
- [ ] WhatsApp integration