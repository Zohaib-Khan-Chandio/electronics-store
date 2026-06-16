# Electronics Store Web Application

A complete, feature-rich e-commerce web application built using **Flask (Python)** and **MongoDB** for searching, reviewing, and buying electronic products.

---

## ✨ Features

* **Search & Discovery:** Users can search for any electronic product instantly.
* **Smart Filtering:** Products can be filtered and sorted by price (**Low to High** or **High to Low**).
* **Product Details & Reviews:** View comprehensive product details, including product name, description, price, and user reviews.
* **Dynamic Review System:** Users can leave reviews on products, which are dynamically stored and embedded within the corresponding product document in MongoDB.
* **Order Management:** Every completed purchase order is securely stored in a dedicated MongoDB orders collection.
* **Checkout & Payments:** Users can purchase products securely by entering their payment details during checkout.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS
* **Database:** MongoDB (NoSQL)

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Zohaib-Khan-Chandio/electronics-store.git
cd electronics-store
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup MongoDB 🍃

Make sure you have MongoDB Compass installed locally or are using MongoDB Atlas (Cloud).

Ensure your MongoDB server is running on:

```text
mongodb://localhost:27017/
```

(Optional) Populate the database with sample data:

```bash
python seed.py
```

### 4. Start the Flask Server

```bash
python app.py
```

### 5. Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

The application should now be running locally.
