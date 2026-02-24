# Tally Prime Data Import Guide

Complete step-by-step instructions for importing test data into Tally Prime Silver.

## 📖 Pre-requisites

- Tally Prime Silver or Gold (any recent version)
- Administrator access to Tally
- Backup of existing data (if any)
- The XML files from this repository

## 🔄 Import Process

### Step 1: Create New Company (Recommended)

1. Open Tally Prime
2. Press **Alt+F3** (Company Info) or click **Company** → **Create Company**
3. Fill in company details:
   - **Name**: e.g., "Test Trading Company"
   - **Mailing Name**: As you want it to appear
   - **Address**: Any test address
   - **State**: Select appropriate state
   - **Pin Code**: Any 6-digit code
   - **Financial Year From**: 1st April 2022 (to include FY 2022-23)
   - **Books Beginning From**: 1st April 2022
4. Enable GST features when prompted:
   - **Enable GST?**: Yes
   - **Registration Type**: Regular
   - **GSTIN/UIN**: Enter the GSTIN from the company data
   - **State**: Select same as company location
5. Press **Enter** to save

### Step 2: Import Masters

1. From **Gateway of Tally**, press **Alt+I** (Import) or go to:
   - **Import/Export** → **Import Data** → **Masters**

2. In the Import screen:
   - **File Type**: Select "XML"
   - **File Path**: Browse to `masters.xml` file
   - **Import Method**: "Merge with existing data" (or "Overwrite" for fresh company)

3. Configure import settings:
   ```
   Import Method: Merge
   Target Location: Current Company
   Allow duplicates: No
   Skip on error: No
   ```

4. Press **Enter** to start import

5. Tally will show import preview:
   - Review the count of ledgers, stock items, etc.
   - Check for any warnings

6. Press **Enter** to confirm import

7. Wait for import completion:
   - Progress bar will show status
   - Import log will display any errors

### Step 3: Verify Masters

After import, verify the data:

1. **Check Ledgers**:
   - Gateway of Tally → Accounts Info → Ledgers → Display
   - Verify count matches expected (see README)
   - Check a few sample ledgers

2. **Check Stock Items**:
   - Gateway of Tally → Inventory Info → Stock Items → Display
   - Verify HSN codes are populated
   - Check tax rates

3. **Check GST Details**:
   - Gateway of Tally → Display → Statutory Reports → GST
   - Verify GSTIN is set correctly

### Step 4: Import Vouchers (Transactions)

1. From **Gateway of Tally**:
   - **Import/Export** → **Import Data** → **Transactions**

2. Select voucher import:
   - **File Type**: XML
   - **File Path**: Browse to `vouchers.xml`
   - **Import Method**: "Merge with existing data"

3. Configure voucher import:
   ```
   Import Method: Merge
   Target Location: Current Company
   Date range: (leave blank for all)
   Voucher types: All
   Skip duplicates: Yes (recommended)
   ```

4. Press **Enter** to start

5. Review import summary:
   - Total vouchers to import
   - Vouchers by type (Sales, Purchase, etc.)
   - Any validation warnings

6. Confirm and complete import

### Step 5: Post-Import Verification

1. **Check Trial Balance**:
   - Gateway of Tally → Display → Trial Balance
   - Ensure it tallies (Debit = Credit)
   - Check for any suspense accounts

2. **Verify Key Reports**:
   - **Profit & Loss**: Should show 3 years of data
   - **Balance Sheet**: Should balance
   - **GST Reports**: GSTR-1, GSTR-3B summaries
   - **Stock Summary**: For trading/manufacturing companies

3. **Sample Voucher Check**:
   - Display → Vouchers
   - Check vouchers from different months
   - Verify GST calculations
   - Check bill-wise references

## ⚠️ Troubleshooting

### Common Import Errors

#### 1. "Ledger does not exist" Error
**Cause**: Masters not imported or voucher references wrong ledger name

**Solution**:
- Import masters.xml first
- Check ledger names match exactly (case-sensitive)
- Verify no special characters in names

#### 2. "Invalid GSTIN" Error
**Cause**: GSTIN format incorrect or state mismatch

**Solution**:
- Verify GSTIN follows format: 2-digit state code + 10-char PAN + 1-digit entity + Z + 1-digit checksum
- Ensure state in company matches first 2 digits of GSTIN

#### 3. "Date out of range" Error
**Cause**: Voucher date before books beginning date

