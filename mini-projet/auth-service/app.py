from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

# Login → renvoie un token JWT
@app.route('/login', methods=['POST'])
def login():
    token = jwt.encode({
        'user': 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

# Vérification du token
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    token = data.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({'valid': True})
    except:
        return jsonify({'valid': False}), 401

if __name__ == '__main__':
    app.run(port=5000)
