from flask import Flask, render_template, redirect, url_for, request, session, flash, redirect, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField, FileField, TextAreaField, DateField, TimeField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import relationship
import datetime
from io import BytesIO
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
import os
import math
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import asc, desc
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fasfasfasfas4f564as54f5as4f51as23f1as32'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/servieating'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
BASE_DIR = dirname(dirname(abspath(__file__)))
MEDIA_DIR = join(BASE_DIR, 'media')
POSTS_IMAGES_DIR = join(MEDIA_DIR, 'profileimages')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    iduser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    correo = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    tipo = db.Column(db.String(45))
    estatus = db.Column(db.String(45))
    fecharegistro = db.Column(db.DateTime, default=datetime.datetime.now)
    ultimavez = db.Column(db.DateTime)
    comensal = db.relationship('Comensal', lazy='dynamic')
    restaurantero = db.relationship('Restaurantero', lazy='dynamic')
    #comentariorest = db.relationship('Comentariorest', lazy='dynamic')
    #comentariomenu = db.relationship('Comentariomenu', lazy='dynamic')
    def get_id(self):
           return (self.iduser)

class Comensal(db.Model):
    idcomensal = db.Column(db.Integer, primary_key=True)
    user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    nombre = db.Column(db.String(100))
    apellidoP = db.Column(db.String(45))
    apellidoM = db.Column(db.String(45))
    fotourl = db.Column(db.String(200))
    calle = db.Column(db.String(45))
    numero = db.Column(db.String(45))
    cruzamiento1 = db.Column(db.String(45))
    cruzamiento2 = db.Column(db.String(45))
    colonia = db.Column(db.String(45))
    cp = db.Column(db.String(45), default='97700')
    telefono = db.Column(db.String(45))
    referencia = db.Column(db.String(100))
    user = db.relationship("User", backref="Comensal")
    megustarest = db.relationship("Megustarest", lazy="dynamic")
    megustamenu = db.relationship("Megustamenu", lazy="dynamic")
    
    def get_id(self):
           return (self.idcomensal)

class Restaurantero(db.Model):
    idrestaurantero = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fotourl = db.Column(db.String(200))
    user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    descripcion = db.Column(db.String(300))
    calle = db.Column(db.String(45))
    numero = db.Column(db.String(45))
    cruzamiento1 = db.Column(db.String(45))
    cruzamiento2 = db.Column(db.String(45))
    colonia = db.Column(db.String(45))
    cp = db.Column(db.String(45), default='97700')
    telefono = db.Column(db.String(45))
    url = db.Column(db.String(100))
    referencia = db.Column(db.String(100))
    tipo = db.Column(db.String(45))
    horarioinicial = db.Column(db.String(45))
    horariocierre = db.Column(db.String(45))
    diaslaborales = db.Column(db.String(45))
    diadescanso = db.Column(db.String(45))
    whatsapp = db.Column(db.String(45))
    eslogan = db.Column(db.String(100))
    facebook = db.Column(db.String(50))
    user = db.relationship("User", backref ='Restaurantero')
    menu = db.relationship("Menu", lazy="dynamic")
    megustarest = db.relationship("Megustarest", lazy="dynamic")
    comentariomenu = db.relationship("Comentariomenu", lazy="dynamic")
    #comentariorest = db.relationship("Comentariorest", lazy="dynamic")
    #megusta = db.relationship("Megustarest", backref="Restaurantero")
    def get_id(self):
        return (self.idrestaurantero)

class Menu(db.Model):
    idmenu = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200)) 
    precio = db.Column(db.String(45))
    estatus = db.Column(db.String(45))
    restaurantero_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    restaurantero_idrestaurantero = db.Column(db.Integer, db.ForeignKey('restaurantero.idrestaurantero'))
    fotourl = db.Column(db.String(200))
    tipo = db.Column(db.String(45))
    presentacion = db.Column(db.String(45))
    restaurantero = db.relationship("Restaurantero", backref='Menu')
    comentariomenu = db.relationship("Comentariomenu", backref='Menu')
    
    def get_id(self):
        return (self.idmenu)

class Comentariorest(db.Model):
    idcomentariorest = db.Column(db.Integer, primary_key=True)  
    restaurantero_idrestaurantero = db.Column(db.Integer, db.ForeignKey('restaurantero.idrestaurantero'))
    restaurantero_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    comentario = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    comensal_idcomensal = db.Column(db.Integer, db.ForeignKey('comensal.idcomensal'))
    comensal_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    #user = db.relationship("User", lazy="dynamic")
    comensal = db.relationship("Comensal", backref='Comentariorest')
    #user = db.relationship("User", foreign_keys=[user_iduser])
    def get_id(self):
        return (self.idcomentariorest)

class Comentariomenu(db.Model):
    idcomentariomenu = db.Column(db.Integer, primary_key=True)
    menu_idmenu = db.Column(db.Integer, db.ForeignKey('menu.idmenu'))
    menu_restaurantero_idrestaurantero = db.Column(db.Integer, db.ForeignKey('restaurantero.idrestaurantero'))
    menu_restaurantero_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    comentario = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    comensal_idcomensal = db.Column(db.Integer, db.ForeignKey('comensal.idcomensal'))
    comensal_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    comensal = db.relationship("Comensal", backref="Comentariomenu")
    #user = db.relationship("User", foreign_keys=[user_iduser], backref="Comentariomenu")
    
    #menu = db.relationship("Menu", backref="ComentarioMenu")
    
    def get_id(self):
        return (self.idcomentariomenu)

class Megustamenu(db.Model):
    idmegustamenu = db.Column(db.Integer, primary_key=True)
    menu_idmenu = db.Column(db.Integer, db.ForeignKey('menu.idmenu'))
    menu_restaurantero_idrestaurantero = db.Column(db.Integer, db.ForeignKey('restaurantero.idrestaurantero'))
    menu_restaurantero_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    estatus = db.Column(db.String(45))
    comensal_idcomensal = db.Column(db.Integer, db.ForeignKey('comensal.idcomensal'))
    comensal_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    #user = db.relationship("User", lazy="dynamic")
    comensal = db.relationship("Comensal", backref="Megustamenu")
    menu = db.relationship("Menu", backref="Megustamenu")
       
    def get_id(self):
        return (self.idmegustamenu)

class Megustarest(db.Model):
    idmegustarest = db.Column(db.Integer, primary_key=True)
    restaurantero_idrestaurantero = db.Column(db.Integer, db.ForeignKey('restaurantero.idrestaurantero'))
    restaurantero_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    estatus = db.Column(db.String(45))
    comensal_idcomensal = db.Column(db.Integer, db.ForeignKey('comensal.idcomensal'))
    comensal_user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    #user = db.relationship("User", backref="MeGustaRest")
    comensal = db.relationship("Comensal", backref="Megustarest")
    restaurantero = db.relationship("Restaurantero", backref="Megustarest")
       
    def get_id(self):
        return (self.idmegustarest)

class Mensaje(db.Model):
    idmensaje = db.Column(db.Integer, primary_key=True)
    user_iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'))
    asunto = db.Column(db.String(50))
    mensaje = db.Column(db.String(250))
    estado = db.Column(db.String(45))
    user = db.relationship("User", backref="Mensaje")
       
    def get_id(self):
        return (self.idmensaje)