**Solution**:
- Check company's "Books Beginning From" date
- Should be 1st April 2022 or earlier for this data
- Modify in Company Info (Alt+F3 → Alter)

#### 4. "Duplicate entry" Error
**Cause**: Voucher with same reference already exists

**Solution**:
- Use "Skip duplicates: Yes" option
- Or import into fresh company
- Check for duplicate bill numbers in source data

#### 5. "XML parsing error" Error
**Cause**: Corrupted XML file or encoding issue

**Solution**:
- Verify file is UTF-8 encoded
- Check for special characters in data
- Re-download the XML file
- Open in text editor to verify structure

#### 6. Import Slow or Hanging
**Cause**: Large file size or system resources

**Solution**:
- Close other applications
- Import in batches (by month if needed)
- Ensure adequate RAM (4GB+ recommended)
- Use SSD for faster I/O

### Data Validation Issues

#### Trial Balance Not Tallied
**Check**:
- All vouchers imported successfully
- No entries in Suspense account
- Opening balances are correct
- Round-off differences (should be minimal)

#### Missing Stock Data
**Check**:
- Stock items imported before vouchers
- Godowns created (for manufacturing company)
- Units of measure defined
- Inventory vouchers have both accounting and inventory entries

#### GST Reports Showing Errors
**Check**:
- GSTIN correctly set in company
- Tax rates assigned to stock items
- HSN/SAC codes populated
- Inter-state vs intra-state correctly identified

## 🔍 Data Quality Checks

### After Import, Verify:

1. **Ledger Count**:
   - Trading: ~45 ledgers
   - Manufacturing: ~60 ledgers
   - Services: ~35 ledgers

2. **Voucher Count** (approximate):
   - Trading: ~7,200 vouchers
   - Manufacturing: ~5,400 vouchers
   - Services: ~3,600 vouchers

3. **Date Range**:
   - Earliest voucher: April 2022 or later
   - Latest voucher: December 2025

4. **GST Compliance**:
   - All taxable supplies have GST
   - Correct CGST/SGST for intra-state
   - Correct IGST for inter-state
   - Tax amounts calculate correctly

5. **Stock Validation** (for trading/manufacturing):
   - Closing stock matches purchases minus sales
   - No negative stock
   - Godown transfers recorded (manufacturing)

## 📊 Expected Results

### Trading Company
- **Total Assets**: Should balance with Liabilities + Equity
- **Profit Trend**: Realistic trading margins (8-15%)
- **GST Liability**: Properly calculated on sales
- **Stock Value**: Matches physical stock expected

### Manufacturing Company
- **Production Cost**: Raw material + Direct expenses
- **WIP Valuation**: Work-in-progress tracked
- **Finished Goods**: Properly valued
- **Multiple Godowns**: Stock tracked across locations

### Services Company
- **Service Income**: Primary revenue source
- **Project-wise**: Costs tracked by cost centers
- **Lower Inventory**: Minimal stock items
- **Higher Margins**: Typical for services (20-40%)

## 🎯 Testing Scenarios

Use this data to test:

1. **GST Reporting**:
   - GSTR-1 (Sales returns)
   - GSTR-3B (Summary returns)
   - GSTR-2A/2B reconciliation

2. **Financial Analysis**:
   - Ratio analysis
   - Trend analysis
   - Budget vs Actual (if budgets created)

3. **Inventory Management**:
   - Stock aging
   - Movement analysis
   - Godown transfers

4. **Bank Reconciliation**:
   - Match bank vouchers with statements
   - Identify unpresented checks

5. **Audit Trail**:
   - Voucher verification
   - Change logs
   - User-wise reports

## 💡 Tips

1. **Import in Test Company First**: Always test import in a dummy company before production

2. **Keep Backups**: Export company data before and after import

3. **Check Logs**: Tally maintains import logs - review them for warnings

4. **Batch Imports**: For very large datasets, import month-by-month

5. **Verify Samples**: Don't verify everything - check random samples from different periods

6. **Use Filters**: Use date ranges and ledger filters to verify specific data subsets

## 📞 Need Help?

If you encounter issues:

1. Check Tally Prime version (update if needed)
2. Verify XML file integrity
3. Review import logs carefully
4. Check Tally help documentation
5. Test with smaller data subset first

---

**Last Updated**: February 2026  
**Tested On**: Tally Prime Silver v1.0 - v6.0  
**Compatibility**: Windows 10/11, Tally Prime all recent versions
