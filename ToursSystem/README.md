# 🌍 Wanderlust Journeys - Tourism Management System

A full-stack web application built with **Python Django**, **MySQL**, **Bootstrap 5**, **HTML5**, **CSS3**, and **JavaScript**.

---

## 🌟 Key Features

1. **User Authentication & Customer Portal**:
   - Secure registration, login, and profile management with user avatars.
   - **Customer Dashboard**: Real-time booking history, status badges, travel voucher generator, review submission, and booking cancellation.

2. **Destination Catalog & Tour Packages**:
   - High-impact visual destinations with climate, best season to visit, and local highlights.
   - Comprehensive Tour Packages with pricing, duration, day-by-day collapsible itineraries, inclusions, and exclusions.
   - Dynamic search bar and sidebar multi-filter (keyword, destination, category, duration, price range, and sorting).

3. **Booking & Payment Simulation**:
   - Multi-step booking checkout flow with traveler count, custom requests, and validation.
   - Dynamic JavaScript price calculator with live total and subtotal updates.
   - Simulated payment checkout (Credit Card, PayPal, Bank Transfer, Cash on Arrival).
   - Instant printable Travel Voucher and Invoice with reference number.

4. **Reviews & Inquiries**:
   - 5-star rating system with customer feedback.
   - Working contact inquiry form for custom trips.

5. **Custom Admin Management Portal**:
   - **Analytics Dashboard**: KPI statistics for Total Revenue, Total Bookings, Active Tours, Registered Customers.
   - **Chart.js Visualizations**: Revenue breakdown by tour category and Booking status distribution doughnut chart.
   - **Destination Management**: Full CRUD operations (Add, Edit, Delete, View).
   - **Tour Package Management**: Full CRUD operations with duration and discount configurations.
   - **Booking Management**: Status updater (Pending, Confirmed, Cancelled, Completed).
   - **Payments & Reports**: Financial logs and transaction summaries.
   - **Customer Directory**: Customer lifetime spend and booking history.
   - **Inquiries Manager**: Review contact messages with read/unread toggle.

---

## 🔑 Default Credentials

| Role | Username | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | `http://127.0.0.1:8000/admin-dashboard/` or `/admin/` |
| **Demo Customer** | `traveler` | `traveler123` | `http://127.0.0.1:8000/dashboard/` |

---

## 🚀 Quick Setup & Installation Guide (VS Code)

### 1. Open Project in VS Code
Open the project directory in VS Code:
```bash
code c:\Users\MSII\Desktop\ToursSystem
```

### 2. Install Required Python Packages
```bash
pip install -r requirements.txt
```
*(Dependencies: `Django`, `PyMySQL`, `Pillow`)*

### 3. Database Setup (PostgreSQL or SQLite Fallback)
The application includes automatic detection:
- **Using PostgreSQL**:
  1. Ensure your PostgreSQL service is running on `127.0.0.1:5432` (PostgreSQL 14+ / 18 supported).
  2. The application will **automatically create** `tourism_db` if it does not exist when using user `postgres` and password `123` (or your custom environment variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
  3. Apply migrations:
     ```bash
     python manage.py migrate
     ```
- **Zero-Config Fallback**:
  If PostgreSQL is stopped or unreachable, the application will automatically fall back to SQLite without crashing!

### 4. Populate Sample Tourism Data
Run the custom seeder command to load world-class destinations (Bali, Swiss Alps, Santorini, Kyoto, Serengeti, Amalfi Coast), packages, and demo accounts:
```bash
python manage.py seed_data
```

### 5. Run the Local Development Server
```bash
python manage.py runserver
```
Visit the application in your browser:
- Public Homepage: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Portal: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)
- Django Native Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Automated Tests
```bash
python manage.py test
```
All 7 unit and integration test suites will execute and verify public routes, booking calculations, payment states, and admin access control.
