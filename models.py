"""Models for Cupcake app"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

default_img = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """db of cupcake flavors"""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating =  db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=default_img)

    def __repr__(self):
        """Show cupcake info in nice format"""
        c = self
        return f'<Cupcake id={c.id}, flavor={c.flavor}, size={c.size}, rating={c.rating}, image={c.image}>'

    def img(self):
        """Return image for cupcake"""
        return self.image or default_img

    def dictionary(self):
        """Serialize cupcake to a dictionary of cupcake info"""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

