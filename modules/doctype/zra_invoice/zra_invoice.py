import frappe
from frappe.model.document import Document
from erpnext_zra_integration.zra_api import ZRAAPI

class ZRAInvoice(Document):
    def before_submit(self):
        settings = frappe.get_doc("ZRA Settings")
        zra_api = ZRAAPI(
            api_key=settings.api_key,
            device_serial_no=settings.device_serial_no,
            branch_id=settings.branch_id,
            tpin=settings.tpin
        )
        
        invoice_data = self.get_invoice_data()
        response = zra_api.submit_sales_invoice(invoice_data)
        
        if response.get('error'):
            frappe.throw(response['error'])

    def get_invoice_data(self):
        # Prepare the invoice data as required by the ZRA API
        invoice_data = {
            "invoice_no": self.name,
            "date": self.posting_date,
            "customer_name": self.customer_name,
            "items": [{
                "item_code": item.item_code,
                "description": item.description,
                "quantity": item.qty,
                "rate": item.rate,
                "amount": item.amount
            } for item in self.items],
            # we We can Add other fields as needed
        }
        return invoice_data
