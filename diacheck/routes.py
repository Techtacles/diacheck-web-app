from flask import render_template, url_for, flash, redirect, request
from diacheck import app, db, bcrypt
from diacheck.forms import RegistrationForm, LoginForm
from diacheck.models import Prediction, User
from flask_login import login_user, current_user, logout_user, login_required
import random
import pickle
model=pickle.load(open('model.pkl','rb'))

@app.route("/") 
def home():
    return render_template('index.html')

@app.route("/about") 
def about():
    return render_template('about.html')
     

@app.route("/register", methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            email = request.form['email'],
            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember='yes')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    else:
        return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    print(Prediction.query.all())
    return render_template('dashboard.html', title='Dashboard')

@app.route("/read", methods=['GET', 'POST'])
@login_required
def read():
    return render_template('read.html', title='Dashboard')


@app.route("/results", methods=['GET', 'POST'])
@login_required
def results():
    #test_number is used to store the current user id, so we could restrict results to a user
    results = Prediction.query.filter_by(test_number = current_user.id).all()
    #Prediction takes in username(current_user.username) , result= prediction model returns 
    return render_template('results.html', title='Results', result = results)

@app.route("/blogs", methods=['GET', 'POST'])
@login_required
def blogs():
    return render_template('blogs.html', title='Blogs')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/predict',methods=['POST'])
def predict():
    highbp=int(request.form['highbp'])
    highcholesterol= int(request.form['highcholesterol'])
    age= int(request.form['age'])
    smoker= int(request.form['smoker'])
    sex= int(request.form['sex'])
    bmi= int(request.form['bmi'])
    fruits= int(request.form['fruits'])
    alcohol= int(request.form['alcohol'])
    physical= int(request.form['physical'])
    hdoa= int(request.form['hdoa'])
    #model=pickle.load(open(r'C:\Users\team\Desktop\DIACHECK\model.pkl','rb'))
    pred=model.predict([[highbp,highcholesterol,smoker,age,sex,bmi,fruits,alcohol,hdoa,physical]])[0]
    to_cmt=Prediction(test_number=current_user.id,result=['diabetis' if pred==1 else 'non diabetis'][0])
    db.session.add(to_cmt)
    db.session.commit()

    if pred==0:
        new_pred='non diabetes'
        return render_template('response.html',prediction_text=f'You do not have diabetes.',pred_value=pred)

    if pred==1:
        new_pred='diabetes'
        return render_template('response.html',prediction_text=f'You are diabetes positive!! Visit a nearby hospital for necessary healthcare.',pred_value=pred)
    
    return render_template('dashboard.html')


if __name__ == '__main__':
   app.run(debug=False)