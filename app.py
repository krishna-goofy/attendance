from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(150), nullable=False)
class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    student_names = db.Column(db.String(1000))  # Ensure this matches your form

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
    day = db.Column(db.String(50), nullable=False)
    timeslot = db.Column(db.String(50), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))  # Link to batch

    folder = db.relationship('Folder', backref=db.backref('timetables', lazy=True))
    batch = db.relationship('Batch', backref=db.backref('timetables', lazy=True))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    period = db.Column(db.String(100), nullable=False)
    coming_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    going_out_time = db.Column(db.DateTime, nullable=True)

    batch = db.relationship('Batch', backref=db.backref('attendances', lazy=True))
    folder = db.relationship('Folder', backref=db.backref('attendances', lazy=True))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_folder', methods=['POST'])
def save_folder():
    data = request.json
    folder_name = data.get('folderName')
    days = data.get('days')
    timeslots = data.get('timeslots')
    table_data = data.get('tableData')

    if folder_name and days and timeslots and table_data:
        # Save the folder name
        folder = Folder(folder_name=folder_name)
        db.session.add(folder)
        db.session.commit()

        # Save the timetable data
        for day in days:
            for timeslot in timeslots:
                period_key = f"{day}_{timeslot}"
                period_data = table_data.get(period_key)
                
                # Debugging information
                print(f"Period Key: {period_key}")
                print(f"Period Data: {period_data}")
                print(f"Type of Period Data: {type(period_data)}")

                try:
                    # Attempt to convert period_data to an integer
                    batch_id = int(period_data)
                except ValueError:
                    print(f"Error: period_data is not convertible to an integer for key {period_key}")
                    batch_id = None  # Handle this case as needed

                new_timetable = Timetable(
                    folder_id=folder.id,
                    day=day,
                    timeslot=timeslot,
                    batch_id=batch_id
                )
                db.session.add(new_timetable)

        db.session.commit()
        return jsonify({'message': 'Folder and timetable saved successfully!'}), 201

    return jsonify({'message': 'Failed to save folder and timetable'}), 400




@app.route('/view_tables')
def view_tables():
    folders = Folder.query.all()
    return render_template('view_tables.html', folders=folders)


@app.route('/get_table_data/<int:folder_id>', methods=['GET'])
def get_table_data(folder_id):
    timetables = Timetable.query.filter_by(folder_id=folder_id).all()
    
    # Define the order of the days of the week
    day_order = {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7
    }
    
    # Sort timetables by day using the defined order and then by timeslot
    sorted_timetables = sorted(timetables, key=lambda x: (day_order.get(x.day, 8), x.timeslot))
    # Create a list of tuples for sorted data
    data = [(timetable.day, timetable.timeslot, timetable.batch_id) for timetable in sorted_timetables]
    return jsonify(data)







"""@app.route('/get_table_data/<int:folder_id>', methods=['GET'])
def get_table_data(folder_id):
    timetables = Timetable.query.filter_by(folder_id=folder_id).all()
    data = {}
    for timetable in timetables:
        key = f"{timetable.day}_{timetable.timeslot}"
        data[key] = timetable.batch_id
    return jsonify(data)"""

@app.route('/create_batch', methods=['GET', 'POST'])
def create_batch():
    if request.method == 'POST':
        print("Received POST request at /create_batch")
        print("Form Data:", request.form)
        try:
            batch_name = request.form['batch_name']
            student_names = request.form['student_names']
            new_batch = Batch(name=batch_name, student_names=student_names)
            db.session.add(new_batch)
            db.session.commit()
            return redirect(url_for('view_batches'))
        except KeyError as e:
            return f"Missing form field: {e}", 400
    else:  # GET request
        return render_template('create_batch.html')

@app.route('/get_batches')
def get_batches():
    batches = Batch.query.all()
    return jsonify([{'id': batch.id, 'name': batch.name} for batch in batches])

@app.route('/view_batches')
def view_batches():
    batches = Batch.query.all()
    return render_template('view_batches.html', batches=batches)

