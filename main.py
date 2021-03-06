from flask import *
from flask_mail import *
from random import *
from PIL import Image,ImageDraw,ImageFont
from datetime import date
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
    database = "webapp"
)
mycursor = mydb.cursor()
app = Flask(__name__)
app.secret_key = 'secret'
mail = Mail(app)
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'mmpkvelammal@gmail.com'
app.config['MAIL_PASSWORD'] = 'mmsap@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)
@app.route('/', methods=['POST','GET'])
def main():
    if request.method=='POST':
        patient = request.form.get('patient')
        doctor = request.form.get('doctor')
        admin = request.form.get('admin')
        if(patient == 'Patient'):
            return redirect(url_for('login_pat'))
        elif (doctor == 'Doctor'):
            return redirect(url_for('login_doc'))
        elif(admin == 'Admin'):
            return redirect(url_for('login_admin'))
    return render_template('mainmainpage.html')
@app.route('/signup_patient',methods=['POST','GET'])
def signup_pat():
    if(request.method == 'POST'):

        name = request.form.get('name')
        uname = request.form.get('username')
        mob = request.form.get('c')
        email = request.form.get('login')
        age = request.form.get('age')
        session['username'] = uname
        send_otp = request.form.get('send_otp')
        submitform = request.form.get('submitform')
        submitotp = request.form.get('submitotp')
        print(name)
        print(uname)
        print(mob)
        print(email)
        print(submitform)
        if(send_otp == "Send Otp"):
            msg = Message('OTP',sender = 'mmpkvelammal@gmail.com', recipients = [email])
            msg.body = name+uname+str(mob)+email+str(otp)
            mail.send(msg)
            return render_template('register_patient.html',name=name,uname=uname,mob=mob,email=email,age=age,visible='none',visible1='block',visible2='none')
        elif(submitotp == "Submit Otp"):
            enter_otp = request.form.get('enterotp')
            print("enter_otp "+enter_otp )
            print("otp ",otp)
            if(int(enter_otp) == otp):
                return render_template('register_patient.html', name=name, uname=uname, mob=mob, email=email,age=age,
                                   visible='none', visible1='none',visible2='block')
        elif(submitform == "Submit"):
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            print(password)
            print(confirm)
            if(password == confirm):
                msg = Message('OTP', sender='mmpkvelammal@gmail.com', recipients=[email])
                msg.body = "Successfully Registered as patient"
                mail.send(msg)
                return redirect(url_for('login_pat'))
        else:
            return redirect(url_for('signup_pat'))
    return render_template('register_patient.html',visible='block',visible1='none',visible2='none')
@app.route('/login_patient',methods=['POST','GET'])
def login_pat():
    if(request.method=='POST'):
        emailme = request.form.get('emailme')
        passwordme = request.form.get('passwordme')
        print(emailme)
        print(passwordme)
        return redirect(url_for('patient_dashboard'))
    return render_template('login_patient.html')
@app.route('/patient_dashboard',methods=['POST','GET'])
def patient_dashboard():
    if(request.method == 'POST'):
        view_doc = request.form.get('view_doc')
        view_rec = request.form.get('view_rec')
        print(view_rec)
        print(view_doc)
        if(view_doc == 'View Doctor'):
            return redirect(url_for('view_doc'))
        elif (view_rec == 'View Records'):
            return redirect(url_for('verify_pat_pass'))
    return render_template('patient_dashboard.html')
@app.route('/verify_patient_password', methods=['POST','GET'])
def verify_pat_pass():
    if (request.method == 'POST'):
        emailme = request.form.get('emailme')
        passwordme = request.form.get('passwordme')
        print(emailme)
        print(passwordme)

        return redirect(url_for('patient_rec'))
    return render_template('verify_by_patient_pass.html')
@app.route('/login_doctors',methods=['POST','GET'])
def login_doc():
    if(request.method=='POST'):
        emailme = request.form.get('emailme')
        passwordme = request.form.get('passwordme')
        print(emailme)
        print(passwordme)
        session['email_doc'] = emailme
        return redirect(url_for('doctor_dashboard'))
    return render_template('login_patient.html')
