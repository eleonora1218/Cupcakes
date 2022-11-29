"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
import pdb

app = Flask(__name__)
app.config['SECRET_KEY'] = "moomooimacow"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

# 127.0.0.1:5000/
@app.route('/')
def homepage():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcake = Cupcake.query.all()
    return render_template('homepage.html', cupcake=cupcake)

# 127.0.0.1:5000/api/cupcakes
@app.route('/api/cupcakes')
def list_cupcakes():
    """View all cupcakes in JSON"""
    cupcakes = [cupcake.dictionary() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

# 127.0.0.1:5000/api/cupcakes/1
@app.route('/api/cupcakes/<int:id>')
def list_cupcake(id):
    """View single cupcake in JSON via id"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.dictionary())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates new cupcake in JSON"""

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    response = jsonify(cupcake=cupcake.dictionary())
    return (response, 201)

# 127.0.0.1:5000/api/cupcakes/1
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def edit_cupcake(id):
    """Edit a cupcake in JSON"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.dictionary())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def remove_cupcake(id):
    """Delete cupcake and return confirmation message in JSON"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="Deleted")