FROM python:3.9-slim

WORKDIR /app

COPY /src /app

CMD ["python", "CSP_Engine.py"]

# docker run -v src/out:/app/out csp-engine to pull the output from the container