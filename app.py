from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Job {self.company} - {self.role}>' 
       




@app.route('/')
def home():
    
    all_jobs=Job.query.all()
    return render_template('index.html', jobs=all_jobs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        company = request.form['company']
        role = request.form['role']
        date_str = request.form['date']
        status = request.form['status']
        if date_str:
            date_applied = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        else:
            date_applied = datetime.now(timezone.utc)

        new_job = Job(company=company, role=role, date_applied=date_applied, status=status)
        db.session.add(new_job)
        db.session.commit()
        return redirect('/')
    
    return render_template('add.html')
    
@app.route('/delete/<int:id>')
def delete(id):
    job=Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    job=Job.query.get_or_404(id)
    if request.method == "POST":
        
        job.company = request.form['company']
        job.role = request.form['role']
        date_str = request.form['date']
        if date_str:
            job.date_applied = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        else:
            job.date_applied = datetime.now(timezone.utc)
        job.status = request.form['status']
        db.session.commit()
        return redirect('/')
    
    return render_template('edit.html', job_to_edit=job)



if __name__  == '__main__':
    app.run(debug=True)