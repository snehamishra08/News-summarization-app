# Use official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Create a non-root user and switch to it (optional for security)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy requirements and install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all project files to /app
COPY --chown=user . /app

# Run Flask and Streamlit together
CMD ["sh", "-c", "python api.py & streamlit run app.py --server.port 7860 --server.enableCORS false --server.address 0.0.0.0"]
