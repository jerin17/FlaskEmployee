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
TOP_EMPS = 10

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

def calculate_avg():
    return 0

@app.route('/', methods=['GET'])
def employee():
    employee_data = {}
    try:
        employee_data = Employee.query.all()
    except Exception as e:
        print(F"Exception while fetching employees : {str(e)}")
    return render_template('employee.html', employee_data=employee_data, heading="Employee")

# viewing Employee Details
@app.route('/employees/<int:id>',  methods=['GET'])
def get_employee(id):
    try:
        employee_data = get_employee_details(id)
        return render_template('viewEmployee.html', employee_data=employee_data)
    except Exception as e:
        return render_template("404.html")


# Adding Employee GET AND POST METHOD
@app.route('/addEmployee', methods=['GET'])
def create_employee():
    return render_template('addEmployee.html', employee_data = {}, errors={})
    

@app.route('/addEmployee', methods=['POST'])
def insert_employee():
    if request.method == 'POST':
        errors = []
        if 'name' in request.form and request.form['name']:
            name = request.form['name']
        else:
            errors.append("Name cannot be blank")

        if 'department' in request.form and request.form['department']:
            department = request.form['department']
        else:
            errors.append("Department cannot be blank")

        if 'salary' in request.form and request.form['salary']:
            salary = request.form['salary']
        else:
            errors.append("Salary cannot be blank")

        if 'hire_date' in request.form and request.form['hire_date']:
            hire_date = request.form['hire_date']
        else:
            errors.append("Hire date cannot be blank")

        if errors == []:
            data = Employee(name, department, salary, hire_date)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('employee'))

        else:
            return render_template('addEmployee.html', employee_data = request.form, errors= errors)

# Updating Employee GET AND POST METHOD
@app.route('/updateEmployee/<int:id>', methods=['GET'])
def update_employee(id):
    try:
        employee_data = get_employee_details(id)
        return render_template('updateEmployee.html', employee_data=employee_data, errors={})
    except Exception as e:
        return render_template("404.html")

@app.route('/updateEmployee', methods=['POST'])
def insert_update_employee():
    print(f"\n\n\n{request.method = }")
    errors = []
    if 'id' in request.form and request.form['id']:
        id = request.form['id']
    
    if 'name' in request.form and request.form['name']:
        name = request.form['name']
    else:
        errors.append("Name cannot be blank")

    if 'department' in request.form and request.form['department']:
        department = request.form['department']
    else:
        errors.append("Department cannot be blank")

    if 'salary' in request.form and request.form['salary']:
        salary = request.form['salary']
    else:
        errors.append("Salary cannot be blank")

    if 'hire_date' in request.form and request.form['hire_date']:
        hire_date = request.form['hire_date']
    else:
        errors.append("Hire date cannot be blank")

    print(f"{errors = }")

    if errors == []:
        employee = Employee.query.filter_by(id=id).first()

        employee.name = name
        employee.department = department
        employee.salary = salary
        employee.hire_date = hire_date
        db.session.commit()
        return redirect(url_for('employee'))

    else:
        return render_template('updateEmployee.html', employee_data = request.form, errors= errors)

# Deleting Employee
@app.route('/deleteEmployee/<int:id>', methods=['GET'])
def delete_employee(id):
    try:
        employee = Employee.query.filter_by(id=id).first()
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('employee'))
    except Exception as e:
        return render_template("404.html")
    
@app.route('/department', methods=['GET'])
def department():
    department_data = {}
    try:
        department_data = Employee.query.with_entities(Employee.department).distinct()
    except Exception as e:
        print(F"Exception while fetching department : {str(e)}")
        department_data = {}
    return render_template('department.html', department_data=department_data)

@app.route('/department/<string:department>', methods=['GET'])
def view_department_employees(department):
    try:
        employee_data = Employee.query.filter_by(department=department)
        return render_template('departmentEmployees.html', employee_data=employee_data, department=department)
    except Exception as e:
        return render_template("404.html")

# Viewing Top earner in company
@app.route('/top_earner', methods=['GET'])
def top_earner():
    employee_data = {}
    try:
        employee_data = Employee.query.order_by(Employee.salary.desc()).limit(TOP_EMPS).all()
    except Exception as e:
        print(F"Exception while fetching employees : {str(e)}")
    return render_template('employee.html', employee_data=employee_data, heading=f"Top {TOP_EMPS} Earner")

# Viewing Recent hires in company
@app.route('/recent_hires', methods=['GET'])
def recent_hires():
    employee_data = {}
    try:
        employee_data = Employee.query.order_by(Employee.hire_date.desc()).limit(TOP_EMPS).all()
    except Exception as e:
        print(F"Exception while fetching employees : {str(e)}")
    return render_template('employee.html', employee_data=employee_data, heading=f"Recent {TOP_EMPS} Hires")

# Viewing Average salaries in the department
@app.route('/average_salaries/<string:department>', methods=['GET'])
def get_average_salaries(department):
    employees = Employee.query.filter_by(department=department).all()
    if not employees:
        return jsonify({'message': 'No employees found in this department.'}), 404
    salaries = [employee.salary for employee in employees]
    avg_salary = sum(salaries) / len(salaries)

    data = {}
    data['department'] = department
    data['salary'] = avg_salary
    return render_template('departmentAverageSalary.html', data=data, heading="Average Salary")

# Error handling 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    start_up.initialize()
    app.run(debug=True)