@app.route('/view_doctors',methods=['POST','GET'])
def view_doc():
    doctors = ['Cristina Groves', 'Marie Wells', 'Henry Daniels', 'Mark Hunter', 'Michael Sullivan', 'Linda Barrett', 'Ronald Jacobs' ]
    specialism = ['Gynecologist', 'Psychiatrist', 'Cardiologist', 'Urologist', 'Ophthalmologist', 'Dentist', 'Oncologist']
    places = []
    img = ['03', '07', '04', '11', '12', '02', '09']
    place = 'United States, San Francisco'
    return render_template('view_doctor.html', doctors = doctors, specialism=specialism, img=img)
@app.route('/view_doctor_profile/<doc>',methods=['POST','GET'])
def view_profile(doc):
    print(doc)
    return render_template('view_doctor_profile.html',doc=doc)
@app.route('/patient_record', methods=['POST','GET'])
def patient_rec():
    if(request.method == 'POST'):
        record = ['Prescription - Dr.Christy @ 3-03-2021', 'Prescription - Dr.Christy @ 4-04-2020',
                  'Prescription - Dr.Christy @ 5-09-2011']
        # img = send_file(url_for('static', filename='images/doctor.png'),mimetype='image')
        logout = request.form.get('logout')
        if(logout == 'logout'):
            return redirect(url_for('main'))
        return send_file('pillow.png',mimetype='image/gif')
    record = ['Prescription - Dr.Christy @ 3-03-2021','Prescription - Dr.Christy @ 4-04-2020','Prescription - Dr.Christy @ 5-09-2011']

    return render_template('patient_records.html',record=record)
@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    if (request.method == 'POST'):
        emailme = request.form.get('emailme')
        passwordme = request.form.get('passwordme')
        print(emailme)
        print(passwordme)
        return redirect(url_for('admin_dashboard'))
    return render_template('login_admin.html')
@app.route('/admin_dashboard',methods=['POST','GET'])
def admin_dashboard():
    doctor = 98
    patients = 1098
    attended = 89
    waiting = 36
    percent = [16, 71, 82, 67, 30]
    dept = ['OPD', 'NEWPATIENTS', 'LABORARTORY', 'TREATMENT', 'DISCHARGE']
    return render_template('admin_dashboard.html',doctor=doctor,patients=patients,attended=attended,waiting=waiting,percent=percent,dept=dept)

@app.route('/doctors_page',methods=['POST','GET'])
def doctor_page():
    doctors = ['Cristina Groves', 'Marie Wells', 'Henry Daniels', 'Mark Hunter', 'Michael Sullivan', 'Linda Barrett', 'Ronald Jacobs' ]
    specialism = ['Gynecologist', 'Psychiatrist', 'Cardiologist', 'Urologist', 'Ophthalmologist', 'Dentist', 'Oncologist']
    places = []
    img = ['03', '07', '04', '11', '12', '02', '09']
    place = 'United States, San Francisco'
    return render_template('doctors_page.html', doctors = doctors, specialism=specialism, img=img)
@app.route('/add_doctor', methods=['POST', 'GET'])
def add_doc():
    if request.method == 'POST':
        first = request.form.get('first')
        last = request.form.get('last')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        country = request.form.get('country')
        city = request.form.get('city')
        state = request.form.get('state')
        code = request.form.get('code')
        phone = request.form.get('phone')
        avatar = request.form.get('avatar')
        bio = request.form.get('bio')
        status = request.form.get('status')
        submit = request.form.get('submit')
        print(first)
        print(last)
        print(username)
        print(email)
        print(password)
        print(confirm)
        print(dob)
        print(gender)
        print(address)
        print(country)
        print(city)
        print(state)
        print(code)
        print(phone)
        print(avatar)
        print(bio)
        print(status)
        print(submit)
        return redirect(url_for('doctor_page'))
    return render_template('add_doctors.html')
