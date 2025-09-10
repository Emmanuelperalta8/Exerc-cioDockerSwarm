FROM python:3.10-slim
WORKDIR /app
COPY frontend.py /app/
RUN pip install flask requests
CMD ["python", "frontend.py"]