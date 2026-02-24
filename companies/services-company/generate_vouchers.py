#!/usr/bin/env python3
"""
Tally Prime Voucher Generator - Services Company
Generates 3 years of realistic voucher data for IT Consulting Company
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
from datetime import datetime, timedelta

# Company Details
COMPANY_NAME = "Test Services Company"
GSTIN = "29AAACS9012E1Z1"
STATE = "Karnataka"

# Date Range
START_DATE = datetime(2023, 4, 1)
END_DATE = datetime(2025, 12, 31)

# Clients (Sundry Debtors)
CLIENTS = [
    {"name": "TechCorp Solutions Pvt Ltd", "state": "Karnataka", "gstin": "29AAACT1234P1Z5"},
    {"name": "GlobalInfotech Inc", "state": "Haryana", "gstin": "06AAACG5678Q1Z3"},
    {"name": "DataSoft Systems", "state": "Telangana", "gstin": "36AAACD9012R1Z1"},
    {"name": "CloudNine Technologies", "state": "Maharashtra", "gstin": "27AAACC3456S1Z8"},
    {"name": "StartupHub Innovations", "state": "Delhi", "gstin": "07AAACS7890T1Z2"},
]

# Vendors (Sundry Creditors)
VENDORS = [
    {"name": "AWS India Pvt Ltd", "state": "Karnataka", "gstin": "29AAACA1234U1Z6"},
    {"name": "Microsoft India", "state": "Telangana", "gstin": "36AAACM5678V1Z4"},
    {"name": "Google Cloud India", "state": "Haryana", "gstin": "06AAACG9012W1Z9"},
    {"name": "Office Supplies Co", "state": "Karnataka", "gstin": "29AAACO3456X1Z7"},
]

# Service Types with rates
SERVICES = [
    {"name": "IT Consulting", "sac": "998311", "rate": 5000, "gst_rate": 18},
    {"name": "Software Development", "sac": "998313", "rate": 8000, "gst_rate": 18},
    {"name": "Cloud Migration Services", "sac": "998314", "rate": 6000, "gst_rate": 18},
    {"name": "Data Analytics", "sac": "998312", "rate": 7000, "gst_rate": 18},
    {"name": "Mobile App Development", "sac": "998313", "rate": 9000, "gst_rate": 18},
    {"name": "Web Development", "sac": "998313", "rate": 4000, "gst_rate": 18},
    {"name": "DevOps Consulting", "sac": "998311", "rate": 6500, "gst_rate": 18},
    {"name": "Cybersecurity Audit", "sac": "998311", "rate": 10000, "gst_rate": 18},
    {"name": "AI/ML Implementation", "sac": "998312", "rate": 12000, "gst_rate": 18},
    {"name": "Technical Support", "sac": "998315", "rate": 3000, "gst_rate": 18},
]

# Banks
BANKS = ["HDFC Bank", "ICICI Bank"]

# Cost Centers
COST_CENTERS = ["Project Alpha", "Project Beta", "Project Gamma", "Support & Maintenance", "Internal R&D"]

def prettify(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

def get_date_range():
    """Generate list of business dates"""
    dates = []
    current = START_DATE
    while current <= END_DATE:
        if current.weekday() < 6:  # Mon-Sat
            dates.append(current)
        current += timedelta(days=1)
    return dates

def is_interstate(from_state, to_state):
    return from_state != to_state

def calculate_gst(amount, gst_rate, is_interstate_flag):
    gst_amount = (amount * gst_rate) / 100
    if is_interstate_flag:
        return {"igst": gst_amount, "cgst": 0, "sgst": 0}
    else:
        return {"igst": 0, "cgst": gst_amount / 2, "sgst": gst_amount / 2}

def create_voucher_element(voucher_type, date, number, entries, narration=""):
    voucher = ET.Element("VOUCHER")
    
    vtype = ET.SubElement(voucher, "VOUCHERTYPENAME")
    vtype.text = voucher_type
    
    vdate = ET.SubElement(voucher, "DATE")
    vdate.text = date.strftime("%Y%m%d")
    
    vnumber = ET.SubElement(voucher, "VOUCHERNUMBER")
    vnumber.text = str(number)
    
    if narration:
        vnarration = ET.SubElement(voucher, "NARRATION")
        vnarration.text = narration
    
    for entry in entries:
        ledger_entry = ET.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
        ledger_name = ET.SubElement(ledger_entry, "LEDGERNAME")
        ledger_name.text = entry["name"]
        amount = ET.SubElement(ledger_entry, "AMOUNT")
        amount.text = str(entry["amount"])
        
        if "tax_type" in entry:
            tax_type = ET.SubElement(ledger_entry, "TAXTYPE")
            tax_type.text = entry["tax_type"]
        if "tax_rate" in entry:
            tax_rate = ET.SubElement(ledger_entry, "TAXRATE")
            tax_rate.text = str(entry["tax_rate"])
        if "sac" in entry:
            sac = ET.SubElement(ledger_entry, "SAC")
            sac.text = entry["sac"]
    
    return voucher

def generate_service_invoice(date, voucher_num):
    """Generate a service invoice (Sales voucher)"""
    client = random.choice(CLIENTS)
    is_interstate_flag = is_interstate(STATE, client["state"])
    
    # Select 1-3 services
    num_services = random.randint(1, 3)
    services = random.sample(SERVICES, num_services)
    
    entries = []
    total_amount = 0
    narration_parts = []
    
    for service in services:
        # Random hours or fixed project fee
        if random.random() > 0.5:
            hours = random.randint(10, 100)
            amount = service["rate"] * hours
            narration_parts.append(f"{service['name']} ({hours} hrs)")
        else:
            amount = random.randint(50000, 300000)
            narration_parts.append(f"{service['name']} (Project)")
        
        total_amount += amount
        
        # Determine income ledger based on service type
        if "Consulting" in service["name"]:
            income_ledger = "IT Consulting Income"
        elif "Development" in service["name"]:
            income_ledger = "Software Development Income"
        elif "Support" in service["name"]:
            income_ledger = "Maintenance & Support Income"
        elif "Cloud" in service["name"]:
            income_ledger = "Cloud Services Income"
        else:
            income_ledger = "Software Development Income"
        
        entries.append({
            "name": income_ledger,
            "amount": -amount,
            "sac": service["sac"]
        })
    
    # Calculate GST
    gst = calculate_gst(total_amount, 18, is_interstate_flag)
    
    if gst["igst"] > 0:
        entries.append({"name": "IGST Output", "amount": -gst["igst"]})
    else:
        entries.append({"name": "CGST Output", "amount": -gst["cgst"]})
        entries.append({"name": "SGST Output", "amount": -gst["sgst"]})
    
    # Client entry (Debit)
    total_with_gst = total_amount + gst["igst"] + gst["cgst"] + gst["sgst"]
    entries.append({
        "name": client["name"],
        "amount": total_with_gst
    })
    
    narration = f"Service invoice to {client['name']}: {', '.join(narration_parts)}"
    
    return create_voucher_element("Sales", date, voucher_num, entries, narration)

def generate_purchase_voucher(date, voucher_num):
    """Generate a Purchase voucher (vendor bills)"""
    vendor = random.choice(VENDORS)
    is_interstate_flag = is_interstate(STATE, vendor["state"])
    
    # Vendor-specific expenses
    if "AWS" in vendor["name"]:
        expense = "Cloud Infrastructure Charges"
        amount = random.randint(30000, 150000)
        narration = f"AWS cloud services - monthly bill"
    elif "Microsoft" in vendor["name"]:
        expense = "Software License Fees"
        amount = random.randint(50000, 200000)
        narration = f"Microsoft licenses (Office 365, Azure)"
    elif "Google" in vendor["name"]:
        expense = "Cloud Infrastructure Charges"
        amount = random.randint(25000, 100000)
        narration = f"Google Cloud Platform services"
    else:
        expense = "Office Expenses"
        amount = random.randint(5000, 20000)
        narration = f"Office supplies purchase"
    
    entries = []
    
    entries.append({
        "name": expense,
        "amount": amount
    })
    
    # Calculate GST
    gst = calculate_gst(amount, 18, is_interstate_flag)
    
    if gst["igst"] > 0:
        entries.append({"name": "IGST Input", "amount": gst["igst"]})
    else:
        entries.append({"name": "CGST Input", "amount": gst["cgst"]})
        entries.append({"name": "SGST Input", "amount": gst["sgst"]})
    
    # Vendor entry (Credit)
    total_with_gst = amount + gst["igst"] + gst["cgst"] + gst["sgst"]
    entries.append({
        "name": vendor["name"],
        "amount": -total_with_gst
    })
    
    return create_voucher_element("Purchase", date, voucher_num, entries, narration)

def generate_payment_voucher(date, voucher_num):
    """Generate a Payment voucher"""
    bank = random.choice(BANKS)
    
    payment_types = [
        ("Salary - Technical Staff", random.randint(200000, 500000), "Monthly salary payment"),
        ("Salary - Admin Staff", random.randint(80000, 150000), "Admin staff salary"),
        ("Office Rent", random.randint(80000, 120000), "Monthly office rent"),
        ("Electricity & Water", random.randint(15000, 30000), "Utility bills"),
        ("Internet & Telecom", random.randint(10000, 20000), "Internet and phone charges"),
        ("Professional Fees", random.randint(25000, 50000), "CA/Legal fees"),
        ("Travel Expenses", random.randint(15000, 40000), "Client visit expenses"),
        ("Training & Development", random.randint(20000, 60000), "Employee training"),
    ]
    
    expense, amount, narration = random.choice(payment_types)
    
    entries = [
        {"name": expense, "amount": amount},
        {"name": bank, "amount": -amount}
    ]
    
    return create_voucher_element("Payment", date, voucher_num, entries, narration)

def generate_receipt_voucher(date, voucher_num):
    """Generate a Receipt voucher"""
    bank = random.choice(BANKS)
    amount = random.randint(5000, 50000)
    
    receipt_types = [
        ("Interest Income", "Interest received from bank"),
    ]
    
    income, narration = random.choice(receipt_types)
    
    entries = [
        {"name": bank, "amount": amount},
        {"name": income, "amount": -amount}
    ]
    
    return create_voucher_element("Receipt", date, voucher_num, entries, narration)

def generate_contra_voucher(date, voucher_num):
    """Generate a Contra voucher"""
    bank = random.choice(BANKS)
    amount = random.randint(20000, 100000)
    
    if random.random() > 0.5:
        entries = [
            {"name": bank, "amount": amount},
            {"name": "Cash", "amount": -amount}
        ]
        narration = f"Cash deposited to {bank}"
    else:
        entries = [
            {"name": "Cash", "amount": amount},
            {"name": bank, "amount": -amount}
        ]
        narration = f"Cash withdrawn from {bank}"
    
    return create_voucher_element("Contra", date, voucher_num, entries, narration)

def generate_journal_voucher(date, voucher_num):
    """Generate a Journal voucher"""
    amount = random.randint(5000, 25000)
    
    journal_types = [
        ("Depreciation", "Depreciation on assets", "Depreciation", "Office Equipment"),
        ("Round Off", "Round off adjustment", "Round Off", "Office Expenses"),
    ]
    
    j_type, narration, debit_ledger, credit_ledger = random.choice(journal_types)
    
    entries = [
        {"name": debit_ledger, "amount": amount},
        {"name": credit_ledger, "amount": -amount}
    ]
    
    return create_voucher_element("Journal", date, voucher_num, entries, narration)

def generate_all_vouchers():
    """Generate all vouchers"""
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
    
    dates = get_date_range()
    voucher_counters = {
        "Sales": 1, "Purchase": 1, "Payment": 1,
        "Receipt": 1, "Contra": 1, "Journal": 1,
    }
    
    total_vouchers = 0
    
    for date in dates:
        # Services company: 3-5 vouchers per day (less than trading)
        num_vouchers = random.randint(3, 5)
        
        for _ in range(num_vouchers):
            voucher_type = random.choices(
                ["Sales", "Purchase", "Payment", "Receipt", "Contra", "Journal"],
                weights=[40, 20, 20, 8, 7, 5]
            )[0]
            
            voucher_num = voucher_counters[voucher_type]
            voucher_counters[voucher_type] += 1
            
            if voucher_type == "Sales":
                voucher = generate_service_invoice(date, voucher_num)
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
    print("Generating Tally Prime vouchers for Services Company...")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    
    envelope, total = generate_all_vouchers()
    
    xml_string = prettify(envelope)
    
    output_file = "vouchers.xml"
    with open(output_file, "wb") as f:
        f.write(xml_string.encode('utf-8'))
    
    print(f"✓ Generated {total} vouchers")
    print(f"✓ Saved to {output_file}")
    print(f"✓ File size: {len(xml_string) / 1024:.2f} KB")
