# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.modelos.inventario import Inventario
from src.modelos.producto import Producto
from src.modelos.usuario import Usuario
from src.modulos.gestor_usuarios import GestorUsuarios
from src.modulos.tienda import Tienda
from src.modulos.persistencia import PersistenciaJSON
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.modelos.venta import Venta
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inicializar los componentes del sistema
gestor = GestorUsuarios()

# Cargar el inventario primero
def cargar_inventario(ruta: str = "data/inventario.json") -> Inventario:
    datos = PersistenciaJSON.cargar_datos(ruta)
    productos = [Producto(**p) for p in datos] if datos else []
    return Inventario(productos)

def guardar_inventario(inventario: Inventario):
    datos = [p.to_dict() for p in inventario.productos]
    PersistenciaJSON.guardar_datos("data/inventario.json", datos)

# Inicializar inventario y tienda
inventario = cargar_inventario()
tienda = Tienda(inventario)

# Ruta de prueba para verificar que el backend está funcionando
@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "Backend del Gestor de Inventario está funcionando"}), 200

# Endpoints de la API
@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos = [p.to_dict() for p in inventario.productos]
    return jsonify(productos)

@app.route('/api/productos', methods=['POST'])
def add_producto():
    try:
        data = request.json
        nuevo = Producto(
            id=data['id'],
            nombre=data['nombre'],
            precio=data['precio'],
            cantidad=data['cantidad'],
            categoria=data['categoria'],
            stock_minimo=data['stock_minimo']
        )
        inventario.agregar_producto(nuevo)
        guardar_inventario(inventario)
        return jsonify({"mensaje": "Producto agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        resultado = inventario.eliminar_producto(id)
        guardar_inventario(inventario)
        return jsonify({"mensaje": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/productos/<int:id>/stock', methods=['PUT'])
def update_stock(id):
    try:
        data = request.json
        cantidad = data['cantidad']
        resultado = inventario.actualizar_stock(id, cantidad)
        guardar_inventario(inventario)
        return jsonify({"mensaje": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = [{"id": id, "nombre": u.nombre, "rol": u.rol} for id, u in gestor.usuarios.items()]
    return jsonify(usuarios)

@app.route('/api/usuarios', methods=['POST'])
def add_usuario():
    try:
        data = request.json
        nuevo = Usuario(
            id=data['id'],
            nombre=data['nombre'],
            rol=data['rol'],
            contraseña=data['contraseña']
        )
        resultado = gestor.crear_usuario(nuevo)
        return jsonify({"mensaje": resultado}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        resultado = gestor.eliminar_usuario(id)
        return jsonify({"mensaje": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/ventas', methods=['POST'])
def registrar_venta():
    try:
        data = request.json
        id_venta = len(tienda.historial_ventas) + 1
        fecha = data['fecha']
        productos = [(next(p for p in inventario.productos if p.id == item['id']), item['cantidad']) for item in data['productos']]
        id_empleado = data['id_empleado']
        venta = Venta(id_venta, fecha, productos, id_empleado, inventario)
        resultado = tienda.registrar_venta(venta, inventario)
        guardar_inventario(inventario)
        return jsonify({"mensaje": resultado}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/ventas', methods=['GET'])
def get_ventas():
    historial = tienda.generar_historial()
    return jsonify(historial)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)