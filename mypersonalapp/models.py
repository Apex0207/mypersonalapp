import datetime
from mypersonalapp import db

class Partners(db.Model):
    p_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    p_email = db.Column(db.String(255), nullable=False)
    p_pass = db.Column(db.String(255), nullable=False)
    p_fname = db.Column(db.String(255), nullable=False)
    p_lname = db.Column(db.String(255), nullable=False)
    p_address = db.Column(db.Text(), nullable=True)
    p_phone = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    patvehicle = db.relationship('Vehicle', back_populates ='vehiclepat')
    partner = db.relationship('PartnerBank', back_populates ='partnerbank')


    #create the foreign keys

class Clients(db.Model):
    c_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    c_email = db.Column(db.String(255), nullable=False)
    c_pass = db.Column(db.String(255), nullable=False)
    c_fname = db.Column(db.String(255), nullable=False)
    c_lname = db.Column(db.String(255), nullable=False)
    c_address = db.Column(db.Text(), nullable=True)
    c_phone = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    crequest = db.relationship('Request', back_populates ='requestc')



class Manufacturers(db.Model):
    man_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    man_name = db.Column(db.String(255), nullable=False)

    #set up the relationship
    manmod = db.relationship('Models', back_populates ='modman')

class Models(db.Model):
    mod_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    mod_name = db.Column(db.String(255), nullable=False)
    man_id = db.Column(db.Integer(), db.ForeignKey("manufacturers.man_id"))
    mod_color = db.Column(db.String(255), nullable=False)
    mod_year = db.Column(db.String(255), nullable=False)
    #set up the relationship
    modman = db.relationship('Manufacturers', back_populates ='manmod')
    modvehicle = db.relationship('Vehicle', back_populates ='vehiclemod')

class Vehicle(db.Model):
    v_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    mod_id = db.Column(db.Integer(), db.ForeignKey("models.mod_id"))
    v_color = db.Column(db.String(255), nullable=False)
    v_image = db.Column(db.String(255), nullable=False)
    reg_number = db.Column(db.String(255), nullable=False)
    mod_year = db.Column(db.String(255), nullable=False)
    p_id = db.Column(db.Integer(), db.ForeignKey("partners.p_id"))
    v_catid = db.Column(db.Integer(), db.ForeignKey("vehiclecategory.cat_id"))
    date_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #set up the relationship
    vehiclemod = db.relationship('Models', back_populates ='modvehicle')
    vehiclepat = db.relationship('Partners', back_populates ='patvehicle')
    vehiclecat = db.relationship('VehicleCategory', back_populates ='catvehicle')
    vrequest = db.relationship('Request', back_populates ='requestv')


class VehicleCategory(db.Model):
    __tablename__='vehiclecategory'
    cat_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cat_name = db.Column(db.String(255), nullable=False)

    #set up the relationship
    catvehicle = db.relationship('Vehicle', back_populates ='vehiclecat')



class PartnerBank(db.Model):
    pb_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pb_name = db.Column(db.String(255), nullable=False)
    acc_no = db.Column(db.String(255), nullable=False)
    acc_name = db.Column(db.String(255), nullable=False)
    p_id = db.Column(db.Integer(), db.ForeignKey("partners.p_id"))
    #set up the relationship
    partnerbank = db.relationship('Partners', back_populates ='partner')

class Request(db.Model):
    r_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    no_of_days = db.Column(db.String(255), nullable=False)
    ref = db.Column(db.String(100), nullable=False)
    v_id = db.Column(db.Integer(), db.ForeignKey("vehicle.v_id"))
    c_id = db.Column(db.Integer(), db.ForeignKey("clients.c_id"))
    r_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    #set up the relationship
    requestv = db.relationship('Vehicle', back_populates ='vrequest')
    requestc = db.relationship('Clients', back_populates ='crequest')
    requestpay = db.relationship('Payment', back_populates ='payrequest')

class Payment(db.Model):
    pay_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pay_method = db.Column(db.String(255), nullable=False)
    r_id = db.Column(db.Integer(), db.ForeignKey("request.r_id"))
    pay_amount = db.Column(db.Float(), nullable=False)
    pay_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    #set up the relationship
    payrequest = db.relationship('Request', back_populates ='requestpay')

class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin= db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow())

class Contactus(db.Model):
    contact_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=True)
    contact_message = db.Column(db.Text(), nullable=True)
