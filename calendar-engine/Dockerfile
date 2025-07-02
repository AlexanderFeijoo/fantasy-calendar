# Start from a lightweight Python 3.11 image
FROM python:3.11-slim

# Set the app directory inside the container
WORKDIR /app

# Copy just the requirements file first (better layer caching)
COPY requirements.txt .

# Install all the Python packages we need
RUN pip install --no-cache-dir -r requirements.txt

# Now bring over the rest of the app code
COPY . .

# Open up port 5000 so we can hit this from localhost
EXPOSE 5000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
