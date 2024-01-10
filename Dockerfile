FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Add the model file to the image
COPY address_verification_model.keras /app/

CMD ["python", "pp_app.py"]
