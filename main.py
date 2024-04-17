from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Double
from datetime import datetime

# SQLAlchemy setup
Base = declarative_base()

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    size = Column(Double(precision=2))
    path = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

# Utility functions
def get_db_session():
    engine = create_engine('sqlite:///CQUK.db')
    Session = sessionmaker(bind=engine)
    return Session()

def save_to_db(obj):
    session = get_db_session()
    session.add(obj)
    session.commit()
    session.close()

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        path = "static/uploads/"
        file.save(path+filename)  # Save the file
        upload_obj = Upload(size=file.content_length, path="/"+path+filename)
        save_to_db(upload_obj)  # Save upload info to the database
        return redirect(url_for('upload_success'))

@app.route('/upload_success')
def upload_success():
    db = get_db_session()
    uploads = db.query(Upload).all()
    return render_template('upload.html', uploads=uploads)

@app.route('/quantize/<int:id>', methods=['GET', 'POST'])
def quantize(id):
    return redirect("/quantize/success")

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def quantize(id):
    pass

@app.route('/download/<int:id>', methods=['GET', 'POST'])
def quantize(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