from datetime import datetime

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':

        class_id = request.form['class_id']
        student_name = request.form['student_name']

        now = datetime.now()
        current_day = now.strftime('%A')
        current_time = now.strftime('%H:%M')

        timetables = Timetable.query.filter_by(folder_id=class_id).all()
        
        current_period = None
        for timetable in timetables:
            if timetable.day == current_day:
                start_time, end_time = timetable.timeslot.split('-')
                if start_time <= current_time <= end_time:
                    current_period = timetable
                    break

        if current_period:
            batch = Batch.query.get(current_period.batch_id)
            if batch and student_name in batch.student_names.split(','):
                # Check if there's an ongoing attendance without a going_out_time
                existing_attendance = Attendance.query.filter_by(
                    student_name=student_name,
                    batch_id=current_period.batch_id,
                    date=now.date(),
                    period=f"{current_period.day} {current_period.timeslot}",
                    going_out_time=None
                ).first()

                if existing_attendance:
                    # Student is leaving, update the going_out_time
                    existing_attendance.going_out_time = now
                    db.session.commit()
                    return jsonify({'message': 'Going out time recorded successfully!'}), 200
                else:
                    # Check if the period has ended and no going out time was recorded
                    end_time_datetime = datetime.strptime(f"{now.date()} {end_time}", '%Y-%m-%d %H:%M')
                    if now > end_time_datetime:
                        # Automatically set the going out time as the period end time
                        attendance_record = Attendance.query.filter_by(
                            student_name=student_name,
                            batch_id=current_period.batch_id,
                            date=now.date(),
                            period=f"{current_period.day} {current_period.timeslot}",
                            going_out_time=None
                        ).first()
                        if attendance_record:
                            attendance_record.going_out_time = end_time_datetime
                            db.session.commit()
                            return jsonify({'message': 'Going out time automatically set to period end time!'}), 200

                    # Student is coming in, create a new record
                    attendance_record = Attendance(
                        student_name=student_name,
                        batch_id=current_period.batch_id,
                        folder_id=class_id,
                        period=f"{current_period.day} {current_period.timeslot}",
                        coming_in_time=now
                    )
                    db.session.add(attendance_record)
                    db.session.commit()
                    return jsonify({'message': 'Attendance marked successfully!'}), 200
            else:
                return jsonify({'message': 'Student is not in the batch for the current period'}), 400
        else:
            return jsonify({'message': 'No ongoing period found for the current time and day'}), 400

    else:  # GET request
        folders = Folder.query.all()
        return render_template('attendance.html', folders=folders)

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if request.method == 'POST':
        student_name = request.form['student_name']

        now = datetime.now()
        current_day = now.strftime('%A')
        current_time = now.strftime('%H:%M')

        # Find the ongoing period across all classes
        timetables = Timetable.query.all()
        current_period = None
        current_class_id = None

        for timetable in timetables:
            if timetable.day == current_day:
                start_time, end_time = timetable.timeslot.split('-')
                if start_time <= current_time <= end_time:
                    current_period = timetable
                    current_class_id = timetable.folder_id
                    break

        # Calculate total duration for the ongoing period
        attendance_taken = False
        formatted_duration = None
        if current_period:
            batch = Batch.query.get(current_period.batch_id)
            if batch and student_name in batch.student_names.split(','):
                attendance_records = Attendance.query.filter_by(
                    student_name=student_name,
                    batch_id=current_period.batch_id,
                    date=now.date(),
                    period=f"{current_period.day} {current_period.timeslot}"
                ).all()

                total_duration = 0
                for record in attendance_records:
                    attendance_taken = True
                    if record.going_out_time:
                        total_duration += (record.going_out_time - record.coming_in_time).total_seconds()
                    else:
                        total_duration += (now - record.coming_in_time).total_seconds()

                hours, remainder = divmod(total_duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                formatted_duration = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

        # Fetch and aggregate attendance for all classes
        all_attendance = Attendance.query.filter_by(student_name=student_name).all()
        
        # Map batch IDs to names
        batch_names = {batch.id: batch.name for batch in Batch.query.all()}

        # Aggregate total duration spent for each unique combination
        aggregated_durations = {}
        for attendance in all_attendance:
            key = (attendance.date, attendance.folder_id, attendance.batch_id, attendance.period)
            if key not in aggregated_durations:
                aggregated_durations[key] = 0

            if attendance.going_out_time:
                aggregated_durations[key] += (attendance.going_out_time - attendance.coming_in_time).total_seconds()
            else:
                aggregated_durations[key] += (now - attendance.coming_in_time).total_seconds()

        # Convert aggregated durations to a readable format
        formatted_aggregated_durations = []
        for (date, folder_id, batch_id, period), total_seconds in aggregated_durations.items():
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_aggregated_durations.append({
                'date': date,
                'class_id': folder_id,
                'batch': batch_names.get(batch_id, 'Unknown'),  # Use batch name
                'period': period,
                'total_duration': f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
            })

        # Aggregate total duration spent in each batch and map batch IDs to names
        batch_durations = {}
        for attendance in all_attendance:
            if attendance.batch_id not in batch_durations:
                batch_durations[attendance.batch_id] = 0
                batch_name = batch_names.get(attendance.batch_id, 'Unknown')
                batch_durations[attendance.batch_id] = {
                    'name': batch_name,
                    'duration': 0
                }

            if attendance.going_out_time:
                batch_durations[attendance.batch_id]['duration'] += (attendance.going_out_time - attendance.coming_in_time).total_seconds()
            else:
                batch_durations[attendance.batch_id]['duration'] += (now - attendance.coming_in_time).total_seconds()

        # Convert batch durations to a readable format
        formatted_batch_durations = {
            details['name']: f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
            for batch_id, details in batch_durations.items()
            for hours, remainder in [divmod(details['duration'], 3600)]
            for minutes, seconds in [divmod(remainder, 60)]
        }

        return render_template(
            'student_dashboard.html',
            folders=Folder.query.all(),
            selected_student=student_name,
            current_period=current_period.timeslot if current_period else None,
            attendance_taken=attendance_taken,
            duration=formatted_duration,
            all_attendance=all_attendance,
            aggregated_durations=formatted_aggregated_durations,
            batch_durations=formatted_batch_durations,  # Pass the batch names with durations
            batch_names=batch_names  # Pass batch names dictionary
        )
    else:
        folders = Folder.query.all()
        return render_template('student_dashboard.html', folders=folders, aggregated_durations=[], batch_durations={}, batch_names={})  # Define default empty dicts



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
