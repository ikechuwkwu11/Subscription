# 📦 Flask Subscription Management API
This is a simple Flask-based REST API for managing user accounts, subscription plans, and subscriptions. The application uses Flask-Login for authentication and SQLite with SQLAlchemy for data storage.

## 🚀 Features
🔐 User registration and login (session-based auth with Flask-Login)
📃 Create, view, and delete plans
🧾 Subscribe to a plan
🔍 View all or single subscriptions
❌ Delete a subscription
🔐 Protected routes (requires login)

## 🛠 Tech Stack
- Python 3
- Flask
- Flask-Login
- SQLAlchemy (ORM)
- SQLite (development DB)
- Postman for testing

## 🔐 Authentication
- Login is required to access most routes.
- Session-based authentication is handled using Flask-Login.

## 📮 API Endpoints
🔑 Auth  
| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| POST   | `/register` | Register a new user |
| POST   | `/login`    | Login user          |
| GET    | `/logout`   | Logout user         |

📦 Plans
| Method | Endpoint            | Description            |
| ------ | ------------------- | ---------------------- |
| POST   | `/plan`             | Create a new plan      |
| GET    | `/get_plan`         | Get all plans          |
| GET    | `/single_plan/<id>` | Get single plan        |
| DELETE | `/delete_plan/<id>` | Delete plan            |
| POST   | `/buy_plan/<id>`    | Simulated plan booking |

🧾 Subscriptions
| Method | Endpoint                    | Description                |
| ------ | --------------------------- | -------------------------- |
| POST   | `/subscription`             | Create a new subscription  |
| GET    | `/get_subscription`         | View all subscriptions     |
| GET    | `/single_subscription/<id>` | View a single subscription |
| DELETE | `/delete_subscription/<id>` | Delete a subscription      |

## 📬 Example Postman Body
✅ Register
{
  "email": "test@example.com",
  "password": "mypassword"
}

✅ Login
{
  "email": "test@example.com",
  "password": "mypassword"
}

✅ Create Plan
{
  "name": "Pro Plan",
  "price": 49.99,
  "billing_cycle": "monthly",
  "api_call_limit": 10000,
  "storage_limit_mb": 500
}

✅ Create Subscription
{
  "user_id": 1,
  "plan_id": 1,
  "start_date": "2025-07-01T12:00:00",
  "end_date": "2025-08-01T12:00:00",
  "is_active": true
}

