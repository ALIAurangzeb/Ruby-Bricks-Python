from cmath import pi
from email.mime import image
from flask import Flask,render_template,request,jsonify
import json
import sqlite3 as sql
import os

app = Flask(__name__)

#Routes
#-----------Start--------------

@app.route('/')
def home():
    setLimit = 6
    GetPropertyRecordsQuery = "select * from Property order by Id Desc Limit %d"%setLimit
    with sql.connect("RubyBricks.db") as con:
            cur = con.cursor()
            cur.execute(GetPropertyRecordsQuery)
            GetAllProperty = cur.fetchall()
    return render_template('index.html', GetAllProperty = GetAllProperty)

@app.route('/AdminPanel')
def AdminPanel():
    #Fetching all records from Database
    GetPropertyRecordsQuery = "select * from Property order by Id Desc"
    with sql.connect("RubyBricks.db") as con:
            cur = con.cursor()
            cur.execute(GetPropertyRecordsQuery)
            GetAllProperty = cur.fetchall()            
          
            return render_template('admin_panel.html',GetAllProperty = GetAllProperty)           
            

@app.route('/Create',methods=['GET','POST'])
def Create():
    if request.method == 'GET':
        return render_template('Create.html')
    
    #else
    Ar = request.form['Ar']
    Bd = request.form['Bd']
    Br = request.form['Br']
    Des = request.form['Des']
    Fur = request.form['Fur']
    Pc = request.form['Pc']
    Gar = request.form['Gar']
    St = request.form['St']
    Pt = request.form['Pt']
    Yb = request.form['Yb']
    Pf = request.form['Pf']
    Pl = request.form['Pl']
    Hn = request.form['Hn']
    pic = request.files['picture']

    #getting imagename type and creating a valid path/location
    #These comments are temporary remember e.g imagename imagepath will change later once records inserted
    if not pic:
        return jsonify("Please Select Image")  

    Imagename =  pic.filename
    Image =      pic.read()
    ImagePath =  "static/images/"+Imagename
    
    #This method will check if the path/Image already exist in folder, if it is exist then it will not let you upload the picture
    if os.path.exists(ImagePath):
        return jsonify("Image already exist")
       

    #Writing Image in bytes
    f = open(ImagePath,'wb')
    f.write(Image)
    f.close()

    #Sql query for inserting records with Images
    with sql.connect("RubyBricks.db") as con:
        cur = con.cursor()
        cur.execute("Insert into Property (Area,Bedrooms,Bathrooms,Garage,Stories,YearBuild,PropertyFor,Description,Furnished,PostCode,PropertyType,ImagePath,ImageName,Place,HouseName) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Ar,Bd,Br,Gar,St,Yb,Pf,Des,Fur,Pc,Pt,ImagePath,Imagename,Pl,Hn))
    
    return jsonify("Records inserted Successfully!!")
    

@app.route('/about')
def About():
    return render_template('about.html')


@app.route('/contact')
def Contact():
    return render_template('contact.html')


@app.route('/services')
def Services():
    return render_template('services.html')


@app.route('/properties')
def Properties():    
    # GetPropertyRecordsQuery = "select * from Property order by Id Desc"
    GetPropertyBySearch = None
    setLimit = 6
    GetPropertyRecordsQuery = "select * from Property order by Id Desc Limit %d"%setLimit
    with sql.connect("RubyBricks.db") as con:
            cur = con.cursor()
            cur.execute(GetPropertyRecordsQuery)
            GetAllProperty = cur.fetchall()

    return render_template('properties.html',GetAllProperty = GetAllProperty, GetPropertyBySearch = GetPropertyBySearch)


@app.route('/properties-single/<int:id>')
def PropertiesSingle(id):
    PropertyId = id
    #Getting record by Id
    GetSinglePropertyRecord = "select * from Property where Id = %d"%PropertyId
    with sql.connect("RubyBricks.db") as con:
            cur = con.cursor()
            cur.execute(GetSinglePropertyRecord)
            GetProperty = cur.fetchone()
            ImagePath = GetProperty[13]
                           
    return render_template('properties-single.html',GetProperty = GetProperty,ImagePath = ImagePath)

@app.route('/SearchProperties',methods=['POST'])
def SearchProperties():
    if request.method == "POST":
        Pf = request.form['Pf'] 
    Pt = request.form['Pt']    
    Loc = request.form['Loc'] 
    GetAllProperty = None
    Flag = []

    search1 = "Fl"
    search2 = "Faisl"
    search3 = "Sa"
    
    print(Pf + " " + Pt + " " + " " + Loc )

    
    with sql.connect("RubyBricks.db") as con:
        cur = con.cursor()
    # cur.execute("select * from Property where Place Like ? ",('%'+search+'%',))
    cur.execute("select * from Property where PropertyType Like ? And Place Like ? And PropertyFor Like ? ",('%'+Pt+'%', '%'+Loc+'%','%'+Pf+'%'))
    # GetPropertyBySearch = cur.fetchall()
    # print(GetPropertyBySearch)
    # query = "Select * from Property where PropertyType = %s OR Place = %s OR PropertyFor = %s"%search1[0] %search2[1] %search3[2]
    # query = "Select * from Property where PropertyType = %s OR Place = %s OR PropertyFor = %s",(search1,search2,search3)
    # cur.execute("Select * from Property where PropertyType = ? And Place = ? And PropertyFor = ?",(search1,search2,search3))
    GetPropertyBySearch = cur.fetchall()
    if GetPropertyBySearch == []:
        return render_template('properties.html',GetPropertyBySearch = GetPropertyBySearch , GetAllProperty = GetAllProperty,Flag = Flag)

    #print(GetPropertyBySearch)
    return render_template('properties.html',GetPropertyBySearch = GetPropertyBySearch , GetAllProperty = GetAllProperty)
           

#-----------End--------------

#This method is for the ContactForm, user can easily contact with admins.
@app.route('/addContact',methods=['POST','GET'])
def AddContactRecords():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            em = request.form['em']
            Sub = request.form['sub']
            Message = request.form['msg']

            with sql.connect("RubyBricks.db") as con:
                cur = con.cursor()
                cur.execute("Insert into Contact (Name,Email,Subject,Message) values (?,?,?,?)",(nm,em,Sub,Message))
                messages = "Data inserted successfully"

        except:
            con.rollback()
            messages = "Data not inserted"
        
        finally:
            # return render_template('result.html',messages=messages)
            return jsonify(messages)
            con.close()



if __name__ == '__main__':
    app.run(debug=True)