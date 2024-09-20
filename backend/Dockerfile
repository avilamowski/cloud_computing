# Utiliza una imagen base oficial de AWS Lambda con Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Copia los archivos necesarios dentro de la imagen
COPY db.py models.py get_publications.py /var/task/

RUN mv /var/task/get_publications.py /var/task/lambda_function.py

# Instala las dependencias (si tienes un requirements.txt)
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Comando para ejecutar la función Lambda (lambda_handler es el punto de entrada)
CMD ["lambda_function.lambda_handler"]
