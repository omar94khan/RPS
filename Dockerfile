# Use an official Python runtime as the base image
FROM python:3.9-slim

# Tesseract OCR Installation
RUN apt-get update -y && apt-get install -y lsb-release && apt-get install -y apt-transport-https
RUN echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null
RUN apt-get update -y -oAcquire::AllowInsecureRepositories=true
RUN apt-get install -y --allow-unauthenticated notesalexp-keyring -oAcquire::AllowInsecureRepositories=true
RUN apt-get update -y && apt-get install -y tesseract-ocr procps 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirement.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the PATH variable to include the Tesseract executable
ENV PATH="/usr/bin:${PATH}"

# Expose any necessary ports
EXPOSE 10038

# Set the entrypoint command or default command for the container
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${SERVER_PORT} main:app"]
