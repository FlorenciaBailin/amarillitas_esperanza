from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_app import app

from flask_app.models.companies import Company
from flask_app.models.products import Product


@app.route('/add/product')
def add_p():
    if 'company_id' not in session:
        return redirect('/')
    
    form = {"id": session['company_id']}
    company = Company.get_by_id(form)
    return render_template('products/add_product.html', company=company)


@app.route('/new_product', methods=['POST'])
def new_product():
    if 'company_id' not in session:
        return redirect('/')
    
    if not Product.validate_product(request.form):
        flash("Nombre y/o descripción deben tener más de dos caracteres", "product")
        return redirect('/add/product')
    
    Product.save(request.form)
    return redirect('/dashboard/company')


@app.route('/product/<int:id>')
def show_product(id):
    
    dicc = {"id": id}
    product = Product.get_by_id(dicc)
    
    return render_template('products/product.html', product=product)


@app.route('/edit/product/<int:id>')
def update_product(id):
    
    if 'company_id' not in session:
        return redirect('/')
    
    dicc = {"id": id}
    product = Product.get_by_id(dicc)
    
    return render_template('products/edit_product.html', product=product)


@app.route('/edit_product', methods=['POST'])
def edit_product():
    if 'company_id' not in session:
        return redirect('/')
    
    Product.update(request.form)
    return redirect('/dashboard/company')

@app.route('/delete/<int:id>')
def delete_product(id):
    
    if 'company_id' not in session:
        return redirect('/')
    
    dicc = {"id": id}
    Product.delete_product(dicc)
    return redirect('/dashboard/company')


