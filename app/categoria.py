from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/pruebas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nomb = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self, cat_nom, cat_desp):
        self.cat_nomb = cat_nom
        self.cat_desp = cat_desp


with app.app_context():
    db.create_all()

# Schema


class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')


# Only one
categoria_schema = CategoriaSchema()
# Many
categorias_schema = CategoriaSchema(many=True)

#Get
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)


# Welcome Message
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido'})


if __name__ == "__main__":
    app.run(debug=True)
