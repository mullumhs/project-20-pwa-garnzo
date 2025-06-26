from flask import render_template, request, redirect, url_for, flash
from models import db, Game # Also import your database model here

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        # This route should retrieve all items from the database and display them on the page.
        games = Game.query.all()
        return render_template('indexnew.html', games = games)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            new_game = Game(
            title=request.form['title'],
            publisher=request.form['publisher'],
            year=int(request.form['year']),
            rating=float(request.form['rating']),
            genre=request.form['title'],
            )
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            # Display the add item form (GET request)
            return render_template('todo.html')

    @app.route('/update', methods=['GET','POST'])
    def update():
        id = request.args.get('id')  		# Get the item ID from form
        game = Game.query.get(id)  	# Fetch item by ID
        #game.name = request.form.get('name')  	# Update name
        #db.session.commit()  			# Commit changes
        #return redirect(url_for('home'))
        return render_template('edit.html', game = game)
        return redirect(url_for('home'))

    @app.route('/delete', methods=['GET'])
    def delete():
        id = request.args.get('id')  	# Get the item ID from form
        game = Game.query.get(id)  # Fetch item by ID
        db.session.delete(game)  	# Delete item
        db.session.commit()  		# Commit changes
        return redirect(url_for('home'))