@app.route('/patient_page',methods=['POST','GET'])
def patient_page():
    name = ['Jennifer Robinson', 'Terry Baker', 'Kyle Bowman', 'Marie Howard', 'Joshua Guzman']
    age=[35, 65, 7, 22, 34]
    phone = ['(207) 808 8863', '(376) 150 6975', '(981) 756 6128', '(634) 09 3833', '(407) 554 4146']
    email = ['jenniferrobinson@example.com', 'terrybaker@example.com', 'kylebowman@example.com', 'mariehoward@example.com', 'joshuaguzman@example.com']
    return render_template('patients_page.html', name=name,age=age,phone=phone,email=email)
@app.route('/doctor_dashboard',methods=['POST','GET'])
def doctor_dashboard():
    total = 9823
    today = 100
    attended = 89
    waiting = 11
    percent = [16, 71, 82, 67, 35]
    dept = ['OPD', 'NEWPATIENTS', 'LABORARTORY', 'TREATMENT', 'DISCHARGE']
    return render_template('doctor_dashboard.html', total=total, today=today, attended=attended, waiting=waiting,
                           percent=percent, dept=dept)
@app.route('/appointments', methods=['POST','GET'])
def appointments():
    app_id = ['APT001','APT0002']
    pat_name = ['Denise Stevens','Denise Stevens']
    age = [35,70]
    date = ['30 dec 2018','30 dec 2019']
    starttime = ['10.00AM', '11.00AM']
    endtime = ['11.00AM', '12.00PM']
    status =['Attending', 'Waiting']
    color = ['green', 'purple']
    return render_template('doctor_appointments.html', app_id=app_id,pat_name=pat_name,age=age,date=date,starttime=starttime,endtime=endtime,color=color,status=status)
@app.route('/doctor_requests', methods=['POST','GET'])
def requests():
    # if(request.method=='POST'):

    app_id = ['APT001']
    pat_name= ['Denise Stevens']
    age = [35]
    date=['35 dec 2018']

    if request.method == 'POST':
        startdate = request.form.get('start')
        enddate = request.form.get('end')
        print(startdate)
        print(enddate)
        attend = request.form.get('yesorno')
        print(attend)
        submityesorno = request.form.get('submityesorno')
        if(submityesorno == 'submit' and attend == 'YES'):

            return render_template('doctor_requests.html', app_id=app_id, pat_name=pat_name, age=age, date=date,
                                   time1title1='block', submityesorno='none')
    return render_template('doctor_requests.html',app_id=app_id,pat_name=pat_name,age=age,date=date,time1title1 = 'none',submityesorno = 'block')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # print(session['email_doc'])
    # doc_email = session['email_doc']
    doc_email = ''
    doc_name = doc_email
    return render_template('doctor_profile.html',doc_name = doc_name)
otp1 = randint(000000, 999999)
@app.route('/view_by_doctor_OTP', methods=['POST', 'GET'])
def doc_otp():

    if request.method == 'POST':
        emailme = request.form.get('emailme')
        sendotp = request.form.get('sendotp')
        enterotp = request.form.get('enterotp')
        submitme = request.form.get('submitme')
        if(sendotp == 'Send Otp'):

            msg = Message('OTP', sender='mmpkvelammal@gmail.com', recipients=[emailme])
            msg.body = emailme +str(otp1)
            mail.send(msg)
            print(otp1)
            return render_template('view_by_doctor_OTP.html',emailme=emailme,visible='none',visible2='block')
        if (submitme == 'Submit Otp'):
            if(enterotp == str(otp1)):
                print(enterotp)
                return redirect(url_for('documents'))
    return render_template('view_by_doctor_OTP.html',visible='block',visible2='none')
@app.route('/view_by_doctor_password', methods=['POST', 'GET'])
def doc_pass():
    if (request.method == 'POST'):
        emailme = request.form.get('emailme')
        passwordme = request.form.get('passwordme')
        print(emailme)
        print(passwordme)
        return redirect(url_for('documents'))
    return render_template('verify_by_doctor_pass.html')
