from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import concurrent.futures
import keras

app = Flask(__name__)

# Load the model
model = load_model('address_verification_model.keras')

# Load the tokenizer
tokenizer = keras.preprocessing.text.Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
tokenizer.fit_on_texts(pd.read_csv('is_cairo_cities.csv')['address'].values)

def process_address(address):
    # Tokenize and pad the input address
    sequence = tokenizer.texts_to_sequences([address])
    padded_sequence = pad_sequences(sequence, maxlen=model.input_shape[1], padding='post')

    # Make a prediction
    prediction = model.predict(padded_sequence)[0][0]
    print(prediction)
    # Return the result
    return {'address': address, 'is_cairo': bool(round(prediction))}

@app.route('/verify_address', methods=['POST'])
def verify_address():
    try:
        # Get the input address from the request
        data = request.get_json()
        address = data.get('address')

        if not address:
            raise ValueError("Missing 'address' in the request JSON.")

        # Use concurrent.futures to parallelize processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(process_address, address)
            result = future.result()

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
