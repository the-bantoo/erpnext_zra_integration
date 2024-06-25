import requests
import json

class ZRAAPI:
    BASE_URL = "http://<hostname>:<server.port>/<vsdcpath>"

    def __init__(self, api_key, device_serial_no, branch_id, tpin):
        self.api_key = api_key
        self.device_serial_no = device_serial_no
        self.branch_id = branch_id
        self.tpin = tpin

    def initialize_device(self):
        url = f"{self.BASE_URL}/initializer/selectInitInfo"
        payload = {
            "tpin": self.tpin,
            "bhfId": self.branch_id,
            "dvcSrlNo": self.device_serial_no
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()

    def submit_sales_invoice(self, invoice_data):
        url = f"{self.BASE_URL}/sales/newInvoice"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.post(url, data=json.dumps(invoice_data), headers=headers)
        return response.json()

    # We can Add other methods as required by the VSDC API
