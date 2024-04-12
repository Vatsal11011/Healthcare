from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/prediction', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        values_list = data.get('values', [])

        
        print(values_list)

        return jsonify({'message': 'Data received successfully'})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error processing data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
