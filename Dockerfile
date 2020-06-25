FROM python:3.5
RUN pip install --no-cache -r requirements.txt
ADD exporter.py .env
CMD ["python", "exporter.py"]
