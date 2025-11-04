<h1 align="center" style="color:#002E47; font-size:2.5rem;">Yusr</h1>

<p align="center" style="color:#2A4628; font-weight:500; font-size:1.2rem;">
An AI-powered digital assistant that unifies government and financial services into one seamless platform.
</p>

---

## Project Overview

Yusr simplifies the user's experience with public services by centralizing multiple government agencies, payment systems, and appointment scheduling into one connected platform.  
Users can securely access services, request documents, pay fines, and manage accounts—all through one modern interface.

---

## Core Functionality

| Feature | Description |
|----------|--------------|
| **Government Agencies** | View all available government entities and their provided services. |
| **Services Management** | Browse, request, and view services offered by each agency. |
| **Service Requests** | Track status of submitted requests (Pending, Processing, Approved, Rejected). |
| **Appointments** | Schedule, view, and manage upcoming appointments. |
| **Bank Accounts** | View, add, update, or delete your bank account. Infinite balance mode for testing. |
| **Traffic Fines** | View and pay all pending fines directly through the platform. |
| **Credit Card Payments** | Securely store, use, and remove credit cards for service payments. |
| **User Authentication** | Secure signup, login, and password management via JWT. |

---

## User Stories

| As a User | I Want To | So That I Can |
|------------|------------|----------------|
| **Sign up and log in securely** | Create an account or log in using my credentials | Access personalized services safely |
| **View government agencies** | See all available agencies and their services | Choose which service I need |
| **Submit a service request** | Fill out forms and submit service requests | Complete applications easily |
| **Track my service request status** | View if it’s pending, approved, or rejected | Stay updated on my request progress |
| **Book an appointment** | Choose a date and time for services that require attendance | Manage my visits efficiently |
| **View and manage my bank account** | See my IBAN, update the display name, or delete it | Control my financial data |
| **Pay traffic fines** | View pending fines and pay directly | Resolve violations easily |
| **Add or delete credit cards** | Manage payment options | Pay for services faster |
| **Change my password** | Update credentials securely | Protect my account access |
| **See all my previous requests** | Access service history | Review or repeat previous actions |

---

## Technologies Used

| Category | Technologies |
|-----------|--------------|
| **Backend Framework** | Django, Django REST Framework |
| **Database** | PostgreSQL |
| **Authentication** | JWT (SimpleJWT) |
| **Frontend** | React (Vite) |
| **Styling** | Custom CSS with royal blue & green palette |
| **Environment** | Pipenv, Docker, dotenv |

---

## ERD Diagram

<div align="center" style="background: linear-gradient(135deg, #002E47, #2A4628); padding: 30px; border-radius: 16px;">

<img src="erd-diagram.png" alt="Yusr ERD Diagram" width="800" style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"/>

</div>

<p align="center" style="color:#002E47; font-weight:600; margin-top:10px;">
The ERD shows the relationships between all models in the backend:
Users, Agencies, Services, Service Requests, Appointments, Bank Accounts, and Traffic Fines.
</p>

---

## API Routes Table

| Endpoint | Method | Description | Auth Required |
|-----------|---------|--------------|----------------|
| `/agencies/` | GET | List all government agencies | ✅ |
| `/services/` | GET | List all available services | ✅ |
| `/services/<id>/` | GET | View details of a specific service | ✅ |
| `/service-requests/` | GET, POST | List or create service requests | ✅ |
| `/service-requests/<id>/` | GET, PUT, DELETE | Retrieve, update, or delete a request | ✅ |
| `/service-requests/<id>/pay/` | POST | Pay for a specific service request | ✅ |
| `/users/signup/` | POST | Register new user | ❌ |
| `/users/login/` | POST | User login | ❌ |
| `/users/token/refresh/` | GET | Refresh user token | ✅ |
| `/users/change-password/` | POST | Change password | ✅ |
| `/credit-card/` | GET, POST, DELETE | Manage credit card | ✅ |
| `/my-fines/` | GET | View unpaid traffic fines | ✅ |
| `/pay-fines/` | POST | Pay all or selected fines | ✅ |
| `/bank-account/` | GET, POST, PUT, DELETE | Manage bank account | ✅ |

---

## Icebox Features

| Planned Feature | Description |
|------------------|-------------|
| **AI Chatbot Integration** | Full conversational flow for requesting services using natural language. |
| **Notifications System** | Email and SMS alerts for service updates and fines. |
| **Multi-language Support** | Arabic/English interface. |
| **Payment History Dashboard** | Visual summary of transactions and payments. |
| **Document Upload** | Support for uploading and verifying identity documents. |

---

## Challenges & Key Takeaways

| Challenge | Takeaway |
|------------|-----------|
| **Complex model relationships** | Gained strong understanding of one-to-many and one-to-one relationships in Django. |
| **Authentication flow setup** | Learned to implement and debug JWT authentication between backend and React frontend. |
| **Database migration issues** | Improved confidence in managing PostgreSQL databases and migrations. |
| **API connection errors** | Built skill in debugging 404/500 responses and ensuring consistent REST design. |
| **Design consistency** | Maintained royal color palette and unified brand identity across frontend and backend. |

---

<p align="center" style="color:#2A4628; font-weight:600; margin-top:40px;">
Developed by Lujain Al Sultan
</p>
