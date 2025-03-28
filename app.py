from flask import Flask, jsonify, request, render_template
import datetime
import hashlib
import json

# Clase Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transacciones = []
        self.crear_bloque(proof=1, previo_hash='0')  # Bloque génesis

    def crear_bloque(self, proof=0, previo_hash='0'):
        bloque = {
            'indice': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previo_hash': previo_hash,
            'transacciones': self.transacciones,
            'hash_actual': '',
        }
        bloque['hash_actual'] = self.calcular_hash(bloque)
        self.transacciones = []  # Vaciar las transacciones después de agregar el bloque
        self.chain.append(bloque)
        return bloque

    def calcular_hash(self, bloque):
        bloque_copia = bloque.copy()
        bloque_copia.pop('hash_actual', None)  # Quitar el hash actual para evitar ciclos
        bloque_str = json.dumps(bloque_copia, sort_keys=True).encode()
        return hashlib.sha256(bloque_str).hexdigest()

    def obtener_ultimo_bloque(self):
        return self.chain[-1]

# Inicializar Flask y la Blockchain
app = Flask(__name__)
blockchain = Blockchain()

# Ruta para obtener la cadena completa
@app.route('/chain', methods=['GET'])
def obtener_cadena():
    response = {'chain': blockchain.chain, 'longitud': len(blockchain.chain)}
    return jsonify(response), 200

# Ruta para agregar transacciones con los campos: Emisor, Receptor, Monto, Entidad
@app.route('/agregar_transaccion', methods=['POST'])
def agregar_transaccion():
    json_data = request.get_json()
    
    # Obtenemos los datos de la transacción
    emisor = json_data.get('emisor')
    receptor = json_data.get('receptor')
    monto = json_data.get('monto')
    entidad = json_data.get('entidad')
    
    if not emisor or not receptor or not monto or not entidad:
        return 'Faltan datos en la transacción', 400

    # Crear una nueva transacción
    transaccion = {
        'emisor': emisor,
        'receptor': receptor,
        'monto': monto,
        'entidad': entidad,
    }
    
    blockchain.transacciones.append(transaccion)
    return jsonify({'mensaje': 'Transacción agregada con éxito'}), 201

# Ruta para minar un bloque
@app.route('/minar_bloque', methods=['POST'])
def minar_bloque():
    ultimo_bloque = blockchain.obtener_ultimo_bloque()
    previo_hash = ultimo_bloque['hash_actual']
    bloque = blockchain.crear_bloque(proof=12345, previo_hash=previo_hash)  # Proof estático
    response = {
        'mensaje': '¡Bloque minado con éxito!',
        'bloque': bloque,
    }
    return jsonify(response), 200

# Ruta principal (frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
