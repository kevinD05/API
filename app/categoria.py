from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))


    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

with app.app_context():
    db.create_all()

#Esquema categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields =('cat_id','cat_nom','cat_desp')

#una sola respuesta
categoria_schema = CategoriaSchema()
#cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET############
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#GET X ID######
@app.route('/categoria', methods=['GET'])
def get_catrgoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#POST#################
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    
    nuevocategoria = Categoria(cat_nom, cat_desp)
    
    db.session.add(nuevocategoria)
    db.session.commit()
    return categoria_schema.jsonify(nuevocategoria)


#put#################
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actulizarcategoria = Categoria.query.get(id)

    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    actulizarcategoria.cat_nom = cat_nom
    actulizarcategoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actulizarcategoria) 

@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminarcategoria = Categoria.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarcategoria)



#Mensaje de Bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido Prueba de API'})


if __name__=="__main__":
    app.run(debug=True)