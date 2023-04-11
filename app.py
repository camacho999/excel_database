from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pandas as pd

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SECRET_KEY'] = 'MYKEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIÓNS'] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    edad = db.Column(db.Integer)
    sexo = db.Column(db.String(10))

    def __init__(self, nombre, apellido, correo, edad, sexo):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.edad = edad
        self.sexo = sexo



@app.route('/')
def index():
    titulo = "Home!"
    lista = ['footer', 'header', 'waca']
    return render_template('index.html', titulo=titulo, lista = lista)

@app.route('/upload')
def upload_file():
    return render_template('post_form.html', usuarios = Usuario.query)

@app.route('/uploader', methods = ['POST'])
def uploader():
    file = request.files['file']
    df = pd.read_excel(file)
    for _, row in df.iterrows():
       usuario = Usuario(nombre = row['Nombre'], apellido = row['Apellido'], correo = row['Correo'], edad = row['Edad'], sexo = row['Sexo'])
       db.session.add(usuario)
    db.session.commit()
    return redirect('/upload') 

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    