@app.route('/documents_doctor', methods=['POST', 'GET'])
def documents():
    if (request.method == 'POST'):
        record = ['Prescription - Dr.Christy @ 3-03-2021', 'Prescription - Dr.Christy @ 4-04-2020',
                  'Prescription - Dr.Christy @ 5-09-2011']
        # img = send_file(url_for('static', filename='images/doctor.png'),mimetype='image')
        logout = request.form.get('logout')
        if (logout == 'logout'):
            return redirect(url_for('main'))
        return send_file('pillow.png', mimetype='image/gif')
    record = ['Prescription - Dr.Christy @ 3-03-2021', 'Prescription - Dr.Christy @ 4-04-2020',
              'Prescription - Dr.Christy @ 5-09-2011']


    return render_template('documents_doctor.html',record=record)
@app.route('/prescription', methods=['POST', 'GET'])
def prescription():
    if request.method == 'POST':
        tablet = request.form.get('tablet').split(',')
        morn = request.form.get('morn').split(',')
        date1 = date.today()
        afternoon = request.form.get('afternoon').split(',')
        night = request.form.get('night').split(',')
        duration = request.form.get('duration').split(',')
        beforefood = request.form.get('beforefood').split(',')
        afterfood = request.form.get('afterfood').split(',')
        noted = request.form.get('noted').split(',')
        lengthoftablets = len(tablet)
        labtestname = request.form.get('labtestname').split(',')
        labtestdate = request.form.get('labtestdate').split(',')
        img = Image.new('RGB',(1000,1300),color = 'white')
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        font1 = ImageFont.truetype("arial.ttf", 50)
        d.text((275,43), "Doctor's Details", fill='black', font=font1)
        d.text((535, 185), "Patient's Details", fill='black', font=font1)
        d.text((100, 200), "Date", fill='black', font=font)
        d.text((95, 350), "Tablet Name", fill='black', font=font)
        d.text((290, 350), "M", fill='black', font=font)
        d.text((365, 350), "A", fill='black', font=font)
        d.text((430, 350), "N", fill='black', font=font)
        d.text((490, 350), "Duration", fill='black', font=font)
        d.text((635, 350), "BF", fill='black', font=font)
        d.text((705, 350), "AF", fill='black', font=font)
        d.text((775, 350), "Notes", fill='black', font=font)
        d.text((235, 960), "Lab Test Name", fill='black', font=font)
        d.text((565, 960), "Lab Test Date", fill='black', font=font)
        d.text((110, 250), "date1" , fill='black', font=font)
        y = 410
        for i in range(1,len(tablet)):
            d.text((95,y),tablet[i],fill='black',font=font)
            d.text((290, y), morn[i], fill='black', font=font)
            d.text((365, y), afternoon[i], fill='black', font=font)
            d.text((430, y), night[i], fill='black', font=font)
            d.text((490, y), duration[i], fill='black', font=font)
            d.text((635, y), beforefood[i], fill='black', font=font)
            d.text((705, y), afterfood[i], fill='black', font=font)
            d.text((775, y), noted[i], fill='black', font=font)
            y+=70
        y = 1030
        for i in range(1,len(labtestname)):
            d.text((235, y), labtestname[i], fill='black', font=font)
            d.text((565, y), labtestname[i], fill='black', font=font)
            y+=70
        img.save('pillow.png')





        print(tablet)
        print(morn)
        print(afternoon)
        print(night)
        print(duration)
        print(beforefood)
        print(afterfood)
        print(noted)
        print(labtestname)
        print(labtestdate)
    return render_template('prescription.html')

# @app.route('/validate',methods=["POST"])
# def validate():
#     user_otp = request.form['otp']
#     if otp == int(user_otp):
#         email = "m.muniprasanna@gmail.com"
#         msg = Message('Successfully Logged in', sender='mmpkvelammal@gmail.com', recipients=[email])
#         msg.body = "successfully logged in go on muni"
#         mail.send(msg)
#         return "<h3> Email  verification is  successful </h3>"
#     return "<h3>failure, OTP does not match</h3>"
if __name__ == '__main__':
    app.run(debug = True)