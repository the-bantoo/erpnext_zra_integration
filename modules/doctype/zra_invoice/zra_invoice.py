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
        items = []
        for item in self.items:
            items.append({
                "itemCode": item.item_code,
                "itemName": item.item_name,
                "qty": item.qty,
                "unitPrice": item.rate,
                "totalAmount": item.amount,
                "taxAmount": item.tax_amount,
                "discountAmount": item.discount_amount
            })

        invoice_data = {
            "invoiceNo": self.name,
            "issueDate": self.posting_date,
            "tpin": self.tpin,
            "bhfId": self.branch_id,
            "customerName": self.customer_name,
            "items": items,
            "totalAmount": self.total,
            "taxAmount": self.total_taxes_and_charges,
            "totalDiscount": self.total_discount,
            "paymentType": self.payment_type,
            "currency": self.currency,
            "exchangeRate": self.conversion_rate
        }
        return invoice_data
