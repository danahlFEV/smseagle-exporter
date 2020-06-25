from dotenv import load_dotenv
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import sys
import requests
import json
import time
import os

load_dotenv()

def call_api(method):
  query = {"method":method, "params":{"access_token":os.getenv("access_token")}}
  resp = requests.post(os.getenv("smseagle")+"/index.php/jsonrpc/sms", json=query)
  return resp.json()["result"]

class CustomCollector(object):
  def collect(self):
    yield GaugeMetricFamily('outgoing_queue_length', "number of messages in database that wait to be processed by GSM/3G-modem", value=call_api("sms.get_queue_length"))
    yield CounterMetricFamily('sentitems_length', "number of messages in database Sentitems folder", value=call_api("sms.get_sentitems_length"))
    yield GaugeMetricFamily('gsmsignal', "GSM/3G signal strength in percent: values between 0-100", value=call_api("signal.get_gsmsignal"))

if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  start_http_server(int(8000))
  REGISTRY.register(CustomCollector())

  while True: time.sleep(1)
