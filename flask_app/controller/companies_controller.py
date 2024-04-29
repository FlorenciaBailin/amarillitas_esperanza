from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
import pymysql
import pymysql.cursors

db = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="amarillitas")

from flask_app import app

from werkzeug.utils import secure_filename
import os

from flask_app.models.companies import Company
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.stars import Star
from flask_app.models.comments import Comment
from flask_app.models.categories import Category



from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    
    companies = Company.get_by_points()
    products = Product.get_by_updated()
    company = Company.get_all()
    categories = Category.get_all()
    return render_template('index/index.html', companies=companies, products=products, company=company, categories=categories)

@app.route('/register')
def new_user():

    return render_template('index/register.html')

@app.route('/register/company', methods=['POST'])
def register_company():
    
    if not Company.validate_company(request.form):
        return redirect('/register')
    
    if 'image' not in request.files:
        flash('No has seleccionado imagen', 'register_company')
        return redirect('/register')
    
    image = request.files['image']
    if image.filename == '':
        flash('Nombre de imagen vacío', 'register_company')
        return redirect('/register')
    
    img_name = secure_filename(image.filename)
    
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
    
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form = {
        "image": img_name,
        "name": request.form['name'],
        "cuit": request.form['cuit'],
        "adress": request.form['adress'],
        "description": request.form['description'],
        "phone": request.form['phone'],
        "category_id": request.form['category_id'],
        "email": request.form['email'],
        "password": pass_encrypt
    }
    
    
    
    new_id = Company.save(form)
    session['company_id'] = new_id
    return redirect('/dashboard/company')

@app.route('/dashboard/company')
def dashboard_company():
    if 'company_id' not in session:
        return redirect('/')
    
    form = {"id": session['company_id']}
    company = Company.get_by_id(form)
    
    form2 = {"id": session['company_id']}
    categories = Category.get_by_company_id(form2)
    
    dicc = {"id": session['company_id']}
    products = Product.get_by_company_id(dicc)
    
    category_select = Category.get_all()
    
    return render_template('company/dashboard_company.html', company=company, products=products, category=categories, category_select=category_select)


@app.route('/login')
def login():
    categories = Category.get_all()
    return render_template('index/login.html', categories=categories)


@app.route('/login/company', methods=['POST'])
def login_company():
    company = Company.get_by_email(request.form)
    if not company:
        flash("Email no registrado", "login")
        return redirect("/login")
    
    if not bcrypt.check_password_hash(company.password, request.form['password']):
        flash("Contraseña incorrecta", "login")
        return redirect('/login')
    
    session['company_id'] = company.id
    return redirect('/dashboard/company')



@app.route('/edit/company/<int:id>')
def edit_company(id):
    
    if 'company_id' not in session:
        return redirect('/')
    
    dicc = {"id": id}
    company = Company.get_by_id(dicc)
    
    return render_template('company/edit_company.html', company=company)


@app.route('/update/company', methods=['POST'])
def update_company():
    if 'company_id' not in session:
        return redirect('/')
    
    Company.update(request.form)
    
    return redirect('/dashboard/company')


@app.route('/logout/company')
def logout_company():
    session.clear()
    return redirect('/')



@app.route('/company/<int:id>')
def company_profile(id):
    
    dicc = {"id": id}
    company = Company.get_by_id(dicc)
    points = Company.company_points(dicc)
    
    form = {"id": id}
    products = Product.get_by_company_id(form)
    comments = Comment.get_by_company_id(form)
    
    categories = Category.get_all()
    
    return render_template('company/company_profile.html', company=company, products=products, points=points, categories=categories, comments=comments)


@app.route('/select/category', methods=['POST'])
def categories():

    # category_id = request.args.get('category_id')

    Category.get_by_company_id(request.form)

    return redirect('/category/' + request.form['category_id'])


@app.route('/category/<int:id>')
def show_categories(id):

    form = {"category_id": id}
    companies= Company.get_by_category(form)
    
    categories = Category.get_all()
    
    dicc = {"id": id}
    category = Category.get_by_id(dicc)
    
    return render_template('index/categories.html', companies=companies, categories=categories, category=category)


@app.route('/search', methods=['GET','POST'])
def search():
    
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if request.method == "POST" and "search" in request.form:
        sql= "SELECT * FROM products WHERE name LIKE '%" + request.form['search'] + "%' or description LIKE '%" + request.form['search'] + "%'"
    else:
        return redirect('/')
    cursor.execute(sql)
    products = cursor.fetchall()
    
    categories = Category.get_all()
    
    return render_template('index/searches.html', products=products, categories=categories)


@app.route('/searches/<string:search>')
def searches(search):
    
    form = {"search": search}
    companies= Company.get_by_search(form)
    
    
    return render_template('index/searches.html', companies=companies)
