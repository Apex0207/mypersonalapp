import json,random,math,os
from flask import session, make_response,render_template,request,redirect,flash,url_for
from sqlalchemy import desc
from mypersonalapp import app,db
from mypersonalapp.models import Admin,Partners,Manufacturers,Models, Vehicle
from mypersonalapp.forms import LoginForm,ContactusForm


@app.route('/')
def index():
    login=LoginForm()
    log=session.get('loggedin')
    if log == None:
        return render_template('index.html')
    else:
        userinfo = db.session.query(Partners).get(log)
        return render_template('index.html',login=login,log=log,userinfo=userinfo)



@app.route('/about')
def about():
    log=session.get('loggedin')
    if log == None:
        return redirect('/')
    else:
        userinfo = db.session.query(Partners).get(log)
    return render_template('about.html',userinfo=userinfo,log=log)

@app.route('/car')
def car():
    log=session.get('loggedin')
    if log == None:
        return redirect('/')
    else:
        userinfo = db.session.query(Partners).get(log)
    return render_template('car.html',userinfo=userinfo,log=log)

@app.route('/contact')
def contact():
    log=session.get('loggedin')
    if log == None:
        return redirect('/')
    else:
        userinfo = db.session.query(Partners).get(log)
    return render_template('contact.html',userinfo=userinfo,log=log)



@app.route('/service')
def service():
    log=session.get('loggedin')
    if log == None:
        return redirect('/')
    else:
        userinfo = db.session.query(Partners).get(log)
    return render_template('service.html',userinfo=userinfo,log=log)

@app.route('/signin')
def signin():
    log=session.get('loggedin')
    if log == None:
        return redirect('/')
    else:
        userinfo = db.session.query(Partners).get(log)
    return render_template('signin.html',userinfo=userinfo,log=log)

@app.route('/admin/login')
def admin_login():
    return render_template('adminlogin.html')


@app.route('/admin/submit/login', methods=['POST'])
def submit_adminlogin():
    username=request.form.get('username')
    adminpass=request.form.get('pwd')
    if username=='' or adminpass=='':
        flash('please complete both fields')
        return redirect(url_for('admin_login'))
    else:
        deets= Admin.query.filter(Admin.admin_username==username, Admin.admin_password==adminpass).first()
        if deets:
            id=Admin.admin_id
            session['admin'] = deets.admin_id
            return redirect(url_for('adminpage'))
        else:
            flash('Invalid login credentials')
            return redirect(url_for('admin_login'))

@app.route('/admin/page')
def adminpage():
    sess=session.get('admin')
    if sess==None:
        return redirect('/admin/login')
    else:
        sess1=db.session.query(Admin).get(sess)
        return render_template('admin/index.html',sess=sess,sess1=sess1)


@app.route('/admin/signout')
def admin_signout():
    session.pop('admin')
    return redirect('/admin/login')


# @app.route('/register')
# def register():
#     return render_template('register.html')



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        email=request.form.get('email')
        pwd1=request.form.get('pwd1')
        pwd2=request.form.get('pwd2')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        address=request.form.get('address')
        phone=request.form.get('phone')
        if email=='' or pwd1 == '' or fname== '' or lname== '' or address== '' or phone== '':
            flash('You need to complete all the fields')
            return redirect('/register')
        elif pwd1 != pwd2:
            flash('The two passwords do not match')
            return redirect('/register')
        else:
            u =Partners(p_email=email,p_pass=pwd1,p_fname=fname,p_lname=lname,p_address=address,p_phone=phone)
            db.session.add(u)
            db.session.commit()
            id = u.p_id
            session['loggedin']=id
            flash('Data inserted')
            return redirect('/')

@app.route('/user/login',methods=['POST','GET'])
def submit_login():
    login = LoginForm()
    username=request.form.get('username')
    pwd=login.pwd.data
    if request.method=='GET':
        return render_template('userlogin.html',login=login)
    if login.validate_on_submit():
        #deets= User.query.filter(User.user_email==username,User.user_pass==pwd).all()
        deets= Partners.query.filter(Partners.p_email==username).filter(Partners.p_pass==pwd).first()

        if deets:
            id = deets.p_id
            session['loggedin']=id
            return redirect('/')
            #retrieve his user_id and then keep in session
            #redirect him/her to userhome
        else:
            flash('Invalid Credentials...Please try again')
            return redirect('/user/login')
            #keep a failed message in flash,then redirect him to login again
    else:
        return render_template('index.html',login=login)


@app.route('/logout')
def user_logout():
    session.pop('loggedin')
    return redirect('/')

@app.route("/admin/addmanufacturers", methods=["POST","GET"])
def manufacturer():
    if request.method == 'GET':
        return render_template('add_man.html')
    else:
        #Retrieve form data (request.form....)
        manname = request.form.get('manname')

        b = Manufacturers(man_name=manname)
        db.session.add(b)
        db.session.commit()
        return redirect("/")

