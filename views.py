from flask import render_template, request, redirect, url_for, flash
from models import db, todo, Affirmation
from datetime import date, timedelta
types = [
             "Self Maintainence",
             "Work",
             "Rest",
             "Leisure",
        ]

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        # This route should retrieve all items from the database and display them on the page.
        tasks = todo.query.all()
        return render_template('indexnew.html', Tasks = tasks)
    
    @app.route('/complete_day', methods=['POST'])
    def complete_day():
        tasks = todo.query.all()
        for task in tasks:
            try:
                old_date = datetime.strptime(task.day, "%d/%m")
                new_date = old_date + timedelta(days=1)
                task.day = new_date.strftime("%d/%m")
            except ValueError:
                continue 
        db.session.commit()
        flash("Day Completed")
        return redirect(url_for('tasks'))

    @app.route('/tasks', methods=['GET'])
    def tasks():

        tasks = todo.query.order_by(todo.day, todo.value).all()
        today = date.today()
        today_str = today.strftime("%d/%m")
        yesterday = today - timedelta(days=1)
        yesterday_str = yesterday.strftime("%d/%m")
        today_tasks = [t for t in tasks if t.day == today_str]
        yesterday_tasks = [t for t in tasks if t.day == yesterday_str]
        existing_count = todo.query.filter_by(day=today_str).count()
        next_value = existing_count + 1

        return render_template(
            'todo.html',
            today_tasks=today_tasks,
            yesterday_tasks=yesterday_tasks,
            types=types,
            next_value=next_value,
            next_day_value=today_str,
            current_date=today_str,
            weekday=today.strftime("%A")
        )
    
    @app.route('/add', methods=['POST'])
    def add():
        name = request.form.get('name')
        type_ = request.form.get('type')
        day = request.form.get('day')  # now a string like "10/09"
        existing_count = todo.query.filter_by(day=day).count()

        add_task = todo(
            name=name,
            type=type_,
            day=day,
            value=existing_count + 1
        )
        db.session.add(add_task)
        db.session.commit()
        flash("Task Added Successfully")
        return redirect(url_for('tasks'))

    @app.route('/edit', methods=['POST'])
    def edit():
        task_id = request.form.get('id')
        task = todo.query.get_or_404(task_id)

        old_value = task.value
        old_day = task.day

        task.name = request.form['name']
        task.type = request.form['type']
        task.day = (request.form['day'])
        new_value = int(request.form['value'])

        if task.day == old_day:
            if new_value < old_value:
                tasks_to_shift = todo.query.filter(
                    todo.day == task.day,
                    todo.value >= new_value,
                    todo.value < old_value,
                    todo.id != task.id
                ).all()
                for t in tasks_to_shift:
                    t.value += 1
            elif new_value > old_value:
                tasks_to_shift = todo.query.filter(
                    todo.day == task.day,
                    todo.value <= new_value,
                    todo.value > old_value,
                    todo.id != task.id
                ).all()
                for t in tasks_to_shift:
                    t.value -= 1
        else:
            tasks_to_shift = todo.query.filter(
                todo.day == task.day,
                todo.value >= new_value
            ).all()                                                                                                                                                                     
            for t in tasks_to_shift:
                t.value += 1

        task.value = new_value

        db.session.commit()
        flash("Task Successfully Edited & Reordered")
        return redirect(url_for('tasks'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    
    @app.route('/delete', methods=['GET'])  
    def delete():
        task_id = request.args.get('id')
        task = todo.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        flash("Task Deleted Successfully")
        return redirect(url_for('tasks'))  
   
    @app.route('/affirmations', methods=['GET'])
    def affirmations():
        current_date = get_current_day()
        current_weekday = get_current_weekday()
        affirmations_list = Affirmation.query.all()
        return render_template(
            'affirmations.html',
            Affirmations=affirmations_list,
            current_date=current_date,
            current_weekday=current_weekday
        )

    @app.route('/add_affirmation', methods=['POST'])
    def add_affirmation():
        text = request.form.get('text')
        day = get_current_day()  # automatically today's date
        if text:
            new_affirmation = Affirmation(text=text, day=day)
            db.session.add(new_affirmation)
            db.session.commit()
            flash("Affirmation Added Successfully")
        return redirect(url_for('affirmations'))

    @app.route('/edit_affirmation', methods=['POST'])
    def edit_affirmation():
        aff_id = request.form.get('id')
        affirmation = Affirmation.query.get_or_404(aff_id)
        affirmation.text = request.form.get('text')
        db.session.commit()
        flash("Affirmation Edited Successfully")
        return redirect(url_for('affirmations'))
    
    @app.route('/toggle_task/<int:task_id>', methods=['POST'])
    def toggle_task(task_id):
        task = todo.query.get_or_404(task_id)
        completed = request.json.get('completed', False)
        task.completed = completed
        db.session.commit()
        return {"success": True}
    
def get_current_day():
    today = date.today()
    return today.strftime("%d/%m/%y")  # e.g., "10/09/25"

def get_current_weekday():
    today = date.today()
    return today.strftime("%A")  # e.g., "Monday"
