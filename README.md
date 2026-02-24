# Tally Prime Test Data

Complete test data package for Tally Prime Silver with 3 years of realistic Indian business data across 3 different companies.

## 📦 What's Included

- **2 Companies** with different industry types (READY TO USE):
  - ✅ **Trading Company** - Wholesale electronics trader (Mumbai) - **COMPLETE**
  - ✅ **Services Company** - IT consulting firm (Bangalore) - **COMPLETE**
  
- **1 Company** (Planned for future):
  - ⏳ **Manufacturing Company** - FMCG manufacturer (Delhi) - _Coming soon_
  
- **Data Coverage**: January 2023 - December 2025 (3 years)
- **Volume**: 100-200 vouchers per month per company
- **All Voucher Types**: Sales, Purchase, Payment, Receipt, Journal, Contra
- **Complete Masters**: Ledgers, Stock Items, Cost Centers, Godowns
- **GST Compliant**: Proper GSTINs, HSN codes, tax rates (5%, 12%, 18%, 28%)
- **Real-world Data**: Includes some intentionally messy entries for testing

## 📁 Folder Structure

```
tally-prime-test-data/
├── README.md (this file)
├── IMPORT-GUIDE.md (detailed import instructions)
├── companies/
│   ├── trading-company/
│   │   ├── masters.xml (Ledgers, Stock Items, etc.)
│   │   └── vouchers.xml (All transactions)
│   ├── manufacturing-company/
│   │   ├── masters.xml
│   │   └── vouchers.xml
│   └── services-company/
│       ├── masters.xml
│       └── vouchers.xml
└── samples/
    └── sample-import-screenshots/
```

## 🚀 Quick Start

### Import Data into Tally Prime

1. **Open Tally Prime Silver**
2. Go to **Gateway of Tally** → **Import/Export** → **Import Data**
3. Select **Masters** or **Transactions** based on file type
4. Browse and select the XML file
5. Tally will show preview - verify the data
6. Press **Enter** to import
7. Check import status for any errors

### Recommended Import Order

1. Import **masters.xml** first (creates ledgers, stock items, etc.)
2. Then import **vouchers.xml** (transactions reference the masters)
3. Verify data in relevant reports

## 📊 Data Summary

### Trading Company (Electronics Wholesale)
- **Location**: Mumbai, Maharashtra
- **GSTIN**: 27AAACT1234C1Z5
- **Ledgers**: 45+ (Customers, Suppliers, Banks, Duties, Expenses)
- **Stock Items**: 30+ (Electronics items with HSN codes)
- **Vouchers**: ~7,200 (200/month × 36 months)
- **Primary Transactions**: Purchase & Sales of electronics

### Manufacturing Company (FMCG)
- **Location**: New Delhi, Delhi
- **GSTIN**: 07AAACM5678D1Z3
- **Ledgers**: 60+ (Raw materials, Finished goods, Manufacturing accounts)
- **Stock Items**: 50+ (Raw materials + Finished products)
- **Godowns**: 3 (Raw Material Store, Production Floor, Finished Goods)
- **Vouchers**: ~5,400 (150/month × 36 months)
- **Primary Transactions**: Material purchase, Production, Sales

### Services Company (IT Consulting) ✅ **COMPLETE**
- **Location**: Bangalore, Karnataka
- **GSTIN**: 29AAACS9012E1Z1
- **Ledgers**: 40+ (Service income, Client accounts, Operating expenses, Cost Centers)
- **Stock Items**: N/A (Service-based company)
- **Vouchers**: ~3,422 (Apr 2023 - Dec 2025)
- **Primary Transactions**: Service invoices, Cloud charges, Salary payments
- **Cost Centers**: 5 project-wise cost centers for tracking

## 🎯 Test Scenarios Covered

### Voucher Types
- ✅ Sales Vouchers (Local & Interstate)
- ✅ Purchase Vouchers (Local & Interstate)
- ✅ Payment Vouchers (Cash & Bank)
- ✅ Receipt Vouchers
- ✅ Journal Vouchers (Adjustments, Depreciation)
- ✅ Contra Vouchers (Cash ↔ Bank transfers)

### GST Scenarios
- ✅ Intra-state (CGST + SGST)
- ✅ Inter-state (IGST)
- ✅ Reverse Charge Mechanism (RCM)
- ✅ Exempted supplies
- ✅ Nil-rated supplies
- ✅ Different tax slabs (5%, 12%, 18%, 28%)

### Real-world Data Quirks
- ⚠️ Some vouchers with round-off differences
- ⚠️ Few entries with missing narration
- ⚠️ Some duplicate bill references (for testing validation)
- ⚠️ Date mismatches in few journal entries
- ⚠️ Ledger name variations (for testing matching)

## 📋 Import Guide

See **IMPORT-GUIDE.md** for:
- Step-by-step import instructions with screenshots
- Troubleshooting common import errors
- Data validation after import
- Tally Prime version compatibility notes

## 🔧 Technical Details

### XML Format
- **Schema**: Tally Definition Language (TDL) compatible
- **Encoding**: UTF-8
- **Root Element**: `<ENVELOPE>`
- **Version**: Tally Prime 1.0+
- **Date Format**: DDMMYYYY
- **Amount Format**: Positive for Debit, Negative for Credit (or as per Tally standard)

### Masters Included
- Ledgers (with proper groups)
- Stock Items (with HSN/SAC codes)
- Stock Groups
- Cost Centers
- Cost Categories
- Godowns (for manufacturing company)
- Units of Measure

### Transactions Included
- Voucher Type references
- Party ledgers
- Accounting entries
- Inventory entries (where applicable)
- GST tax breakdowns
- Bill-wise references

## ⚠️ Important Notes

1. **Test Environment Only**: This data is for testing/training purposes only
2. **GSTIN Format**: GSTINs used are fictional but follow proper format
3. **Backup First**: Always backup your Tally data before importing
4. **Version**: Tested with Tally Prime Silver (latest version)
5. **Data Quality**: Intentionally includes some messy data for testing validation

## 📞 Support

For issues or questions:
1. Check **IMPORT-GUIDE.md** for troubleshooting
2. Verify Tally Prime version compatibility
3. Ensure masters are imported before vouchers
4. Check XML file encoding (should be UTF-8)

## 📄 License

This test data is provided for educational and testing purposes. Free to use for:
- Software testing
- Training and education
- Demo purposes
- Development and QA

**Not for**: Commercial use, real accounting, tax filing

---

**Created**: February 2026  
**Compatible**: Tally Prime Silver & Gold  
**Data Period**: Jan 2023 - Dec 2025
