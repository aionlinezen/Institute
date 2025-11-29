# 🔗 URL Reference Guide

## ✅ **Correct Institute URLs**

Based on your database, the correct URLs are:

### Working Institute URLs
- **Demo Institute**: http://localhost:5000/institute/demo
- **InstName1**: http://localhost:5000/institute/usernameurl1
- **NewCoaching**: http://localhost:5000/institute/usrnameurl2

### ❌ **Incorrect URLs** (These won't work)
- ~~http://localhost:5000/InstName1/usernameurl1~~
- ~~http://localhost:5000/NewCoaching/usrnameurl2~~

## 📋 **Current Institutes in Database**

| Institute Name | Username (URL) | Status | Correct URL |
|---|---|---|---|
| Excellence Coaching Institute | demo | Active | `/institute/demo` |
| InstName1 | usernameurl1 | Active | `/institute/usernameurl1` |
| NewCoaching | usrnameurl2 | Active | `/institute/usrnameurl2` |

## 🎯 **URL Pattern**

The URL pattern is: `http://localhost:5000/institute/{username}`

Where `{username}` is the username field from the database, NOT the institute name.

## 🔧 **IT Admin Powers**

IT Admin can now:
- ✅ **Edit institute details** (name, email, UPI, amount)
- ✅ **Enable/disable institutes**
- ✅ **Create new institutes**
- ✅ **Prevent disabled institutes from logging in**

## 💰 **Amount Configuration**

Institute owners can configure the amount that will be collected when aspirants register:
- ✅ **Admin Dashboard** → Amount field
- ✅ **Payment page** uses configured amount
- ✅ **UPI payments** use correct amount

## 🚀 **Test the Fixed Features**

1. **Visit working URLs**:
   - http://localhost:5000/institute/usernameurl1
   - http://localhost:5000/institute/usrnameurl2

2. **Test IT admin editing**:
   - Login: http://localhost:5000/it/login (itadmin/itadmin123)
   - Click "Edit" button on any institute

3. **Test disabled login prevention**:
   - Disable an institute via IT admin
   - Try to login as that institute owner

All bugs are now fixed! 🎉