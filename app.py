from flask import Flask,render_template,request,redirect,url_for
import pymysql
db_connection = None
tb_cursor = None


app = Flask(__name__)

@app.route("/")
def index():
    empsdata=getallemp()
    return render_template("index.html",data=empsdata)

@app.route("/add/",methods=["GET","POST"])
def addemp():
    if request.method =="POST":
        data = request.form
        isInserted = insertIntoTable(data['txtName'],data['txtAddr'],data['txtPhone'],data['txtBd'],data['txtDep'],data['txtSal'])
        if(isInserted):
            message="Done"
            return redirect(url_for("index"))
        else:
            message="Failed"
            return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updateEmp():
    id = request.args.get("ID",type=int,default=1)
    idData = getEmpid(id)
    if request.method == "POST":
        data = request.form
        print(data)
        isUpdated = updateEmpIntoTable(data['txtName'],data['txtAddr'],data['txtPhone'],data['txtBd'],data['txtDep'],data['txtSal'],id)
        if(isUpdated):
            message = "Updattion sucess"
            return redirect(url_for("index"))
        else:
            message = "Updattion Error"
            return redirect(url_for("index"))
    return render_template("update.html",data=idData)

@app.route("/delete/")
def delemp():
    id = request.args.get("ID",type=int,default=1)
    deleteempFromTable(id)
    return redirect(url_for("index"))

def dbconnect():
    global db_connection,tb_cursor
    db_connection = pymysql.connect(host="localhost",user="root",passwd="",database="ems",port=3306)
    if(db_connection):
        print("connected")
        tb_cursor=db_connection.cursor()
    else:
        print("failed")
 
def dbDisconnect():
    db_connection.close()
    tb_cursor.close()

def getallemp():
    dbconnect()
    getQuerry = "select * from emp"
    tb_cursor.execute(getQuerry)
    empsdata = tb_cursor.fetchall()
    print(empsdata)
    dbDisconnect()
    return empsdata

def getEmpid(emp_id):
    dbconnect()
    selectQuery = "SELECT * FROM emp WHERE id=%s;"
    tb_cursor.execute(selectQuery,(emp_id))
    oneData = tb_cursor.fetchone()
    dbDisconnect()
    return oneData



def insertIntoTable(name,addr,phone,bd,dep,sal):
    dbconnect()
    insert_query="insert into emp(name,addr,phone,birth,dep,sal) values (%s,%s,%s,%s,%s,%s);"
    tb_cursor.execute(insert_query,(name,addr,phone,bd,dep,sal))
    db_connection.commit()
    dbDisconnect()
    return True

def updateEmpIntoTable(name,addr,phone,bd,dep,sal,id):
    dbconnect()
    updateQuery = "UPDATE emp SET name=%s,addr=%s,phone=%s,birth=%s,dep=%s,sal=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(name,addr,phone,bd,dep,sal,id))
    db_connection.commit()
    dbDisconnect()
    return True

def deleteempFromTable(id):
    dbconnect()
    deleteQuery = "DELETE FROM emp WHERE id=%s;"
    tb_cursor.execute(deleteQuery,(id))
    db_connection.commit()
    dbDisconnect()
    return True



if(__name__)=='__main__':
    app.run(debug=True)