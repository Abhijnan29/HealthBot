from datetime import timedelta
from flask import Flask, render_template, request, redirect, jsonify,url_for, session
import mysql.connector
import openai
#from passlib.hash import sha256_crypt
app = Flask(__name__)

app.secret_key ='bdc556f280795c3fbeeceec6c1371403e130cfef785cbd02ba648f3a10ff3c75'

# Set up OpenAI API credentials
openai.api_key = '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'

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin",
    database="hospitallogin"
)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods =['GET', 'POST'])
def log():
    msg2=''
    if request.method == 'POST' and 'login-email' in request.form and 'login-password' in request.form:
        email = request.form['login-email']
        password = request.form['login-password']
        
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT email,password FROM reg WHERE email = %s AND password = %s', (email, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
           # session['id'] = account['id']
            session['email'] = account['email']
            session['password'] = account['password']
            msg2= 'Logged in Successfully'
            #return 'Logged in successfully !'
            return render_template('home.html',msg2=msg2)
        else:
            msg2 = 'Incorrect username / password !'
            #return 'Incorrect username / password !'
            return render_template('login.html', msg2=msg2)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('login'))

@app.route('/register')
def Registration():
    return render_template('Registration.html')

@app.route('/register', methods= ['GET' , 'POST'])
def submit():
    msg = ''
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phonenumber=request.form['phonenumber']
    address=request.form['address']
    password=request.form['password']
    #encpassword=sha256_crypt.hash(password)

    # Insert data into the database
    cursor = db.cursor()
    query = "INSERT INTO reg (firstname,lastname,email,phonenumber,address,password) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (firstname,lastname,email,phonenumber,address,password)
    cursor.execute(query, values)
    db.commit()

    # Optionally, you can close the database connection after the insertion
    cursor.close()
    db.close()
   
    msg= 'Data inserted Successfully'
    #return "Data inserted Successfully"
    return render_template('login.html', msg=msg)

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/contact')

def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
   return render_template('about.html')



#@app.route('/contact', methods= ['GET' , 'POST'])
#def submit():
#    name  = request.form['name'] 
#    email = request.form['email']
#    phonenumber=request.form['phonenumber']
#    desc=request.form['desc']

    # Insert data into the database
#    cursor = db.cursor()
#    query = "INSERT INTO reg (name,email,phonenumber,desc) VALUES (%s, %s, %s, %s)"
#    values = (name,email,phonenumber,desc)
#    cursor.execute(query, values)
#    db.commit()

    # Optionally, you can close the database connection after the insertion
#    cursor.close()
#    db.close()
   
    #return "Data inserted Successfully"
#    return render_template('Data_submit.html')

#



@app.route('/forget')
def forget():
   return render_template('forget_password.html');




# Define the default route to return the index.html file
@app.route("/chat")
def chat():
    return render_template("chatbot.html")

# Define the /api route to handle POST requests
#@app.route("/api", methods=["POST"])
#def api():
    # Get the message from the POST request
#    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    
#    completion = openai.ChatCompletion.create(
#    model="gpt-3.5-turbo",
#    messages=[
#        {"role": "user", "content": "\n\nHi,How may I help you today ?"}
#    ]
#    )
#    if completion.choices[0].message!=None:
#        return completion.choices[0].message

#    else :
#        return 'Failed to Generate response!'

 
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False,host='0.0.0.0')
    
session.permanent = True
app.permanent_session_lifetime = timedelta(seconds=3)
session.modified = True
  
