# app.py

from flask import Flask, jsonify, request, abort, send_from_directory
from datastructure import FamilyStructure
import os

# Creamos la app Flask, indicándole que los archivos estáticos viven en la carpeta 'static'
app = Flask(__name__, static_folder='static')
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# ------------------------------------------------------------------
# 1) RUTA PARA SERVIR index.html (la interfaz) en la raíz "/"
# ------------------------------------------------------------------
@app.route('/', methods=['GET'])
def serve_homepage():
    # send_from_directory buscará un archivo llamado "index.html" dentro de la carpeta static/
    return send_from_directory(app.static_folder, 'index.html')


# ------------------------------------------------------------------
# 2) Datos en memoria: la familia Jackson
# ------------------------------------------------------------------
jackson_family = FamilyStructure("Jackson")
# Agregamos los miembros iniciales:
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})


# ------------------------------------------------------------------
# 3) ENDPOINTS DE LA API (JSON)
# ------------------------------------------------------------------

# 3.1) GET /members → obtener lista completa
@app.route('/members', methods=['GET'])
def handle_get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception:
        return jsonify({"error": "Hubo un error al obtener todos los miembros"}), 500


# 3.2) GET /members/<int:member_id> → obtener un miembro por ID
@app.route('/members/<int:member_id>', methods=['GET'])
def handle_get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception:
        return jsonify({"error": "Hubo un error al buscar el miembro"}), 500


# 3.3) POST /members → agregar un nuevo miembro
@app.route('/members', methods=['POST'])
def handle_add_member():
    if not request.is_json:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    data = request.get_json()
    # Validar campos mínimos
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Debe incluir 'first_name', 'age' y 'lucky_numbers'"}), 400

    # Validar que age sea entero > 0
    if not isinstance(data["age"], int) or data["age"] <= 0:
        return jsonify({"error": "'age' debe ser un entero mayor que cero"}), 400

    # Validar que lucky_numbers sea lista de enteros
    if not isinstance(data["lucky_numbers"], list) or not all(isinstance(n, int) for n in data["lucky_numbers"]):
        return jsonify({"error": "'lucky_numbers' debe ser una lista de enteros"}), 400

    new_member_payload = {
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }
    # Si el cliente envía un "id" explícito, validarlo
    if "id" in data:
        if not isinstance(data["id"], int) or data["id"] <= 0:
            return jsonify({"error": "'id' (si se proporciona) debe ser un entero > 0"}), 400
        new_member_payload["id"] = data["id"]

    try:
        new_member = jackson_family.add_member(new_member_payload)
        return jsonify(new_member), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Hubo un error al agregar el nuevo miembro"}), 500


# 3.4) DELETE /members/<int:member_id> → eliminar un miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    try:
        was_deleted = jackson_family.delete_member(member_id)
        if was_deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception:
        return jsonify({"error": "Hubo un error al eliminar el miembro"}), 500


# ------------------------------------------------------------------
# 4) Arrancar el servidor
# ------------------------------------------------------------------
if __name__ == "__main__":
    # El puerto 5000 por defecto, escucha en todas las direcciones
    app.run(host='0.0.0.0', port=5000, debug=True)