class Pedido(UserMixin, db.Model):
    idpedido = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.String(100))
    total = db.Column(db.String(45))
    #menu_idmenu = db.Column(db.Integer, foreign_key=True)
    #menu_restaurantero_idrestaurantero = db.Column(db.Integer, foreign_key=True)
    #menu_restaurantero_user_iduser = db.Column(db.Integer, foreign_key=True)
    #comensal_idcomensal = db.Column(db.Integer, foreign_key=True)
    #comensal_user_iduser = db.Column(db.Integer, foreign_key=True)
    horaregistro = db.Column(db.DateTime, default=datetime.datetime.now)
    tiempoentrega = db.Column(db.String)
          
@login_manager.user_loader
def load_user(iduser):
    return User.query.get(int(iduser))

@login_manager.user_loader
def cargar_tipoUsuario(user_tipo):
    return User.query.get(user_tipo)

class LoginForm(FlaskForm):
    username = StringField('',validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('',validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Recordar')
    #msg = StringField('msg')

class RegisterForm(FlaskForm):
    correo = StringField('',validators=[InputRequired(), Email(message='Correo no válido'), Length(max=50)])
    username = StringField('',validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('',validators=[InputRequired(), Length(min=8, max=16)])
    tipo = SelectField('Escoja un tipo de usuario', choices=[('Comensal', 'Comensal'),('Restaurantero', 'Restaurantero')], validators=[InputRequired()])
    #aceptar = BooleanField('Acepto los términos y condiciones', validators=[InputRequired(message="Por favor selecciona esta casilla para terminar el registro")])

class RegisterCambiarDatosForm(FlaskForm):
    correo = StringField('Correo',validators=[InputRequired(), Email(message='Correo no válido'), Length(max=50)])
    username = StringField('Usuario',validators=[InputRequired(), Length(min=4, max=15)])

class RegisterCambiarContraseñaForm(FlaskForm):
    password = PasswordField('Ingrese la nueva contraseña',validators=[InputRequired(), Length(min=8, max=16)])

##### Formularios del Comensal #############
class RegisterCambiarNombreComensal(FlaskForm):
    nombre = StringField('Nombre(s)',validators=[InputRequired(), Length(min=4, max=50)])
    apellidoP = StringField('Apellido Paterno',validators=[InputRequired(), Length(min=2, max=50)])   
    apellidoM = StringField('Apellido Materno',validators=[InputRequired(), Length(min=2, max=50)]) 
    calle = StringField('Calle',validators=[InputRequired(), Length(min=1, max=50)])
    numero = StringField('Número',validators=[InputRequired(), Length(min=2, max=50)])   
    cruzamiento1 = StringField('Cruzamiento 1',validators=[InputRequired(), Length(min=2, max=50)])  
    cruzamiento2 = StringField('Cruzamiento 2',validators=[InputRequired(), Length(min=2, max=50)]) 
    colonia = StringField('Colonia',validators=[InputRequired(), Length(min=2, max=50)])
    #cp = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    telefono = StringField('Teléfono',validators=[InputRequired(), Length(min=2, max=50)])
    referencia = TextAreaField('Referencias',validators=[InputRequired(), Length(min=2, max=100)])

class RegisterCambiarDireccionComensal(FlaskForm):
    calle = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    numero = StringField('',validators=[InputRequired(), Length(min=2, max=50)])   
    cruzamiento1 = StringField('',validators=[InputRequired(), Length(min=2, max=50)])  
    cruzamiento2 = StringField('',validators=[InputRequired(), Length(min=2, max=50)]) 
    colonia = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    cp = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    telefono = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    referencia = TextAreaField('',validators=[InputRequired(), Length(min=2, max=100)])

class BuscarForm(FlaskForm):
    buscar = StringField('',validators=[InputRequired(), Length(min=4, max=100)])
    opciones = SelectField('Buscar por:', choices=[('Nombre', 'Nombre'),('Cena', 'Cena'),
    ('Almuerzo', 'Almuerzo'),('Desayuno', 'Desayuno'), ('Panadería', 'Panadería'),
    ('Pastelería', 'Pastelería'), ('Carrito', 'Carrito'), ('Puesto', 'Puesto')], validators=[InputRequired()])

##### Formularios del Restaurantero #######
class RegisterCambiarNombreRest(FlaskForm):
    nombre = StringField('Nombre',validators=[InputRequired(), Length(min=4, max=50)])
    facebook = StringField('Facebook',validators=[InputRequired(), Length(min=4, max=50)])
    descripcion = TextAreaField('Descripción',validators=[InputRequired(), Length(min=4, max=300)])
    url = StringField('Página web')
    tipo = SelectField('Escoja su tipo de negocio', choices=[('Restaurante', 'Restaurante'),('Lonchería', 'Lonchería'),
    ('Cocina Ecónomica', 'Cocina Ecónomica'),('Pizzería', 'Pizzería'), ('Panadería', 'Panadería'),
    ('Pastelería', 'Pastelería'), ('Carrito', 'Carrito'), ('Puesto', 'Puesto'), ('Marisquería', 'Marisquería'), ('Taquería', 'Taquería')], validators=[InputRequired()])
    horario1 = TimeField('De', validators=[InputRequired()])
    horario2 = TimeField('A', validators=[InputRequired()])
    diaslaboral = SelectField('Días Laborales', choices=[('Lunes a Viernes', 'Lunes a Viernes'),('Lunes a Domingo', 'Lunes a Domingo'),('Viernes, Sábado y Domingo', 'Viernes, Sábado y Domingo'),
    ('Lunes, Miércoles y Viernes', 'Lunes, Miércoles y Viernes'),('Martes y Jueves', 'Martes y Jueves'),('Martes, Miércoles y Jueves', 'Martes, Miércoles y Jueves')
    ,('Jueves, Viernes, Sábado y Domingo', 'Jueves, Viernes, Sábado y Domingo'),('Sábado y Domingo', 'Sábado y Domingo'),('Lunes', 'Lunes'),('Martes', 'Martes'),('Miércoles', 'Miércoles'),('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),('Sábado', 'Sábado'),('Domingo', 'Domingo')], validators=[InputRequired()])
    diadescanso = SelectField('Día de Descanso', choices=[('Lunes', 'Lunes'),('Martes', 'Martes'),('Miércoles', 'Miércoles'),('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),('Sábado', 'Sábado'),('Domingo', 'Domingo'), ('Sin descanso','Sin descanso')], validators=[InputRequired()])
    eslogan = StringField('Eslogan',validators=[InputRequired(), Length(min=4, max=100)])
    calle = StringField('Calle',validators=[InputRequired(), Length(min=1, max=50)])
    numero = StringField('Número',validators=[InputRequired(), Length(min=2, max=50)])   
    cruzamiento1 = StringField('Cruzamiento 1',validators=[InputRequired(), Length(min=2, max=50)])  
    cruzamiento2 = StringField('Cruzamiento 2',validators=[InputRequired(), Length(min=2, max=50)]) 
    colonia = StringField('Colonia',validators=[InputRequired(), Length(min=2, max=50)])
    #cp = StringField('',validators=[InputRequired(), Length(min=2, max=50)])
    telefono = StringField('Teléfono',validators=[InputRequired(), Length(min=10, max=12)])
    referencia = TextAreaField('Referencias',validators=[InputRequired(), Length(min=2, max=100)]) 
    whatsapp = StringField('WhatsApp',validators=[InputRequired(), Length(min=10, max=12)])
    
class RegisterCambiarDireccionRest(FlaskForm):
    pass

class RegisterMenuForm(FlaskForm):
    nombre = StringField('',validators=[InputRequired(), Length(min=4, max=45)])
    descripcion = TextAreaField('',validators=[InputRequired(), Length(min=4, max=200)])
    precio = StringField('Precio',validators=[InputRequired(), Length(min=1, max=6)])
    estatus = SelectField('Estatus', choices=[('Disponible', 'Disponible'),('No Disponible', 'No Disponible')], validators=[InputRequired()])
    tipo = SelectField('Tipo', choices=[('Comida', 'Comida'),('Bebida', 'Bebida'), ('Entremés', 'Entremés'), ('Postre', 'Postre'),
    ('Antojito', 'Antojito'), ('Plato Fuerte', 'Plato Fuerte'), ('Desayuno', 'Desayuno'), ('Almuerzo', 'Almuerzo'), ('Cena', 'Cena'),
    ('Botana','Botana'), ('Especial',('Especial'))], validators=[InputRequired()])
    presentacion = SelectField('Tipo', choices=[('Pieza', 'Pieza'),('Orden', 'Orden'), ('Paquete', 'Paquete'), ('Combo', 'Combo'),
    ('1/4 Litro', '1/4 Litro'), ('1/2 Litro', '1/2 Litro'), ('1 Litro', '1 Litro'), ('Grande', 'Grande'), ('Mediano', 'Mediano'), ('Chico', 'Chico'),
    ('Rebanada', 'Rebanada')], validators=[InputRequired()])

class RegisterFormComensal(FlaskForm):    
    
    nombre = StringField('',validators=[InputRequired(), Length(min=4, max=30)])
    apellidoP = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    apellidoM = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    calle = StringField('',validators=[InputRequired(), Length(min=1, max=30)])
    numero = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cruzamiento1 = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cruzamiento2 = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    colonia = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cp = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    referencia = TextAreaField('',validators=[InputRequired(), Length(min=2, max=100)])
    telefono = StringField('',validators=[InputRequired(), Length(min=10, max=10)])
    foto = FileField('selecciona imagen:')

class RegisterFormRestaurantero(FlaskForm):
    nombre = StringField('',validators=[InputRequired(), Length(min=4, max=100)])
    descripcion = TextAreaField('',validators=[InputRequired(), Length(min=2, max=300)])
    url = StringField('',validators=[InputRequired(), Length(min=2, max=100)])
    calle = StringField('',validators=[InputRequired(), Length(min=1, max=30)])
    numero = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cruzamiento1 = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cruzamiento2 = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    colonia = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    cp = StringField('',validators=[InputRequired(), Length(min=2, max=30)])
    referencia = TextAreaField('',validators=[InputRequired(), Length(min=2, max=100)])
    telefono = StringField('',validators=[InputRequired(), Length(min=10, max=10)])
    tipo = SelectField('', choices=[('Restaurante', 'Restaurante'),('Lonchería', 'Lonchería'),
    ('Cocina Ecónomica', 'Cocina Ecónomica'),('Fonda', 'Fonda'), ('Pizzería', 'Pizzería'), ('Panadería', 'Panadería'),
    ('Pastelería', 'Pastelería'), ('Carrito', 'Carrito'), ('Puesto', 'Puesto')], validators=[InputRequired()])
    horario1 = SelectField('', choices=[('06:00 AM', '06:00 AM'),('07:00 AM', '07:00 AM'),('08:00 AM', '08:00 AM'),
    ('09:00 AM', '09:00 AM'),('10:00 AM', '10:00 AM'),('11:00 AM', '11:00 AM')
    ,('12:00 PM', '12:00 PM'),('01:00 PM', '01:00 PM'),('02:00 PM', '02:00 PM'),('03:00 PM', '03:00 PM'),('04:00 PM', '04:00 PM'),
    ('05:00 PM', '05:00 PM'),('06:00 PM', '06:00 PM'),('07:00 PM', '07:00 PM'),('08:00 PM', '08:00 PM'),
    ('09:00 PM', '09:00 PM'),('10:00 PM', '10:00 PM'),('11:00 PM', '11:00 PM'),('12:00 PM', '12:00 PM')], validators=[InputRequired()])
    horario2 = SelectField('', choices=[('06:00 AM', '06:00 AM'),('07:00 AM', '07:00 AM'),('08:00 AM', '08:00 AM'),
    ('09:00 AM', '09:00 AM'),('10:00 AM', '10:00 AM'),('11:00 AM', '11:00 AM')
    ,('12:00 PM', '12:00 PM'),('01:00 PM', '01:00 PM'),('02:00 PM', '02:00 PM'),('03:00 PM', '03:00 PM'),('04:00 PM', '04:00 PM'),
    ('05:00 PM', '05:00 PM'),('06:00 PM', '06:00 PM'),('07:00 PM', '07:00 PM'),('08:00 PM', '08:00 PM'),
    ('09:00 PM', '09:00 PM'),('10:00 PM', '10:00 PM'),('11:00 PM', '11:00 PM'),('12:00 PM', '12:00 PM')], validators=[InputRequired()])
    
class FormBusqueda(FlaskForm):
    buscar =  StringField('')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()      
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                #session['user'] = form.username.data       
                tipoUsuario = user.tipo
                estatus = user.estatus                
                print(datetime.datetime.now())
                if tipoUsuario == 'Comensal' and estatus == 'Permitido':
                    user.ultimavez = datetime.datetime.now()
                    db.session.commit() 
                    return redirect(url_for('home'))  
                else:
                    if tipoUsuario == 'Restaurantero' and estatus == 'Permitido':
                        user.ultimavez = datetime.datetime.now()
                        db.session.commit() 
                        return redirect(url_for('homeRest')) 
                    else:
                       flash('Lo sentimos, su cuenta esta supendida.') 
                       return redirect(url_for('login'))                              
        flash('El usuario o password son incorrectos', 'warning')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('¡Ya existe un usuario registrado con ese nombre!')
                return redirect(url_for('signup')) 
            else:
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(username=form.username.data, correo=form.correo.data, password=hashed_password, tipo=form.tipo.data, estatus="Permitido")       
                db.session.add(new_user)
                db.session.commit()
                flash('Usuario registrado correctamente')
                return redirect(url_for('login')) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)  
        return render_template('error.html')                                 
    return render_template('signup.html', form=form)

######## rutas del comensal #######
@app.route('/perfilComensal', methods=['GET', 'POST'])
@login_required
def perfilComensal():   
    iduser=current_user.iduser 
    com2 = Comensal.query.filter_by(user_iduser=iduser).first() 
    #com2.nombre
    print(iduser)
    us = User.query.get(iduser)  
    form = RegisterFormComensal()
    form2 = RegisterForm()
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    
    if comensalId.first() is not None:
        print('Existe')  
        com = Comensal.query.filter_by(user_iduser=iduser).first()
        session['comensalid'] = com.idcomensal
        print(com.idcomensal)  
        if form.validate_on_submit():   
            us.username = form2.username.data
            us.correo = form2.correo.data           
            c = Comensal.query.get(com.idcomensal)
            c.nombre = form.nombre.data
            c.apellidoP = form.apellidoP.data
            c.apellidoM = form.apellidoM.data
            c.calle = form.calle.data
            c.numero = form.numero.data
            c.cruzamiento1 = form.cruzamiento1.data
            c.cruzamiento2 = form.cruzamiento2.data
            c.cp = form.cp.data
            c.telefono = form.telefono.data
            c.referencia = form.referencia.data
            c.colonia = form.colonia.data
            db.session.commit()           
            flash('Datos actualizados correctamente', 'info')
            return redirect(url_for("perfilComensal"))     
       
    else:
        print('No Existe')
        if form.validate_on_submit():     
            hashed_password = generate_password_hash(form2.password.data, method='sha256')
            #us.username = form2.username.data
            us.username = form2.username.data
            us.correo = form2.correo.data
            #us.password = hashed_password
            print(us.username)        
            perfilComensal = Comensal(user_iduser=iduser, nombre=form.nombre.data, apellidoP=form.apellidoP.data, apellidoM=form.apellidoM.data,
            calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
            colonia=form.colonia.data, cp=form.cp.data, telefono=form.telefono.data, referencia=form.referencia.data)
            db.session.add(perfilComensal)
            db.session.commit()
            flash('Datos agregados correctamente', 'info')
            return redirect(url_for("perfilComensal"))  
        else:
            flash('Los datos no se agregaron', 'warning')                      
    
    return render_template('perfilComensal.html', form=form, form2=form2, user=us, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarContraseña', methods=['GET', 'POST'])
def cambiarContraseña():
    iduser=current_user.iduser   
    form = RegisterCambiarContraseñaForm()    
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    hashed_password = generate_password_hash(form.password.data, method='sha256')
    try:
        if form.validate_on_submit():   
            us.password = hashed_password     
            db.session.commit()           
            flash('Contraseña actualizada correctamente')
            return redirect(url_for("home")) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                   
    return render_template('cambiarContraseña.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/subirImagenComensal', methods=['GET', 'POST'])
@login_required
def subirImagenComensal():
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    
    if request.method == 'POST':  
        imagen = request.files['imagenFile']             
        com2 = Comensal.query.filter_by(user_iduser=iduser).first()        
        print(iduser)       
        comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
        no = str(current_user.iduser)    
        nombre_imagen = secure_filename(no + '_' + imagen.filename)
        ruta_imagen = os.path.abspath('../Proyecto-ServiEating/static/profile-pictures/{}'.format(nombre_imagen))
        ruta_html = '../static/profile-pictures/{}'.format(nombre_imagen)
       
        if comensalId.first() is not None:
            print('Existe')             
            print(ruta_html)
            imagen.save(ruta_imagen)   
            com.fotourl = ruta_html
            db.session.commit()
            flash('Imagen actualizada correctamnete', 'info')
            return redirect(url_for("datosComensal"))     
       
        else:
            print('No Existe')     
            imagen.save(ruta_imagen)           
            perfilComensal = Comensal(user_iduser=iduser, fotourl=ruta_html)
            db.session.add(perfilComensal)
            db.session.commit()
            flash('Imagen subida correctamente', 'info')
            return redirect(url_for("datosComensal"))  
    else:
        return render_template("subirImagenComensal.html", datos=com, user=us, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarDatos', methods=['GET', 'POST'])
@login_required
def cambiarDatos():
    iduser=current_user.iduser   
    form = RegisterCambiarDatosForm()    
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    flash('Si vas a cambiar el nombre de usuario y/o correo, asegurate de que no sean los mismos que los actuales.')
    try:
        if form.validate_on_submit():  
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('¡Ya existe un usuario registrado con ese nick!')
                return redirect(url_for('cambiarDatos')) 
            else: 
                us.username = form.username.data
                us.correo = form.correo.data           
                db.session.commit()           
                flash('Datos actualizados correctamente')
                return redirect(url_for("datosComensal"))       
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                   
    return render_template('cambiarDatos.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarNombreComensal', methods=['GET', 'POST'])
@login_required
def cambiarNombreComensal():
    iduser=current_user.iduser   
    form = RegisterCambiarNombreComensal()    
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    try:
       
        if form.validate_on_submit():  
            if comensalId.first() is not None: #si existen los datos del usuario
                com.nombre = form.nombre.data
                com.apellidoP = form.apellidoP.data 
                com.apellidoM = form.apellidoM.data
                com.calle = form.calle.data
                com.numero = form.numero.data 
                com.cruzamiento1 = form.cruzamiento1.data    
                com.cruzamiento2 = form.cruzamiento2.data    
                com.colonia = form.colonia.data               
                com.telefono = form.telefono.data
                com.referencia = form.referencia.data          
                db.session.commit()           
                flash('Datos actualizados correctamente')
                return redirect(url_for("datosComensal")) 
            else: # no existen los datos del usuario
                ruta_html = '../static/perfil02blanco.png'
                perfilComensal = Comensal(user_iduser=iduser, nombre=form.nombre.data, apellidoP=form.apellidoP.data, apellidoM=form.apellidoM.data, fotourl=ruta_html,
                calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
                colonia=form.colonia.data, telefono=form.telefono.data, referencia=form.referencia.data)
                db.session.add(perfilComensal)
                db.session.commit()
                flash('Datos agregados correctamente')
                return redirect(url_for("datosComensal")) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                   
    return render_template('cambiarNombreComensal.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarDireccionComensal', methods=['GET', 'POST'])
@login_required
def cambiarDireccionComensal():
    iduser=current_user.iduser   
    form = RegisterCambiarDireccionComensal()    
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    try:
        if comensalId.first() is not None:
            form.referencia.data = com.referencia  
        if form.validate_on_submit():   
            if comensalId.first() is not None: #si existen los datos del usuario
                com.calle = form.calle.data
                com.numero = form.numero.data 
                com.cruzamiento1 = form.cruzamiento1.data    
                com.cruzamiento2 = form.cruzamiento2.data    
                com.colonia = form.colonia.data
                com.cp = form.cp.data   
                com.telefono = form.telefono.data
                com.referencia = form.referencia.data   
                db.session.commit()           
                flash('Datos actualizados correctamente')
                return redirect(url_for("datosComensal")) 
            else: # no existen los datos del usuario
                ruta_html = '../static/perfil02blanco.png'
                perfilComensal = Comensal(user_iduser=iduser, calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
                colonia=form.colonia.data, cp=form.cp.data, telefono=form.telefono.data, referencia=form.referencia.data, fotourl=ruta_html)
                db.session.add(perfilComensal)
                db.session.commit()
                flash('Datos agregados correctamente')
                return redirect(url_for("datosComensal"))  
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e) 
                                      
    return render_template('cambiarDireccionComensal.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/restaurantesComensal', methods=['GET', 'POST'])
@login_required
def restaurantesComensal():
    form = FormBusqueda()
    iduser=current_user.iduser 
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    page = request.args.get('page', 1, type=int)  
    rest1=Restaurantero.query.paginate(page=page, per_page=5, error_out=False)
    #rest1 = Restaurantero.query.join(Megustarest).filter(Megustarest.restaurantero_idrestaurantero == Restaurantero.idrestaurantero).all()
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    try:       
        rest= Restaurantero.query.join(Menu).order_by(Restaurantero.idrestaurantero).all()
        menu=Menu.query.filter_by(restaurantero_idrestaurantero=Restaurantero.idrestaurantero).all()
        totalMeGusta = Megustarest.query.all()
        print(menu)
        if comensalId.first() is not None:
            #meGusta = Megustarest.query.filter_by(comensal_idcomensal=com.idcomensal).all()
            meGusta = Megustarest.query.join(Comensal).filter(Comensal.user_iduser == Megustarest.comensal_user_iduser).filter(Megustarest.restaurantero_idrestaurantero==Restaurantero.idrestaurantero)
            if meGusta.all() is not None:
                print("Si")
            else:
                print("No")           
        else:
            meGusta=""
        return render_template('restaurantesComensal.html',total=totalMeGusta, me=meGusta, form=form, menu=menu, rest=rest1, name=current_user.username, datos=com)
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                    
    return render_template('restaurantesComensal.html', datos=com, form=form,name=current_user.username)

@app.route('/buscarRestaurantesComensal', methods=['GET', 'POST'])
@login_required
def buscarRestaurantesComensal():
    form = FormBusqueda()
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    try:
        #buscar       
        buscar = request.form.get('buscar')
        rest1=Restaurantero.query.filter(Restaurantero.nombre.ilike(f'%{buscar}%')).all()
        #termina buscar   
        return render_template('buscarRestComensal.html', form=form, rest=rest1, name=current_user.username, datos=com, buscar=buscar)
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                    
    return render_template('buscarRestComensal.html', datos=com,form=form,name=current_user.username)

@app.route('/buscarMenuComensal', methods=['GET', 'POST'])
@login_required
def buscarMenuComensal():
    form = FormBusqueda()
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    try:  
        
        rest1=Restaurantero.query.all()
        #c=Menu.query.filter(Menu.restaurantero_idrestaurantero==rest.idrestaurantero).count()
        #buscar   
        page = request.args.get('page', 1, type=int)    
        buscar = request.form.get('buscar')
       
        
        rest1=Menu.query.filter_by(estatus='Disponible').filter(or_(Menu.nombre.ilike(f'%{buscar}%'),Menu.tipo.ilike(f'%{buscar}%'))).all()
        #termina buscar 
        rest= Restaurantero.query.filter(Restaurantero.nombre.ilike==('%form.buscar.data%')).all()
        menu=Menu.query.filter_by(restaurantero_idrestaurantero=Restaurantero.idrestaurantero).all()
        print(menu)
        return render_template('buscarMenuComensal.html', form=form, menu=menu, rest=rest1, name=current_user.username, datos=com, buscar=buscar)
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                    
    return render_template('buscarMenuComensal.html', form=form,name=current_user.username, datos=com)

@app.route('/contacto', methods=['GET', 'POST'])
@login_required
def contacto():
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    return render_template('contacto.html', name=current_user.username, datos=com)

@app.route('/home')
@login_required
def home():   
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    return render_template('home.html', name=current_user.username, datos=com)

@app.route('/menuComensal')
@login_required
def menuComensal():
    iduser=current_user.iduser 
    rest2 = Restaurantero.query.filter_by(user_iduser=iduser).first()   
    rest3=Restaurantero.query.all()  
    session.pop('buscar',None)
    rest = Restaurantero.query.filter_by(user_iduser=iduser).first()#id foranea de restaurantero_idrestaurantero
   
    page = request.args.get('page', 1, type=int)
    c= Menu.query.filter_by(estatus='Disponible').join(Restaurantero).order_by(Menu.restaurantero_idrestaurantero).paginate(page=page, per_page=10, error_out=False)
    d=Restaurantero.query.join(Menu).all()
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    
    return render_template('menuComensal.html', menu=c, res= d, name=current_user.username, datos=com)

@app.route('/datosComensal', methods=['GET', 'POST'])
@login_required
def datosComensal():
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()    
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
            
    return render_template('datosComensal.html', user=us, datos=com, name=current_user.username)

@app.route('/misPedidos',methods=['GET', 'POST'])
def misPedidos():
    c= Menu.query.join(Restaurantero).all()
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    return render_template('misPedidos.html', menu=c, datos=com)

@app.route('/restaurante/<id>', methods=['GET', 'POST'])
def restaurante(id):
    print(id)
    form = BuscarForm()
    time = datetime.datetime.now()
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    m = Restaurantero.query.filter_by(idrestaurantero=id).first()
    print(m.user_iduser)
    #rest2 = Menu.query.filter_by(restaurantero_user_iduser=m).all()     
    print(m)   
    page = request.args.get('page', type=int, default=1)
    pageComen = request.args.get('pageComen', type=int, default=1)
    menu=Menu.query.filter_by(estatus='Disponible').filter_by(restaurantero_user_iduser=m.user_iduser).paginate(page=page, per_page=5, error_out=False)
    especiales=Menu.query.filter_by(estatus='Disponible').filter_by(restaurantero_user_iduser=m.user_iduser).filter_by(tipo='Especial').all()
    comen = Comentariorest.query.filter_by(restaurantero_idrestaurantero=id).order_by(desc(Comentariorest.fecha)).paginate(page=pageComen, per_page=5, error_out=False)
    totalComentarios = Comentariorest.query.filter_by(restaurantero_idrestaurantero=id).count()
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    totalMeGusta = Megustarest.query.filter_by(restaurantero_idrestaurantero=id).count()
    if comensalId.first() is not None:
        meGusta = Megustarest.query.filter_by(restaurantero_idrestaurantero=id).filter_by(comensal_idcomensal=com.idcomensal).first()
    else:
        meGusta=""
    #pagination = Pagination(page=page, total=45)
    return render_template('restaurante.html',  totalComentarios=totalComentarios, comen=comen, especiales=especiales, me=meGusta, total=totalMeGusta, time=time, form= form, user=us, datos=com, menu=menu, res=m, name=current_user.username)

@app.route('/deleteComentarioRest/<id>/<idrest>', methods=['GET', 'POST', 'DELETE'])
def deleteComentarioRest(id, idrest):
    print(id)
    m = Comentariorest.query.filter_by(idcomentariorest=id).delete()
    db.session.commit()
    flash('Comentario eliminado correctamente')
    return redirect(url_for('restaurante', id=idrest))

@app.route('/comentarRest/<id>', methods=['GET', 'POST'])
def comentarRest(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    res = Restaurantero.query.filter_by(idrestaurantero=id).first()
    comen = Comentariorest.query.filter_by(restaurantero_idrestaurantero=id).all()
    #verificar = Comentariomenu.query.join(Comensal).filter(Comensal.idcomensal == Comentariomenu.comensal_idcomensal)
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    try:
        if comensalId.first() is not None:    
            comentario = request.form.get('comentario')
            add = Comentariorest(restaurantero_idrestaurantero=id, restaurantero_user_iduser=res.user_iduser,
            comensal_user_iduser=iduser,comensal_idcomensal=com.idcomensal,comentario=comentario)
            db.session.add(add)
            db.session.commit()
            flash('Comentario añadido')
        else:
            flash('No puedes comentar hasta que tus datos esten completos, por favor actualizalos.')
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)             
    #m = Restaurantero.query.filter_by(idrestaurantero=id).first()     
    return redirect(url_for('restaurante', id=id))

@app.route('/buscarMenuRest/<id>', methods=['GET', 'POST'])
def buscarMenuRest(id):
    print(id)
    form = BuscarForm()
    time = datetime.datetime.now()
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    m = Restaurantero.query.filter_by(idrestaurantero=id).first()
    print(m.user_iduser)
    #rest2 = Menu.query.filter_by(restaurantero_user_iduser=m).all()     
    print(m)  
    buscar = request.form.get('buscar')
    print(buscar)
    page = request.args.get('page', type=int, default=1)
    menu2=Menu.query.filter_by(restaurantero_user_iduser=m.user_iduser).paginate(page=page, per_page=5, error_out=False).items 
    menu=Menu.query.filter_by(restaurantero_user_iduser=m.user_iduser).filter(Menu.nombre.ilike(f'%{buscar}%')).all()
        
    
    return render_template('buscarMenuRest.html', time=time, form= form, user=us, datos=com, menu=menu,  menu2=menu2, res=m, name=current_user.username, buscar=buscar)

@app.route('/meGusta/<id>', methods=['GET', 'POST'])
def meGusta(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    m = Restaurantero.query.filter_by(idrestaurantero=id).first()
    estatus = "Me Gusta"
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:
        add = Megustarest(restaurantero_idrestaurantero=id,restaurantero_user_iduser=m.user_iduser,comensal_idcomensal=com.idcomensal,
        comensal_user_iduser=com.user_iduser, estatus=estatus)
        db.session.add(add)
        db.session.commit()
        flash("¡Se ha añadido a tus favoritos!")
    else:
        flash("No puedes dar me gusta hasta que tus datos esten completos")

    print("Te Gusta")    
    return redirect(url_for('restaurante', id=id))

@app.route('/noMeGusta/<id>', methods=['GET', 'POST'])
def noMeGusta(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    m = Restaurantero.query.filter_by(idrestaurantero=id).first()
    estatus = "Ya No Me Gusta"
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    actualizar = Megustarest.query.filter_by(restaurantero_idrestaurantero=id).filter_by(comensal_idcomensal=com.idcomensal).first()
    print(actualizar.idmegustarest)
    eliminar = Megustarest.query.filter_by(idmegustarest=actualizar.idmegustarest).delete()
    db.session.commit()
    flash("¡Se ha quitado de tus favoritos")
   

    print("Te Gusta")    
    return redirect(url_for('restaurante', id=id))

@app.route('/verComida/<id>', methods=['GET', 'POST'])
def verComida(id):
    print(id)
    page = request.args.get('page', type=int, default=1)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    comen = Comentariomenu.query.filter_by(menu_idmenu=id).order_by(desc(Comentariomenu.fecha)).paginate(page=page, per_page=5, error_out=False)
    menu=Menu.query.filter_by(idmenu=id).first()
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    totalComentarios = Comentariomenu.query.filter_by(menu_idmenu=id).count()
    totalMeGusta = Megustamenu.query.filter_by(menu_idmenu=id).count()
    if comensalId.first() is not None:        
        meGusta = Megustamenu.query.filter_by(menu_idmenu=id).filter_by(comensal_idcomensal=com.idcomensal).first()     
    else:
        meGusta=""
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    print(menu)
    return render_template('verComida.html',  me=meGusta, total=totalMeGusta,totalComentarios=totalComentarios, comen=comen, user=us, datos=com, menu=menu,  name=current_user.username)

@app.route('/deleteComentarioMenu/<id>/<idmenu>', methods=['GET', 'POST', 'DELETE'])
def deleteComentarioMenu(id, idmenu):
    print(id)
    m = Comentariomenu.query.filter_by(idcomentariomenu=id).delete()
    db.session.commit()
    flash('Comentario eliminado correctamente')
    return redirect(url_for('verComida', id=idmenu))

@app.route('/meGustaComida/<id>', methods=['GET', 'POST'])
def meGustaComida(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    p = Menu.query.filter_by(idmenu=id).first()
    print(p.restaurantero_idrestaurantero)
    m = Restaurantero.query.filter_by(idrestaurantero=p.restaurantero_idrestaurantero).first()
    estatus = "Me Gusta"
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:
        add = Megustamenu(menu_idmenu=id, menu_restaurantero_idrestaurantero=m.idrestaurantero, menu_restaurantero_user_iduser=m.user_iduser,
        comensal_idcomensal=com.idcomensal, comensal_user_iduser=com.user_iduser, estatus=estatus)
        db.session.add(add)
        db.session.commit()
        flash("¡Se ha añadido a tus comidas favoritas!")
    else:
        flash("No lo puedes añadir a tus favoritos si tus datos no estan completos, por favor actualizalos")

    print("Te Gusta")    
    return redirect(url_for('verComida', id=id))

@app.route('/noMeGustaComida/<id>', methods=['GET', 'POST'])
def noMeGustaComida(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()
    p = Menu.query.filter_by(idmenu=id).first()
    m = Megustamenu.query.filter_by(idmegustamenu=id).first()
    estatus = "Ya No Me Gusta"
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    actualizar = Megustamenu.query.filter_by(menu_restaurantero_idrestaurantero=p.restaurantero_idrestaurantero).filter_by(comensal_idcomensal=com.idcomensal).first()
    #print(actualizar.idmegustarest)
    eliminar = Megustamenu.query.filter_by(idmegustamenu=actualizar.idmegustamenu).delete()
    db.session.commit()
    flash("¡Se ha quitado de tus favoritos")  
    print("Ya No Te Gusta")    
    return redirect(url_for('verComida', id=id))

@app.route('/comentarMenu/<id>', methods=['GET', 'POST'])
def comentarMenu(id):
    print(id)
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first() 
    comen = Comentariomenu.query.filter_by(menu_idmenu=id).all()
    #verificar = Comentariomenu.query.join(Comensal).filter(Comensal.idcomensal == Comentariomenu.comensal_idcomensal)
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    try:
        if comensalId.first() is not None:
            menu=Menu.query.filter_by(idmenu=id).first()
            print(menu)
            comentario = request.form.get('comentario')
            add = Comentariomenu(menu_idmenu=id, menu_restaurantero_idrestaurantero=menu.restaurantero.idrestaurantero, menu_restaurantero_user_iduser=menu.restaurantero.user_iduser,
            comensal_user_iduser=iduser,comensal_idcomensal=com.idcomensal,comentario=comentario)
            db.session.add(add)
            db.session.commit()
            flash('Comentario añadido')
        else:
            flash('No puedes comentar hasta que tus datos esten completos, por favor actualizalos.')
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)             
    #m = Restaurantero.query.filter_by(idrestaurantero=id).first()     
    return redirect(url_for('verComida', id=id))

@app.route('/comidasFavoritas/', methods=['GET', 'POST'])
def comidasFavoritas():
    iduser=current_user.iduser 
    d=Restaurantero.query.join(Menu).all()
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    page = request.args.get('page', 1, type=int)
    buscar = request.form.get('buscar')
    #if session['search']:
        #buscar = session['search']
        
    #elif request.method == 'POST':
        #buscar = request.form.get('buscar')
        #session['search'] = buscar
        #if buscar:
            #pass
        #else:
            #session.pop('buscar',None)
    rest = Restaurantero.query.filter_by(user_iduser=iduser).first()#id foranea de restaurantero_idrestaurantero
    
    if buscar:      
        menu = Megustamenu.query.filter_by(comensal_user_iduser=iduser).join(Menu).filter(or_(Menu.nombre.ilike(f'%{buscar}%'),Menu.tipo.ilike(f'%{buscar}%'))).order_by(desc(Megustamenu.idmegustamenu)).paginate(page=page, per_page=10, error_out=False)               
    else:      
        menu = Megustamenu.query.filter_by(comensal_user_iduser=iduser).order_by(desc(Megustamenu.idmegustamenu)).paginate(page=page, per_page=10, error_out=False)
    
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    return render_template('comidasFavoritas.html', menu=menu, buscar=buscar,res= d, name=current_user.username, datos=com)

@app.route('/ajax', methods=["GET", "POST"])             
def ajax():
    if request.method == "POST":
        buscar = request.form.get('buscar')
        iduser=current_user.iduser  
        us = User.query.get(iduser)  
        com = Comensal.query.filter_by(user_iduser=iduser).first()    
        page = request.args.get('page', 1, type=int)
    
        menu = Megustamenu.query.filter_by(comensal_user_iduser=iduser).join(Menu).filter(Menu.nombre.ilike(f'%{buscar}%')).order_by(desc(Megustamenu.idmegustamenu)).paginate(page=page, per_page=1, error_out=False)           
        jsonify(menu)
        return render_template("comidasFavoritas.html", datos_modificados=menu,name=current_user.username, datos=com)

@app.route('/restFavoritos/', methods=['GET', 'POST'])
def restFavoritos():
    iduser=current_user.iduser 
    rest2 = Restaurantero.query.filter_by(user_iduser=iduser).first()   
    rest3=Restaurantero.query.all()  
    #restId = Restaurantero.query.get(rest2)#restaurantero_idrestaurantero
    rest = Restaurantero.query.filter_by(user_iduser=iduser).first()#id foranea de restaurantero_idrestaurantero
    
    page = request.args.get('page', 1, type=int)
    c= Menu.query.filter_by(estatus='Disponible').join(Restaurantero).order_by(Menu.restaurantero_idrestaurantero).paginate(page=page, per_page=10, error_out=False)
    d=Restaurantero.query.join(Menu).all()
    us = User.query.get(iduser) 
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
   
    
    comensalId = User.query.join(Comensal).filter(Comensal.user_iduser == iduser)
    if comensalId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    
    #menu=Menu.query.order_by('restaurantero_idrestaurantero').all()
    return render_template('restFavoritos.html', menu=c, res= d, name=current_user.username, datos=com)

####### rutas del restaurantero ########
@app.route('/perfilRest', methods=['GET', 'POST'])
@login_required
def perfilRest():
    
    iduser=current_user.iduser 
    rest2 = Restaurantero.query.filter_by(user_iduser=iduser).first()    
    
    #rest2.nombre
    print(iduser)
    us = User.query.get(iduser)  
    form = RegisterFormRestaurantero()
    form2 = RegisterForm()
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    
    if restId.first() is not None:
        print('Existe')  
        rest = Restaurantero.query.filter_by(user_iduser=iduser).first()
        rest.idrestaurantero
        print(rest.idrestaurantero)  
        if form.validate_on_submit():  
            us.username = form2.username.data
            us.correo = form2.correo.data           
            c = Restaurantero.query.get(rest.idrestaurantero)
            c.nombre = form.nombre.data
            c.descripcion = form.descripcion.data
            c.url = form.url.data
            c.calle = form.calle.data
            c.numero = form.numero.data
            c.cruzamiento1 = form.cruzamiento1.data
            c.cruzamiento2 = form.cruzamiento2.data
            c.cp = form.cp.data
            c.telefono = form.telefono.data
            c.referencia = form.referencia.data
            c.colonia = form.colonia.data
            c.tipo = form.tipo.data
            hor1 = form.horario1.data
            hor2 = form.horario2.data
            horacompuesta = hor1 + " - " +hor2
            c.horario = horacompuesta
            db.session.commit()           
            flash('Datos actualizados correctamente', 'info')
            return redirect(url_for("perfilRest"))           
    else:
        print('No Existe')
        if form.validate_on_submit():     
            hashed_password = generate_password_hash(form2.password.data, method='sha256')
            us.username = form2.username.data
            us.correo = form2.correo.data
            #us.password = hashed_password
            print(us.username) 
            hor1 = form.horario1.data
            hor2 = form.horario2.data
            horacompuesta = hor1 + " - " +hor2       
            perfilRest = Restaurantero(user_iduser=iduser, nombre=form.nombre.data, descripcion=form.descripcion.data,
            calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
            colonia=form.colonia.data, cp=form.cp.data, telefono=form.telefono.data, url=form.url.data, referencia=form.referencia.data,tipo=form.tipo.data, horario=horacompuesta)
            db.session.add(perfilRest)
            db.session.commit()
            flash('Datos agregados correctamente', 'info')
            return redirect(url_for("perfilRest"))  
        else:
            flash('Los datos no se agregaron', 'warning')                      
    
    return render_template('perfilRest.html', form=form, form2=form2, rest=rest2, user=us,name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarDatosRest', methods=['GET', 'POST'])
@login_required
def cambiarDatosRest():
    iduser=current_user.iduser   
    form = RegisterCambiarDatosForm()    
    com = Comensal.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    flash('Si vas a cambiar el nombre de usuario y/o correo, asegurate de que no sean los mismos que los actuales.')
    try:
        if form.validate_on_submit(): 
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('¡Ya existe un usuario registrado con ese nick!')
                return redirect(url_for('cambiarDatosRest')) 
            else: 
                us.username = form.username.data
                us.correo = form.correo.data           
                db.session.commit()           
                flash('Datos actualizados correctamente')
                return redirect(url_for("datosRest")) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                   
    return render_template('cambiarDatosRest.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/subirImagenRest', methods=['GET', 'POST'])
@login_required
def subirImagenRest():
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()
    try:
        if request.method == 'POST':  
            imagen = request.files['imagenFile']             
            com2 = Restaurantero.query.filter_by(user_iduser=iduser).first()        
            print(iduser)       
            restlId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
            no = str(current_user.iduser)    
            nombre_imagen = secure_filename(no + '_' + imagen.filename)
            ruta_imagen = os.path.abspath('../Proyecto-ServiEating/static/profile-pictures/{}'.format(nombre_imagen))
            ruta_html = '../static/profile-pictures/{}'.format(nombre_imagen)
       
            if restlId.first() is not None:
             print('Existe')             
             print(ruta_html)
             imagen.save(ruta_imagen)   
             com.fotourl = ruta_html
             db.session.commit()
             flash('Imagen actualizada correctamente', 'info')
             return redirect(url_for("datosRest"))     
       
            else:
             print('No Existe')     
             imagen.save(ruta_imagen)           
             perfilRest = Restaurantero(user_iduser=iduser, fotourl=ruta_html)
             db.session.add(perfilRest)
             db.session.commit()
             flash('Imagen subida correctamente', 'info')
             return redirect(url_for("datosRest"))  
        else:
            return render_template("subirImagenRest.html", datos=com, user=us, name=current_user.username, iduser=current_user.iduser)
    except Exception as e:
        print("Ha ocurrido algo mal")
        print(e)
    return render_template("subirImagenRest.html", datos=com, user=us, name=current_user.username, iduser=current_user.iduser)
    
@app.route('/cambiarNombreRest', methods=['GET', 'POST'])
@login_required
def cambiarNombreRest():
    iduser=current_user.iduser   
    form = RegisterCambiarNombreRest()    
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)   
    try:           
        if form.validate_on_submit():            
            #horaCompuesta = hor1 + " - " + hor2
            #horaInicial = datetime.strftime(hor1, '%H:%M:%S %p').time()
            #print(horaInicial)
            h1=str(form.horario1.data)
            h2=str(form.horario2.data)
            hor1 = "2020-07-26" + " " + h1
            hor2 = "2020-07-26" + " " + h2
            if restId.first() is not None: #si existen los datos del usuario
                com.nombre = form.nombre.data
                com.descripcion = form.descripcion.data 
                com.url = form.url.data  
                com.tipo = form.tipo.data 
                com.horarioinicial = hor1
                com.horariocierre = hor2
                com.diaslaborales = form.diaslaboral.data
                com.diadescanso = form.diadescanso.data 
                com.eslogan = form.eslogan.data  
                com.calle = form.calle.data
                com.numero = form.numero.data 
                com.cruzamiento1 = form.cruzamiento1.data    
                com.cruzamiento2 = form.cruzamiento2.data    
                com.colonia = form.colonia.data               
                com.telefono = form.telefono.data
                com.referencia = form.referencia.data  
                com.whatsapp = form.whatsapp.data 
                com.facebook = form.facebook.data   
                db.session.commit()           
                flash('Datos actualizados correctamente')
                return redirect(url_for("datosRest")) 
            else: # no existen los datos del usuario
                ruta_html = '../static/restblanco.png'
                perfilRest = Restaurantero(user_iduser=iduser, nombre=form.nombre.data, descripcion=form.descripcion.data, url=form.url.data, 
                fotourl=ruta_html, tipo=form.tipo.data, horarioinicial=hor1, horariocierre=hor2, diaslaborales=form.diaslaboral.data, diadescanso=form.diadescanso.data, eslogan=form.eslogan.data,
                calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
                colonia=form.colonia.data, telefono=form.telefono.data, referencia=form.referencia.data, whatsapp=form.whatsapp.data,  facebook=form.facebook.data)
                db.session.add(perfilRest)
                db.session.commit()
                flash('Datos agregados correctamente')
                return redirect(url_for("datosRest")) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)  
                           
    return render_template('cambiarNombreRest.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarDireccionRest', methods=['GET', 'POST'])
@login_required
def cambiarDireccionRest():
    iduser=current_user.iduser   
    form = RegisterCambiarDireccionRest()    
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    try:
        if restId.first() is not None: 
            form.referencia.data = com.referencia
        else:
            form.referencia.data = form.referencia.data 
        if form.validate_on_submit():   
            if restId.first() is not None: #si existen los datos del usuario
                com.calle = form.calle.data
                com.numero = form.numero.data 
                com.cruzamiento1 = form.cruzamiento1.data    
                com.cruzamiento2 = form.cruzamiento2.data    
                com.colonia = form.colonia.data
                com.cp = form.cp.data   
                com.telefono = form.telefono.data
                com.referencia = form.referencia.data  
                com.whatsapp = form.whatsapp.data 
                db.session.commit()           
                flash('Datos actualizados correctamente')   
                return redirect(url_for("datosRest")) 
            else: # no existen los datos del usuario
                ruta_html = '../static/restblanco.png'
                perfilRest = Restaurantero(user_iduser=iduser, calle=form.calle.data, numero=form.numero.data, cruzamiento1=form.cruzamiento1.data, cruzamiento2=form.cruzamiento2.data,
                colonia=form.colonia.data, cp=form.cp.data, telefono=form.telefono.data, referencia=form.referencia.data, fotourl=ruta_html, whatsapp=form.whatsapp.data)
                db.session.add(perfilRest)
                db.session.commit()
                flash('Datos agregados correctamente')
                return redirect(url_for("datosRest"))  
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                     
    return render_template('cambiarDireccionRest.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/cambiarContraseñaRest', methods=['GET', 'POST'])
def cambiarContraseñaRest():
    iduser=current_user.iduser   
    form = RegisterCambiarContraseñaForm()    
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()  
    us = User.query.get(iduser) 
    hashed_password = generate_password_hash(form.password.data, method='sha256')
    try:
        if form.validate_on_submit():   
            us.password = hashed_password     
            db.session.commit()           
            flash('Contraseña actualizada correctamente')
            return redirect(url_for("homeRest")) 
        
    except Exception as e:
        print("No se ha podido actualizar los datos")
        print(e)                                   
    return render_template('cambiarContraseñaRest.html', form=form, user=us, datos=com, name=current_user.username, iduser=current_user.iduser)

@app.route('/datosRest', methods=['GET', 'POST'])
@login_required
def datosRest():
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()  
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    if restId.first() is not None:  
        pass
    else:
        
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
       
    return render_template('datosRest.html', user=us, datos=com, name=current_user.username)

@app.route('/contactoRest', methods=['GET', 'POST'])
@login_required
def contactoRest():    
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()
    return render_template('contactoRest.html', datos=com, name=current_user.username)

@app.route('/homeRest')
@login_required
def homeRest():
    iduser=current_user.iduser   
    com = Restaurantero.query.filter_by(user_iduser=iduser).first() 
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    if restId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    return render_template('homeRest.html', datos=com, name=current_user.username)

@app.route('/gestionMenu', methods=['GET', 'POST'])
@login_required
def gestionMenu():
    form = RegisterMenuForm()   
    iduser=current_user.iduser 
    us = User.query.get(iduser) 
    com = Restaurantero.query.filter_by(user_iduser=iduser).first()
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    try:
        if restId.first() is not None:                                        
            rest2 = Restaurantero.query.filter_by(user_iduser=iduser).first()     
            #restId = Restaurantero.query.get(rest2)#restaurantero_idrestaurantero
            rest = Restaurantero.query.filter_by(user_iduser=iduser).first()#id foranea de restaurantero_idrestaurantero
            rest.idrestaurantero#restaurantero_idrestaurantero
            rest.user_iduser#restaurantero_user_iduser
            print(rest.idrestaurantero)
            print(rest.user_iduser)
            menu=Menu.query.filter_by(restaurantero_idrestaurantero=rest.idrestaurantero).all()
            if request.method == 'POST':  
                imagen = request.files['imagenFile']             
                #com2 = Restaurantero.query.filter_by(user_iduser=iduser).first()        
                print(iduser)                       
                no = str(current_user.iduser)    
                nombre_imagen = secure_filename(no + '_' + imagen.filename)
                ruta_imagen = os.path.abspath('../Proyecto-ServiEating/static/menu-pictures/{}'.format(nombre_imagen))
                ruta_html = '../static/menu-pictures/{}'.format(nombre_imagen)
                if form.validate_on_submit(): 
                    imagen.save(ruta_imagen)                               
                    menu = Menu(restaurantero_user_iduser=rest.user_iduser, restaurantero_idrestaurantero=rest.idrestaurantero, nombre=form.nombre.data, descripcion=form.descripcion.data,
                    precio=form.precio.data, estatus=form.estatus.data, tipo=form.tipo.data, fotourl=ruta_html, presentacion=form.presentacion.data)
                    db.session.add(menu)
                    db.session.commit()
                    flash('Comida agregada correctamente')
                    return redirect(url_for("gestionMenu")) 
                return render_template('gestionMenu.html', datos=com, menu=menu,form=form, name=current_user.username)
            else:
                return render_template('gestionMenu.html', datos=com, menu=menu, form=form, name=current_user.username)         
        else:
            flash('Para un óptimo rendimiento de esta función, le pedimos que actualice los datos del negocio, como información del mismo y dirección.') 
            #return render_template('homeRest.html', datos=com, name=current_user.username)
    except Exception as e:
        print("Ha ocurrido algo mal")
        print(e)
    return render_template('gestionMenu.html', datos=com, form=form, name=current_user.username)      

@app.route('/gestionPedidos')
@login_required
def gestionPedidos():
    restId = User.query.join(Restaurantero).filter(Restaurantero.user_iduser == iduser)
    if restId.first() is not None:  
        pass
    else:
        flash('Parece que tus datos no están completos, por favor actualizalos en el apartado de tu perfil') 
    return render_template('gestionPedidos.html', name=current_user.username)

@app.route('/deleteMenu/<id>', methods=['GET', 'POST', 'DELETE'])
def deleteMenu(id):
    print(id)
    m = Menu.query.filter_by(idmenu=id).delete()
    db.session.commit()
    flash('Comida eliminada correctamente')
    return redirect(url_for('gestionMenu'))

@app.route('/updateMenu/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def updateMenu(id):
    print(id)
    form = RegisterMenuForm()
    m = Menu.query.filter_by(idmenu=id).first()
    if form.validate_on_submit():
        pass
    db.session.commit()
    #flash('Comida eliminada correctamente')
    return redirect(url_for('gestionMenu'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/error')
def error():
    render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
