from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for

from flask_app import app

from flask_app.models.companies import Company
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.stars import Star
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
    
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form = {
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
    
    category = Category.get_by_company_id(form)
    
    dicc = {"company_id": session['company_id']}
    products = Product.get_by_company_id(dicc)
    
    return render_template('company/dashboard_company.html', company=company, products=products, category=category)


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
    
    form = {"company_id": id}
    products = Product.get_by_company_id(form)
    
    categories = Category.get_all()
    
    return render_template('company/company_profile.html', company=company, products=products, points=points, categories=categories)


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


@app.route('/search', methods=['post'])
def search():
    Company.get_by_search(request.form)
    
    return redirect('/searches/' + request.form['search'])


@app.route('/searches/<string:search>')
def searches(search):
    
    form = {"search": search}
    companies= Company.get_by_search(form)
    
    return render_template('index/searches.html', companies=companies)
