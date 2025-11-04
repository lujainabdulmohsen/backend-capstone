<div align="center" style="background: linear-gradient(135deg, #002E47, #2A4628); padding: 40px 20px; border-radius: 20px; color: #ffffff;">
  
  <h1 style="font-size: 2.5rem; margin-bottom: 10px;">Yusr Backend</h1>
  <h3 style="color: #CDE4DA;">Django REST API for the Yusr Government Services Assistant</h3>
  
</div>

---

## 1. Project Overview  

The **Yusr Backend** provides a secure and scalable REST API for the Yusr full-stack application.  
It manages user authentication, government agencies, services, service requests, appointments, traffic fines, and bank accounts.

---

## 2. Tech Stack  

| Layer | Tools & Frameworks |
|-------|---------------------|
| **Language** | Python 3.13 |
| **Framework** | Django 5, Django REST Framework |
| **Database** | PostgreSQL |
| **Authentication** | JWT (SimpleJWT) |
| **Environment Management** | pipenv, dotenv |
| **Deployment** | Docker, docker-compose |
| **Version Control** | Git, GitHub |

---

## 3. User Stories  

| ID | User Story | Feature Implemented |
|----|-------------|--------------------|
| 1 | As a user, I can create an account and log in securely. | JWT Authentication |
| 2 | As a user, I can view available government agencies and services. | Agencies & Services |
| 3 | As a user, I can create and track my service requests. | Service Requests |
| 4 | As a user, I can view and pay my traffic fines. | Traffic Fines |
| 5 | As a user, I can manage my appointments. | Appointments |
| 6 | As a user, I can add, edit, and delete my bank account. | Bank Account |

---

## 4. CRUD Features  

| Model | Create | Read | Update | Delete |
|--------|---------|-------|---------|---------|
| **User** | ✅ | ✅ | ✅ | ❌ |
| **Service Request** | ✅ | ✅ | ✅ | ✅ |
| **Appointment** | ✅ | ✅ | ✅ | ✅ |
| **Traffic Fine** | Admin | ✅ | ✅ | ❌ |
| **Bank Account** | ✅ | ✅ | ✅ | ✅ |

---

## 5. Installation & Setup  

```bash
git clone https://github.com/<your-username>/yusr-backend.git
cd yusr-backend
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver

---

## **6. Icebox Features**

| Feature | Description |
|----------|-------------|
| **AI-based document verification** | Extract data from uploaded documents using AI. |
| **Multi-language support** | Arabic and English interface. |
| **Notification system** | Automatic reminders for appointments and payments. |
| **Role-based access control** | Permissions for admins and users. |

---

## **7. Challenges & Key Takeaways**

- Designed multiple relational models with Django ORM.  
- Implemented secure authentication using JWT.  
- Built and tested API endpoints with Django REST Framework.  
- Integrated backend with the React frontend.  

---

### **Developed by Lujain Al Sultan**
