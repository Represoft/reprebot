# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 (streamlit) and 8000 (fastapi) available to the world outside this container
EXPOSE 8501 8000

# Define environment variable
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV API_HOST=${API_HOST}

# Run the entrypoint script when the container launches
ENTRYPOINT ["/app/entrypoint.sh"]
