import os,secrets
from PIL import Image
from letdeal import app,db
from flask import render_template,request,redirect,url_for,make_response,after_this_request,flash
from flask_login import login_user,logout_user,login_required,current_user
from letdeal.forms import LoginForm,ProfileForm,SellerForm,ProductForm,BuyForm
from letdeal.models import User, Address, Seller, Category, Product, Order, OrderItem


@app.route("/")
def index():
    if current_user.is_authenticated:
        print("yes")
    return render_template("index.html")


@app.route("/nav")
def nav():
    # products = Product.query.all()
    product_id = request.args.get('product_id',type=str)
    select_product = Product.query.filter_by(product_id=product_id).first()
    return render_template("test.html",select_product=select_product)

@app.route("/categorylist")
def category_list():
    category_id = request.args.get('category_id','0',str)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("category_list.html",products=products)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    varify = request.args.get("varify",0,type=int)
    number = form.phone_number.data
    if varify and form.otp.data ==123456:
        user = User.query.filter_by(phone=str(number)).first()
        if user:
            login_user(user)
            print(user)
            return redirect(url_for("index"))
        
        else:
            @after_this_request
            def set_cookies(response):
                res = response
                res.set_cookie("phone",str(number))
                return res           
            return redirect(url_for("profile"))
    return render_template("login.html",form=form)

@app.route("/profile",methods=['GET','POST'])
def profile():
    form = ProfileForm()
    phone =request.cookies.get("phone")
    print(phone)
    if form.validate_on_submit():
        add_user = User(name=form.name.data,email=form.email.data,phone=phone)
        db.session.add(add_user)
        db.session.commit()
        new_user = User.query.filter_by(name=form.name.data,email=form.email.data,phone=phone).first()
        add_address = Address(user_id=new_user.user_id,street=form.street.data,city=form.city.data,
                              state=form.state.data,postal_code=form.postal_code.data,country=form.country.data)
        db.session.add(add_address)
        db.session.commit()
        login_user(new_user)
        flash("User as Created")
        return redirect(url_for("index"))
    return render_template("profile.html",form=form)

@app.route("/seller",methods=['GET','POST'])
@login_required
def seller():
    form = SellerForm()
    seller = Seller.query.filter_by(user_id=current_user.user_id).first()
    if seller and request.method=="get":
        return redirect('product')
    
    if form.validate_on_submit():
        print("yse")
        add_seller = Seller(user_id=current_user.user_id,factory_name=form.factory_name.data,
                            description=form.description.data,requirement=form.requirement.data)
        db.session.add(add_seller)
        db.session.commit()
        return redirect(url_for("product"))
    
    return render_template("seller.html",form=form)


def save_image(image_file):
    random_hax = secrets.token_hex(8)
    _,f_ext = os.path.splitext(image_file.filename)
    image_filename = random_hax+f_ext
    image_path = os.path.join(app.root_path,'static/category',image_filename)
    img_size = (400,400)
    img = Image.open(image_file)
    img.thumbnail(img_size)
    img.save(image_path)
    return image_filename

@app.route("/product",methods=["GET","POST"])
@login_required
def product():
    form = ProductForm()
    seller = Seller.query.filter_by(user_id=current_user.user_id).first()
    if seller is None:
        return redirect('seller')
    
    products = Product.query.filter_by(Seller_id=seller.seller_id).all()
    category = request.args.get('category','None',str)
    product_img = (url_for('static',filename='category/'))
    print(category)
    if form.validate_on_submit() and category == 'addproduct':
        if form.image.data:
            img_file = save_image(form.image.data)
        print("yse")
        add_product = Product(Seller_id=seller.seller_id,name=form.product_name.data,description=form.description.data,
                              price=form.price.data,category_id=form.category_id.data,stock_quantity=form.quantity.data,image_url=img_file)
        db.session.add(add_product)
        db.session.commit()
        return redirect(url_for("product"))
    
    if request.method == 'GET' and category == 'edit':
        product_id = request.args.get('product_id',type=str)
        editproduct = Product.query.filter_by(product_id=product_id).first()
        print(editproduct.category.name)
        form.category_id.data = editproduct.category.name
        form.product_name.data = editproduct.name
        form.description.data = editproduct.description
        form.price.data = editproduct.price
        form.quantity.data = editproduct.stock_quantity
        form.image.data = editproduct.image_url
        print("edit called",product_id)
        return render_template("product.html",form=form,products=products,data={'category':'editproduct','h1':'Edit Product','product_id':product_id})
    
    if category == 'editproduct' and form.validate_on_submit():
        print("edit Session")
        product_id = request.args.get('product_id',type=str)
        editproduct = Product.query.filter_by(product_id=product_id).first()
        category = Category.query.filter_by(category_id=form.category_id.data).first()
        if form.image.data:
            img_file = save_image(form.image.data)
            editproduct.image_url = img_file

        editproduct.category.name  = category.name
        editproduct.name =form.product_name.data
        editproduct.description =form.description.data
        editproduct.price =form.price.data
        editproduct.stock_quantity =form.quantity.data
        print(category.name)
        db.session.commit()
        return redirect(url_for('product'))

    return render_template("product.html",form=form,products=products,product_img=product_img,data={'category':'addproduct','h1':'Add Product','product_id':'product_id'})


@app.route("/buyform",methods=['GET','POST'])
@login_required
def buyform():
    form = BuyForm()
    product_id = request.args.get('product_id',type=str)
    select_product = Product.query.filter_by(product_id=product_id).first()

    if form.validate_on_submit():
        shipping = Address.query.filter_by(user_id=current_user.user_id).first()
        products = Product.query.filter_by(product_id=form.product_id.data).first()
        products.stock_quantity -= form.quantity.data
        add_order = Order(user_id=current_user.user_id,total_amount=(form.quantity.data*products.price),
                          shipping_address_id=shipping.address_id,billing_address_id=products.Seller_id)
        db.session.add(products)
        db.session.add(add_order)
        db.session.commit()
        product = Order.query.order_by(Order.order_date.desc()).filter_by(user_id=current_user.user_id,total_amount=(form.quantity.data*products.price)).first()
        add_orderitem = OrderItem(order_id =product.order_id ,product_id=form.product_id.data,quantity=form.quantity.data,
                                 price_at_purchase=form.purchase_price.data)
        db.session.add(add_orderitem)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("buyform.html",form=form,select_product=select_product)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/category",methods=['GET','POST'])
def category():
    categorys = Category.query.all()
    if request.method == 'POST':
        names = request.form.get('names')
        print(names)
        new_name = Category(name=names)
        db.session.add(new_name)
        db.session.commit()
    return render_template("category.html",categorys=categorys)



@app.route("/errors")
def errors():
    # u = Order.query.filter_by(user_id=current_user.user_id).first()
 
    return redirect(url_for('index'))
    