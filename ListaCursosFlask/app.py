from flask import Flask, render_template, request,  redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'senabd'

app.secret_key = 'mysecretkey'
mysql=MySQL(app)

@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM curso')
    data = cur.fetchall()
    return render_template('index.html', cursos=data)
    

@app.route('/add_cursos', methods=['GET','POST'])
def add_cursos():
    if request.method == "POST":
        codigo=request.form['codigo']
        nombre=request.form['nombre']
        horas=request.form['horas']
        area=request.form['area']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO curso (codigo,nombre,horas,area) VALUES(%s, %s, %s, %s)',(codigo,nombre,horas,area)) 
        mysql.connection.commit()
        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/edit/<id>')
def get_curso(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM curso WHERE id = %s',(id))
    data = cur.fetchall() # retorna un unico valor
    return render_template('edit_curso.html', c = data[0]) #lleva a edit_curso el registro 
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update_curso(id):
    
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        horas = request.form['horas']
        area = request.form['area']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE curso SET codigo = %s, nombre = %s, horas = %s, area = %s WHERE id = %s' ,(codigo,nombre,horas,area,id))
        mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM curso WHERE ID ={0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('index'))

def pagina_no_encontrada(error):
    #return render_template('404.html'),404
    return redirect(url_for('index'))

if __name__=='__main__':
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True)
