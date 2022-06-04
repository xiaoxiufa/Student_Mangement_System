from flask import *
import pymysql
app = Flask(__name__,
            static_url_path='/static', # 静态文件路径
            static_folder='static',
            template_folder='templates' #模板文件
            )
def conn_DB():
    global sql
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="student", charset="utf8")
    cursor = conn.cursor()
    sql = 'select username,password from student'
    cursor.execute(sql)
    list_data=[]
    data=cursor.fetchall()
    for i in data:
        dic={'用户名':i[0], '密码':i[1]}
        list_data.append(dic)

    conn.commit()
    cursor.close()
    conn.close()
    return list_data
def connt_DB1():
    global SQL
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="student", charset="utf8")
    cursor = conn.cursor()
    SQL = 'select * from student_sore'
    cursor.execute(SQL)
    list_data = []
    data = cursor.fetchall()
    for i in data:
        dic = {'name': i[1], 'chinese': i[2], 'math':i[3], 'English':i[4]}
        list_data.append(dic)

    conn.commit()
    cursor.close()
    conn.close()
    return list_data
def add_data():
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="student", charset="utf8")
    cursor = conn.cursor()

    sql = "INSERT INTO `student_sore` (`ID`, `username`, `语文`, `数学`, `英语`) VALUES (NULL, '%s','%s', '%s' , '%s');"%(name, chinese, math, english)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    pass
def delete_data():
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="student", charset="utf8")
    cursor = conn.cursor()

    sql = "DELETE FROM student_sore where username='%s';"%(d_name)

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    pass
def change_data():
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="student", charset="utf8")
    cursor = conn.cursor()

    sql = "UPDATE student_sore SET `语文`='%s', `数学`='%s', `英语`='%s' WHERE username='%s'"%(change_chinese, change_math, change_english, change_name)

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    pass
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method =='POST':
        name = request.form.get('name')
        passwd = request.form.get('passwd')
        data = conn_DB()
        for temp in data:
            print(temp['用户名'], temp['密码'])
            if temp['用户名'] == name and temp['密码']==passwd:
                return redirect('/admin')
    return render_template('login.html')
@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('register.html')

@app.route('/admin')
def admin():
    student_data=connt_DB1()
    print(student_data)
    return render_template('admin.html', students=student_data, ensure_ascii=False)

@app.route('/add', methods=['POST', 'GET'])
def add():
    global name
    global chinese
    global math
    global english
    if request.method == "POST":
        name=request.form.get('name')
        chinese = request.form.get('chinese')
        math= request.form.get('math')
        english= request.form.get('english')
        int(chinese)
        int(math)
        int(english)
        print(name, chinese,math,english)
        add_data()
        return redirect('/add')
    return render_template('add.html')


@app.route('/change', methods=['POST', 'GET'])
def change():
    global change_name
    global change_chinese
    global change_math
    global change_english
    change_name=request.args.get('name')
    print(change_name)
    if request.method == 'POST':
        change_chinese=request.form.get('chinese')
        change_math = request.form.get('math')
        change_english = request.form.get('english')
        try:
            change_data()
        except:
            return redirect('/admin')
        return redirect('/admin')
    return render_template('change.html', name=change_name)

@app.route('/delete', methods=['POST','GET'])
def delete():
    global d_name
    d_name=request.args.get('name')
    delete_data()
    return redirect('/admin')
if __name__ == '__main__':
    app.run()

