# Coach Institute SaaS - Simple Setup

## ✅ What's Ready

A complete SaaS platform for coaching institutes with:
- **Admin Dashboard** - Manage institute settings, payments, registrations
- **Student Landing Pages** - Configurable institute pages with registration
- **Payment Processing** - UPI/Card payments with tracking
- **Email Notifications** - Automated emails for registrations/payments
- **Multi-tenant** - Easy setup for multiple institutes

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install flask werkzeug
```

### Step 2: Create Demo Institute
```bash
python demo_setup.py
```

### Step 3: Start Application
```bash
python start_app.py
```

## 🎯 Access Your Platform

**Demo Institute Page:**
- URL: http://localhost:5000/institute/demo
- Test student registration and payment flow

**Admin Panel:**
- URL: http://localhost:5000/admin/login  
- Username: `demo`
- Password: `demo123`

**Main Landing:**
- URL: http://localhost:5000
- Create new institutes or login to existing ones

## 📋 Admin Features

Once logged in as admin, you can:
- ✏️ Edit institute name and offer text
- 📄 Upload PDF study materials
- 💬 Manage student testimonials
- 💳 Configure UPI payment details
- 📊 View registration and payment tracking
- 📧 Monitor email notifications (printed to console)

## 👥 Student Flow

Students can:
1. Visit institute page (`/institute/demo`)
2. View institute information and testimonials
3. Download study materials (PDFs)
4. Register with name, email, phone
5. Complete payment (demo mode)
6. Receive confirmation emails

## 🏢 Create New Institute

### Option 1: Use Setup Script
```bash
python setup_new_institute.py
```

### Option 2: Manual Registration
1. Go to http://localhost:5000/admin/register
2. Fill institute details
3. Login and configure settings

## 📁 Key Files

- `coach_saas_app.py` - Main Flask application
- `payment_service.py` - Payment backend (run separately on port 5001)
- `start_app.py` - Easy startup script
- `demo_setup.py` - Creates demo institute
- `templates/` - All HTML templates
- `coach_saas.db` - SQLite database (auto-created)

## 🚀 Production Deployment

### Backend (Render/Heroku)
1. Push code to GitHub
2. Connect to hosting platform
3. Set environment variables:
   - `SECRET_KEY` - Random secret key
   - `SENDER_EMAIL` - Gmail for notifications  
   - `SENDER_PASSWORD` - Gmail app password

### Frontend (GitHub Pages)
- Static files ready for deployment
- Custom domain support available

## 💰 Business Ready

The platform is designed for SaaS business:
- **Subscription Model** - Monthly fees per institute
- **Transaction Fees** - Percentage on payments
- **Setup Charges** - One-time onboarding
- **Custom Features** - Additional development

## 🔧 Customization

Each institute can configure:
- Institute name and branding
- Promotional offers/announcements  
- "Why choose us" bullet points
- PDF downloads (question papers)
- Student testimonials with images
- UPI payment details
- Contact information

## 📞 Support

For issues:
1. Check console output for errors
2. Verify Flask is installed
3. Ensure port 5000 is available
4. Check database file permissions

## 🎯 Next Steps

1. **Test locally** - Use demo institute to test all features
2. **Create real institute** - Use setup script for actual institute
3. **Deploy to production** - Follow deployment guide
4. **Start marketing** - Begin customer acquisition

---

**Ready to launch your coaching institute SaaS business!** 🚀