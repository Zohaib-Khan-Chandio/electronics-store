from flask import Flask, render_template, session, redirect, url_for, request
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = MongoClient(os.getenv("MONGO_URI"))
db = client["electronics"]

db.products.create_index([("category", ASCENDING)])
db.orders.create_index([("email", ASCENDING)])

@app.route("/")
def home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "")
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = category
    if sort == "low":
        products = list(db.products.find(query).sort("price", 1))
    elif sort == "high":
        products = list(db.products.find(query).sort("price", -1))
    else:
        products = list(db.products.find(query))
    categories = db.products.distinct("category")
    return render_template("home.html", products=products, categories=categories,
                           search=search, selected_category=category, sort=sort)

@app.route("/product/<id>")
def product(id):
    item = db.products.find_one({"_id": ObjectId(id)})
    return render_template("product.html", product=item)

@app.route("/add-to-cart/<id>", methods=["POST"])
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    cart = session["cart"]
    cart.append(id)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    cart_items = []
    total = 0
    for item_id in cart_ids:
        p = db.products.find_one({"_id": ObjectId(item_id)})
        if p:
            cart_items.append(p)
            total += p["price"]
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/remove-from-cart/<id>")
def remove_from_cart(id):
    cart = session.get("cart", [])
    cart.remove(id)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout")
def checkout():
    cart_ids = session.get("cart", [])
    if not cart_ids:
        return redirect(url_for("cart"))
    cart_items = []
    total = 0
    for item_id in cart_ids:
        p = db.products.find_one({"_id": ObjectId(item_id)})
        if p:
            cart_items.append(p)
            total += p["price"]
    return render_template("checkout.html", cart_items=cart_items, total=total)

@app.route("/place-order", methods=["POST"])
def place_order():
    cart_ids = session.get("cart", [])
    cart_items = []
    total = 0
    for item_id in cart_ids:
        p = db.products.find_one({"_id": ObjectId(item_id)})
        if p:
            cart_items.append({"name": p["name"], "price": p["price"]})
            total += p["price"]
            db.products.update_one(
                {"_id": ObjectId(item_id)},
                {"$inc": {"stock": -1}}
            )
    order = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "address": request.form.get("address"),
        "items": cart_items,
        "total": total,
        "status": "Pending",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db.orders.insert_one(order)
    session["cart"] = []
    return redirect(url_for("confirmation"))

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

@app.route("/my-orders", methods=["GET", "POST"])
def my_orders():
    orders = []
    email = ""
    if request.method == "POST":
        email = request.form.get("email")
        orders = list(db.orders.find({"email": email}))
    return render_template("my_orders.html", orders=orders, email=email)

@app.route("/submit-review/<id>", methods=["POST"])
def submit_review(id):
    review = {
        "reviewer": request.form.get("reviewer"),
        "comment": request.form.get("comment"),
        "rating": int(request.form.get("rating")),
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    db.products.update_one(
        {"_id": ObjectId(id)},
        {"$push": {"reviews": review}}
    )
    return redirect(url_for("product", id=id))

ADMIN_PASSWORD = "admin123"

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    products = list(db.products.find())
    orders = list(db.orders.find())
    low_stock = list(db.products.find({"stock": {"$lt": 3}}))
    categories = db.products.distinct("category")

    pipeline = [
        {"$group": {
            "_id": None,
            "total_revenue": {"$sum": "$total"},
            "total_orders": {"$sum": 1}
        }}
    ]
    report = list(db.orders.aggregate(pipeline))
    stats = report[0] if report else {"total_revenue": 0, "total_orders": 0}

    best_pipeline = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    best = list(db.orders.aggregate(best_pipeline))
    best_product = best[0]["_id"] if best else "No orders yet"

    return render_template("admin.html", products=products, orders=orders,
                           low_stock=low_stock, stats=stats,
                           best_product=best_product, categories=categories)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            error = "Wrong password!"
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/add-product", methods=["POST"])
def admin_add_product():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    category = request.form.get("category")
    if category == "__new__":
        category = request.form.get("new_category", "").strip()
    product = {
        "name": request.form.get("name"),
        "category": category,
        "price": int(request.form.get("price")),
        "description": request.form.get("description"),
        "image": request.form.get("image"),
        "stock": int(request.form.get("stock")),
        "reviews": []
    }
    db.products.insert_one(product)
    return redirect(url_for("admin"))

@app.route("/admin/delete-product/<id>")
def admin_delete_product(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    db.products.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("admin"))

@app.route("/admin/edit-product/<id>", methods=["GET", "POST"])
def admin_edit_product(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    product = db.products.find_one({"_id": ObjectId(id)})
    categories = db.products.distinct("category")
    if request.method == "POST":
        category = request.form.get("category")
        if category == "__new__":
            category = request.form.get("new_category", "").strip()
        db.products.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form.get("name"),
                "category": category,
                "price": int(request.form.get("price")),
                "description": request.form.get("description"),
                "image": request.form.get("image"),
                "stock": int(request.form.get("stock"))
            }}
        )
        return redirect(url_for("admin"))
    return render_template("edit_product.html", product=product, categories=categories)

@app.route("/admin/update-status/<id>", methods=["POST"])
def update_order_status(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    db.orders.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": request.form.get("status")}}
    )
    return redirect(url_for("admin_order_detail", id=id))

@app.route("/admin/order/<id>")
def admin_order_detail(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    order = db.orders.find_one({"_id": ObjectId(id)})
    return render_template("order_detail.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)