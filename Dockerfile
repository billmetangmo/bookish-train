# Use an official lightweight Python image.
FROM python:3.9-alpine3.20

# Set up a working directory
WORKDIR /app

# Install dependencies using requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create and switch to a non-root user to run the app
RUN adduser -D bookish -u 1001
USER 1001

# Copy the Python script into the image under the non-root user
COPY --chown=bookish:bookish script.py .

# Define the entry point that runs the script
ENTRYPOINT ["python", "./script.py"]