@app.route("/admin/addmodel", methods=["POST","GET"])
def model():
    if request.method == 'GET':
        return render_template('add_model.html')
    else:
        #Retrieve form data (request.form....)
        modname = request.form.get('modname')
        modcolor = request.form.get('modcolor')
        modyear = request.form.get('modyear')
        b = Models(mod_name=modname,mod_color=modcolor,mod_year=modyear)
        db.session.add(b)
        db.session.commit()
        return redirect("/")

@app.route('/post/details/<int:id>')
def post_details(id):
    loggedin = session.get('loggedin')
    userinfo = Partners.query.get(loggedin)
    if loggedin == None:
        return redirect('/')
    else:
        mandeets = db.session.query(Manufacturers).filter(Manufacturers.man_id==id).all()
        modeldeets=     Models.query.get_or_404(id)
        return render_template('car.html',modeldeets=modeldeets,userinfo=userinfo,mandeets=mandeets)



@app.route('/post/car', methods=['POST'])
def post_cars():
    #retrieve data
    manid=request.form.get('manid')
    manname=request.form.get('manname')
    c = Manufacturers(man_id=manid,man_name=manname)
    db.session.add(c)
    db.session.commit()

    return f"{manid} and {manname}"


@app.route('/rent/car',methods=['POST','GET'])
def rent_car():
    return render_template('rent.html')

@app.route("/request",methods=['GET','POST'])
def request_car():
    if request.method =='GET':
        return render_template('rent.html')
    else:
        noofdays=request.form.get('ndays')
        #generate a random number as transaction ref
        ref =int(random.random() * 1000000)
        session['refno']=ref #keep ref  in session
        #insert into database
        db.session.execute(f"INSERT INTO request SET no_of_days='{noofdays}',ref='{ref}'")
        db.session.commit()
        return redirect('/comfirmpay')


@app.route('/comfirmpay')
def comfirmpay():
    ref=session.get('refno')
    #run query to retrieve details of the donation
    qry= db.session.execute(f"SELECT * FROM request WHERE ref={ref}")
    data= qry.fetchone()
    return render_template("payconfirm.html",data=data)


@app.route('/admin/addvehicle', methods=['GET','POST'])
def addvehicle():
    if request.method =='GET':
        return render_template('add_vehicle.html')
    else:
        #Retrieve form data (request.form....)
        color = request.form.get('vcolor')
        regnumber = request.form.get('regnumber')
        pid = request.form.get('pid')
        year = request.form.get('vyear')
        catid = request.form.get('catid')
        modid = request.form.get('modid')

        #request file
        pic_object = request.files.get('image')
        original_file = pic_object.filename
        if color =='' or regnumber =='' or pid =='' or year =='' or catid =='' or modid =='':
            flash("Please complete all the fields")
            return render_template('add_vehicle.html')
        if original_file !='': #check if file is not empty
            extension = os.path.splitext(original_file)
            if extension[1].lower() in ['.jpg','.png','.jpeg']:
                fn = math.ceil(random.random() * 100000000)
                save_as = str(fn)+extension[1]
                pic_object.save(f"mypersonalapp/static/images/{save_as}")
                #insert other details into db
                b = Vehicle(v_color=color,v_image=save_as,reg_number=regnumber,p_id=pid,mod_year=year,v_catid=catid,mod_id=modid)
                db.session.add(b)
                db.session.commit()
                return redirect("/admin/page")
            else:
                flash('File Not Allowed')
                return render_template("add_vehicle.html")

        else:
            save_as =""
            b = Vehicle(v_color=color,v_image=save_as,reg_number=regnumber,p_id=pid,v_year=year,v_catid=catid,mod_id=modid)
            db.session.add(b)
            db.session.commit()
            return redirect("/admin/page")

@app.route('/admin/vehicle')
def vehicle():
    sess1=db.session.query(Admin).get(id)
    vehicle_deets=Vehicle.query.all()

    return render_template('/admin/index.html',vehicle_deets=vehicle_deets,sess1=sess1)

@app.route('/vehicle/details/<int:id>')
def vehicle_details(id):
    sess1=db.session.query(Admin).get(id)
    loggedin = session.get('loggedin')
    if loggedin == None:
        return redirect('/')
    else:
        vehicle_deets = db.session.query(Vehicle).filter(Vehicle.v_id==id).all()
        return render_template('admin/index.html',vehicle_deets=vehicle_deets,sess1=sess1)

@app.route('/admin/vehicle/delete/<id>')
def vehicle_delete(id):
    b=db.session.query(Vehicle).get(id)
    db.session.delete(b)
    db.session.commit()
    flash(f'vehicle {id} deleted')
    return redirect('/admin/page')