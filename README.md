
# 🚗 Vehicle Registration System

A complete **CRUD-based web application** built using **Flask**, **SQLite**, **Bootstrap UI**, and deployable on **Google Kubernetes Engine (GKE)**.  
The system allows **Franchise Owners** and **Customers** to manage vehicle registrations easily.

---

## 🚀 Features

### 👨‍💼 Franchise Owner
- Login to dashboard  
- View all vehicles under their franchise  
- Add new vehicles  
- Update existing vehicles  

### 👤 Customer
- Login to dashboard  
- View their own registered vehicles  
- Update vehicle details  

### ⚙️ System Features
- SQLite database  
- Flask SQLAlchemy ORM  
- User authentication with Flask-Login  
- Responsive UI using Bootstrap 5  
- Dockerized & ready for GKE deployment  
- Clean MVC-style project structure  

---

## 📁 Project Structure

```

vehicle_registry/
├── app/
│   ├── **init**.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       └── vehicle_form.html
├── static/
│   └── css/
│       └── style.css
├── run.py
├── requirements.txt
└── Dockerfile

````

---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/vehicle-registry.git
cd vehicle-registry
````

### **2️⃣ Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Application**

```bash
python run.py
```

✔️ App will start at:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 Default Login Credentials (Auto-Created)

### **Franchise Owner**

```
username: owner1
password: owner123
```

### **Customer**

```
username: customer1
password: cust123
```

---

## 🧪 How to Use

* Login using provided credentials
* Owners can see **all vehicles** of their franchise
* Customers can see **only their vehicles**
* Add, Edit, Update vehicle details from dashboard

---

## 🐳 Docker Support

### **Build Docker Image**

```bash
docker build -t vehicle-registry .
```

### **Run Container**

```bash
docker run -p 5000:5000 vehicle-registry
```

---

## ☁️ Deploy on Google Kubernetes Engine (GKE)

### **1️⃣ Tag & Push Image**

```bash
docker tag vehicle-registry gcr.io/<project-id>/vehicle-registry
docker push gcr.io/<project-id>/vehicle-registry
```

### **2️⃣ Apply Kubernetes Deployment**

```bash
kubectl apply -f deployment.yaml
```

### **3️⃣ Get Public External IP**

```bash
kubectl get service vehicle-registry-service
```

Access app using the **EXTERNAL-IP**.

---

## 🎨 UI / UX Highlights

* Clean & responsive Bootstrap layout
* Styled login form
* Dashboard with vehicle table
* Status highlighting (Active/Expired)
* User-friendly form design

---

## 📦 Technologies Used

* Python Flask
* SQLite
* SQLAlchemy
* Flask-Login
* Bootstrap 5
* Docker
* Google Kubernetes Engine (GKE)

---

## 🚀 Future Enhancements

* JWT-based API
* Role-based permissions
* Search & filtering on dashboard
* Migrate SQLite → Cloud SQL (Postgres)
* Add dark mode

---

## 👩‍💻 Author

**Shruti Goel**


