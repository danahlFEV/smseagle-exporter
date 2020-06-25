FROM python:3.5
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt
COPY . .
CMD ["python", "exporter.py"]
