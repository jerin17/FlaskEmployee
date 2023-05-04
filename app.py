from flask import Flask, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
import start_up
import os 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.String(20))

    def __init__(self, name, department, salary, hire_date):
        self.name = name
        self.department = department
        self.salary = salary
        self.hire_date = hire_date

def get_employee_details(id):
    employee = Employee.query.filter_by(id=id).first()
    employee_data = {}
    employee_data['id'] = employee.id
    employee_data['name'] = employee.name
    employee_data['department'] = employee.department
    employee_data['salary'] = employee.salary
    employee_data['hire_date'] = employee.hire_date
    return employee_data

@app.route('/', methods=['GET'])
def employee():
    employee_data = Employee.query.all()
    return render_template('employee.html', employee_data=employee_data, heading="Employee")

# viewing Employee Details
@app.route('/employees/<int:id>',  methods=['GET'])
def get_employee(id):
    employee_data = get_employee_details(id)
    return render_template('viewEmployee.html', employee_data=employee_data)

# Adding Employee GET AND POST METHOD
@app.route('/addEmployee', methods=['GET'])
def create_employee():
    return render_template('addEmployee.html')

@app.route('/addEmployee', methods=['POST'])
def insert_employee():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']
        hire_date = request.form['hire_date']

        data = Employee(name, department, salary, hire_date)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('employee'))

# Updating Employee GET AND POST METHOD
@app.route('/updateEmployee/<int:id>', methods=['GET'])
def update_employee(id):
    employee_data = get_employee_details(id)
    return render_template('updateEmployee.html', employee_data=employee_data)

@app.route('/updateEmployee', methods=['POST'])
def insert_update_employee():
    id = request.form['id']

    employee = Employee.query.filter_by(id=id).first()
    if not employee:
        return jsonify({'error': 'Employee not found'})
    name = request.form['name']
    department = request.form['department']
    salary = request.form['salary']
    hire_date = request.form['hire_date']
    
    employee.name = name
    employee.department = department
    employee.salary = salary
    employee.hire_date = hire_date
    db.session.commit()
    return redirect(url_for('employee'))

# Deleting Employee
@app.route('/deleteEmployee/<int:id>', methods=['GET'])
def delete_employee(id):
    employee = Employee.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employee'))

# Viewing Department details
@app.route('/department', methods=['GET'])
def department():
    department_data = Employee.query.with_entities(Employee.department).distinct()
    return render_template('department.html', department_data = department_data)

@app.route('/department/<string:department>', methods=['GET'])
def view_department_employees(department):
    employee_data = Employee.query.filter_by(department=department)
    return render_template('departmentEmployees.html', employee_data=employee_data, department=department)

# Viewing Top earner in comapny
@app.route('/top_earner', methods=['GET'])
def top_earner():
    employee_data = Employee.query.order_by(Employee.salary.desc()).limit(5).all()
    return render_template('employee.html', employee_data=employee_data, heading="Top Earner")

# Viewing Recent hires in comapny
@app.route('/recent_hires', methods=['GET'])
def recent_hires():
    employee_data = Employee.query.order_by(Employee.hire_date.desc()).limit(5).all()
    return render_template('employee.html', employee_data=employee_data, heading="Recent Hires")

if __name__ == '__main__':
    start_up.initialize()
    app.run(debug=True)
