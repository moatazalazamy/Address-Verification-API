import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from sklearn.model_selection import train_test_split
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load the CSV file
data = pd.read_csv('is_cairo_cities.csv')

# Separate features (addresses) and labels (is_cairo)
X = data['address'].values
y = data['is_cairo'].values

# Tokenize addresses
tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
tokenizer.fit_on_texts(X)
X = tokenizer.texts_to_sequences(X)

# Pad sequences to a uniform length
max_length = max([len(x) for x in X])
X = tf.keras.preprocessing.sequence.pad_sequences(X, maxlen=max_length, padding='post')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=max_length),
    LSTM(units=64),
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print('Test Accuracy:', accuracy)

model.save('address_verification_model.keras')
