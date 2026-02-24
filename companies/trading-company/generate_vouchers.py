#!/usr/bin/env python3
"""
Tally Prime Voucher Generator
Generates 3 years of realistic voucher data for Trading Company
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
from datetime import datetime, timedelta

# Company Details
COMPANY_NAME = "Test Trading Company"
GSTIN = "27AAACT1234C1Z5"
STATE = "Maharashtra"

# Date Range
START_DATE = datetime(2023, 4, 1)
END_DATE = datetime(2025, 12, 31)

# Customers (Sundry Debtors)
CUSTOMERS = [
    {"name": "Acme Electronics Pvt Ltd", "state": "Maharashtra", "gstin": "27AAACA1234B1Z5"},
    {"name": "TechWorld Solutions", "state": "Delhi", "gstin": "07AAACT5678C1Z3"},
    {"name": "Digital Systems Inc", "state": "Karnataka", "gstin": "29AAACD9012D1Z1"},
    {"name": "Sharma Electronics", "state": "Maharashtra", "gstin": "27AAACS3456E1Z8"},
    {"name": "Patel Trading Co", "state": "Gujarat", "gstin": "24AAACP7890F1Z2"},
]

# Suppliers (Sundry Creditors)
SUPPLIERS = [
    {"name": "Samsung India Electronics Ltd", "state": "Uttar Pradesh", "gstin": "09AAACS1234G1Z6"},
    {"name": "LG Electronics India", "state": "Haryana", "gstin": "06AAACL5678H1Z4"},
    {"name": "Sony India Pvt Ltd", "state": "Haryana", "gstin": "06AAACS9012I1Z9"},
    {"name": "Wholesale Electronics Hub", "state": "Maharashtra", "gstin": "27AAACW3456J1Z7"},
    {"name": "Mumbai Tech Distributors", "state": "Maharashtra", "gstin": "27AAACM7890K1Z5"},
]

# Stock Items with HSN codes and rates
STOCK_ITEMS = [
    {"name": "Samsung 43\" Smart TV", "hsn": "8528", "rate": 25000, "gst_rate": 18},
    {"name": "LG 50\" 4K TV", "hsn": "8528", "rate": 35000, "gst_rate": 18},
    {"name": "Sony Headphones WH-1000XM4", "hsn": "8518", "rate": 12000, "gst_rate": 18},
    {"name": "Samsung Galaxy Tab", "hsn": "8471", "rate": 28000, "gst_rate": 18},
    {"name": "LG Washing Machine 7kg", "hsn": "8450", "rate": 18000, "gst_rate": 18},
    {"name": "Sony Bluetooth Speaker", "hsn": "8518", "rate": 5000, "gst_rate": 18},
    {"name": "HDMI Cable 2m", "hsn": "8544", "rate": 500, "gst_rate": 18},
    {"name": "USB Cable Type-C", "hsn": "8544", "rate": 300, "gst_rate": 18},
    {"name": "Power Bank 10000mAh", "hsn": "8507", "rate": 1500, "gst_rate": 18},
    {"name": "Wireless Mouse", "hsn": "8471", "rate": 800, "gst_rate": 18},
    {"name": "Keyboard Wireless", "hsn": "8471", "rate": 1200, "gst_rate": 18},
    {"name": "Webcam HD 1080p", "hsn": "8525", "rate": 2500, "gst_rate": 18},
    {"name": "External HDD 1TB", "hsn": "8471", "rate": 4000, "gst_rate": 18},
    {"name": "Pen Drive 64GB", "hsn": "8471", "rate": 600, "gst_rate": 18},
    {"name": "Mobile Charger Fast", "hsn": "8504", "rate": 1000, "gst_rate": 18},
]

# Banks
BANKS = ["HDFC Bank", "ICICI Bank"]

def prettify(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

def get_date_range():
    """Generate list of business dates between START_DATE and END_DATE"""
    dates = []
    current = START_DATE
    while current <= END_DATE:
        # Skip Sundays (business days only)
        if current.weekday() < 6:
            dates.append(current)
        current += timedelta(days=1)
    return dates

def is_interstate(from_state, to_state):
    """Check if transaction is interstate"""
    return from_state != to_state

def calculate_gst(amount, gst_rate, is_interstate_flag):
    """Calculate GST amounts"""
    gst_amount = (amount * gst_rate) / 100
    if is_interstate_flag:
        return {"igst": gst_amount, "cgst": 0, "sgst": 0}
    else:
        return {"igst": 0, "cgst": gst_amount / 2, "sgst": gst_amount / 2}

def create_voucher_element(voucher_type, date, number, entries, narration=""):
    """Create a voucher XML element"""
    voucher = ET.Element("VOUCHER")
    
    # Voucher type
    vtype = ET.SubElement(voucher, "VOUCHERTYPENAME")
    vtype.text = voucher_type
    
    # Date
    vdate = ET.SubElement(voucher, "DATE")
    vdate.text = date.strftime("%Y%m%d")
    
    # Voucher number
    vnumber = ET.SubElement(voucher, "VOUCHERNUMBER")
    vnumber.text = str(number)
    
    # Narration
    if narration:
        vnarration = ET.SubElement(voucher, "NARRATION")
        vnarration.text = narration
    
    # Ledger entries
    for entry in entries:
        ledger_entry = ET.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
        
        ledger_name = ET.SubElement(ledger_entry, "LEDGERNAME")
        ledger_name.text = entry["name"]
        
        amount = ET.SubElement(ledger_entry, "AMOUNT")
        amount.text = str(entry["amount"])
        
        # Add tax details if present
        if "tax_type" in entry:
            tax_type = ET.SubElement(ledger_entry, "TAXTYPE")
            tax_type.text = entry["tax_type"]
        
        if "tax_rate" in entry:
            tax_rate = ET.SubElement(ledger_entry, "TAXRATE")
            tax_rate.text = str(entry["tax_rate"])
        
        if "hsn" in entry:
            hsn = ET.SubElement(ledger_entry, "HSN")
            hsn.text = entry["hsn"]
    
    return voucher

def generate_sales_voucher(date, voucher_num):
    """Generate a Sales voucher"""
    customer = random.choice(CUSTOMERS)
    is_interstate_flag = is_interstate(STATE, customer["state"])
    
    # Select 2-4 random items
    num_items = random.randint(2, 4)
    items = random.sample(STOCK_ITEMS, num_items)
    
    entries = []
    total_amount = 0
    narration_parts = []
    
    for item in items:
        qty = random.randint(1, 10)
        amount = item["rate"] * qty
        total_amount += amount
        
        # Sales ledger entry
        entries.append({
            "name": "Sales - Interstate" if is_interstate_flag else "Sales - Local",
            "amount": -amount,  # Credit
            "hsn": item["hsn"]
        })
        
        narration_parts.append(f"{item['name']} x{qty}")
    
    # Calculate GST
    gst = calculate_gst(total_amount, 18, is_interstate_flag)
    
    if gst["igst"] > 0:
        entries.append({"name": "IGST Output", "amount": -gst["igst"]})
    else:
        entries.append({"name": "CGST Output", "amount": -gst["cgst"]})
        entries.append({"name": "SGST Output", "amount": -gst["sgst"]})
    
    # Customer entry (Debit)
    total_with_gst = total_amount + gst["igst"] + gst["cgst"] + gst["sgst"]
    entries.append({
        "name": customer["name"],
        "amount": total_with_gst  # Debit
    })
    
    narration = f"Sale to {customer['name']}: {', '.join(narration_parts)}"
    
    return create_voucher_element("Sales", date, voucher_num, entries, narration)

def generate_purchase_voucher(date, voucher_num):
    """Generate a Purchase voucher"""
    supplier = random.choice(SUPPLIERS)
    is_interstate_flag = is_interstate(STATE, supplier["state"])
    
    # Select 2-5 random items
    num_items = random.randint(2, 5)
    items = random.sample(STOCK_ITEMS, num_items)
    
    entries = []
    total_amount = 0
    narration_parts = []
    
    for item in items:
        qty = random.randint(2, 20)
        amount = item["rate"] * qty
        total_amount += amount
        
        # Purchase ledger entry
        entries.append({
            "name": "Purchase - Interstate" if is_interstate_flag else "Purchase - Local",
            "amount": amount,  # Debit
            "hsn": item["hsn"]
        })
        
        narration_parts.append(f"{item['name']} x{qty}")
    
    # Calculate GST
    gst = calculate_gst(total_amount, 18, is_interstate_flag)
    
    if gst["igst"] > 0:
        entries.append({"name": "IGST Input", "amount": gst["igst"]})
    else:
        entries.append({"name": "CGST Input", "amount": gst["cgst"]})
        entries.append({"name": "SGST Input", "amount": gst["sgst"]})
    
    # Supplier entry (Credit)
    total_with_gst = total_amount + gst["igst"] + gst["cgst"] + gst["sgst"]
    entries.append({
        "name": supplier["name"],
        "amount": -total_with_gst  # Credit
    })
    
    narration = f"Purchase from {supplier['name']}: {', '.join(narration_parts)}"
    
    return create_voucher_element("Purchase", date, voucher_num, entries, narration)

def generate_payment_voucher(date, voucher_num):
    """Generate a Payment voucher"""
    bank = random.choice(BANKS)
    amount = random.randint(5000, 50000)
    
    # Random expense type
    expense_types = [
        ("Rent Expense", "Monthly office rent"),
        ("Salary Expense", "Staff salary payment"),
        ("Electricity Charges", "Electricity bill payment"),
        ("Internet & Phone", "Internet and phone charges"),
        ("Transport Charges", "Transport expenses"),
    ]
    
    expense, narration = random.choice(expense_types)
    
    entries = [
        {"name": expense, "amount": amount},  # Debit
        {"name": bank, "amount": -amount}  # Credit
    ]
    
    return create_voucher_element("Payment", date, voucher_num, entries, narration)

def generate_receipt_voucher(date, voucher_num):
    """Generate a Receipt voucher"""
    bank = random.choice(BANKS)
    amount = random.randint(10000, 100000)
    
    # Random receipt type
    receipt_types = [
        ("Interest Income", "Interest received from bank"),
        ("Discount Received", "Discount from supplier"),
    ]
    
    income, narration = random.choice(receipt_types)
    
    entries = [
        {"name": bank, "amount": amount},  # Debit
        {"name": income, "amount": -amount}  # Credit
    ]
    
    return create_voucher_element("Receipt", date, voucher_num, entries, narration)

def generate_contra_voucher(date, voucher_num):
    """Generate a Contra voucher (Cash ↔ Bank)"""
    bank = random.choice(BANKS)
    amount = random.randint(10000, 50000)
    
    # Randomly decide direction
    if random.random() > 0.5:
        # Cash to Bank
        entries = [
            {"name": bank, "amount": amount},  # Debit
            {"name": "Cash", "amount": -amount}  # Credit
        ]
        narration = f"Cash deposited to {bank}"
    else:
        # Bank to Cash
        entries = [
            {"name": "Cash", "amount": amount},  # Debit
            {"name": bank, "amount": -amount}  # Credit
        ]
        narration = f"Cash withdrawn from {bank}"
    
    return create_voucher_element("Contra", date, voucher_num, entries, narration)

def generate_journal_voucher(date, voucher_num):
    """Generate a Journal voucher"""
    amount = random.randint(1000, 10000)
    
    journal_types = [
        ("Depreciation", "Depreciation on assets", "Office Expenses", "Drawings"),
        ("Round Off", "Round off adjustment", "Round Off", "Office Expenses"),
    ]
    
    j_type, narration, debit_ledger, credit_ledger = random.choice(journal_types)
    
    entries = [
        {"name": debit_ledger, "amount": amount},  # Debit
        {"name": credit_ledger, "amount": -amount}  # Credit
    ]
    
    return create_voucher_element("Journal", date, voucher_num, entries, narration)

def generate_all_vouchers():
    """Generate all vouchers for 3 years"""
    envelope = ET.Element("ENVELOPE")
    
    # Header
    header = ET.SubElement(envelope, "HEADER")
    version = ET.SubElement(header, "VERSION")
    version.text = "1"
    trequest = ET.SubElement(header, "TALLYREQUEST")
    trequest.text = "Import Data"
    type_elem = ET.SubElement(header, "TYPE")
    type_elem.text = "Data"
    id_elem = ET.SubElement(header, "ID")
    id_elem.text = "Transactions"
    
    # Body
    body = ET.SubElement(envelope, "BODY")
    importdata = ET.SubElement(body, "IMPORTDATA")
    requestdesc = ET.SubElement(importdata, "REQUESTDESC")
    reportname = ET.SubElement(requestdesc, "REPORTNAME")
    reportname.text = "All Vouchers"
    
    staticvars = ET.SubElement(requestdesc, "STATICVARIABLES")
    svc = ET.SubElement(staticvars, "SVCURRENTCOMPANY")
    svc.text = COMPANY_NAME
    
    requestdata = ET.SubElement(importdata, "REQUESTDATA")
    
    # Generate vouchers
    dates = get_date_range()
    voucher_counters = {
        "Sales": 1,
        "Purchase": 1,
        "Payment": 1,
        "Receipt": 1,
        "Contra": 1,
        "Journal": 1,
    }
    
    total_vouchers = 0
    
    for date in dates:
        # Generate 5-8 vouchers per day
        num_vouchers = random.randint(5, 8)
        
        for _ in range(num_vouchers):
            voucher_type = random.choices(
                ["Sales", "Purchase", "Payment", "Receipt", "Contra", "Journal"],
                weights=[30, 30, 15, 10, 10, 5]
            )[0]
            
            voucher_num = voucher_counters[voucher_type]
            voucher_counters[voucher_type] += 1
            
            if voucher_type == "Sales":
                voucher = generate_sales_voucher(date, voucher_num)
            elif voucher_type == "Purchase":
                voucher = generate_purchase_voucher(date, voucher_num)
            elif voucher_type == "Payment":
                voucher = generate_payment_voucher(date, voucher_num)
            elif voucher_type == "Receipt":
                voucher = generate_receipt_voucher(date, voucher_num)
            elif voucher_type == "Contra":
                voucher = generate_contra_voucher(date, voucher_num)
            elif voucher_type == "Journal":
                voucher = generate_journal_voucher(date, voucher_num)
            
            requestdata.append(voucher)
            total_vouchers += 1
    
    return envelope, total_vouchers

if __name__ == "__main__":
    print("Generating Tally Prime vouchers...")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    
    envelope, total = generate_all_vouchers()
    
    # Write to file
    xml_string = prettify(envelope)
    
    output_file = "vouchers.xml"
    with open(output_file, "wb") as f:
        f.write(xml_string.encode('utf-8'))
    
    print(f"✓ Generated {total} vouchers")
    print(f"✓ Saved to {output_file}")
    print(f"✓ File size: {len(xml_string) / 1024:.2f} KB")
