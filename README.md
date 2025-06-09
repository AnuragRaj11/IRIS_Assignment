# 📊 Enhanced Excel Processor API (FastAPI)

A FastAPI application that reads and processes data from Excel sheets, providing endpoints to interact with sheet tables, rows, and columns dynamically.

---

## ✨ Features

- 📂 Upload `.xls` or `.xlsx` Excel files dynamically
- 🧾 Identify and extract tables from Excel sheets
- 🗂️ List all available table/sheet names
- 🔍 Get row names (first column values) for specific tables
- ➕ Calculate sum of numeric values in:
  - Specific rows (`/row_sum`)
  - Specific columns (`/column_sum`)
- 🧼 Robust error handling and input validation
- 🧠 Handles:
  - Scientific notation (e.g., `1.23E+5`)
  - Currency (`$1,000`)
  - Percentages (`10%`)
  - Mixed fractions (`1 3/4`)
- 📜 Pagination support for large row results
- 🚫 Graceful failure for empty/missing sheets

---

## 🚀 Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

▶️ Usage
Start the FastAPI server

bash
Copy
Edit
uvicorn main:app --reload --port 9090
Visit Docs

arduino
Copy
Edit
http://127.0.0.1:9090/docs
Upload Excel File

http
Copy
Edit
POST /upload
Form-Data: file: <your .xls or .xlsx file>
Endpoints

A. 🔗 /list_tables
http
Copy
Edit
GET /list_tables
Response:
{
  "tables": ["Sheet1", "Investment", "Revenue"]
}
B. 🔗 /get_table_details
http
Copy
Edit
GET /get_table_details?table_name=Sheet1&limit=10&offset=0
Response:
{
  "table_name": "Sheet1",
  "row_names": ["Initial Investment", "EBIT", "Net CF"]
}
C. 🔗 /row_sum
http
Copy
Edit
GET /row_sum?table_name=Sheet1&row_name=Initial Investment
Response:
{
  "table_name": "Sheet1",
  "row_name": "Initial Investment",
  "sum": 62484.0
}
D. 🔗 /column_sum
http
Copy
Edit
GET /column_sum?table_name=Sheet1&column_name=2024
Response:
{
  "table_name": "Sheet1",
  "column_name": "2024",
  "sum": 107594.50
}
🧪 Testing
To help you quickly test your application, use the following:

✅ Base URL: http://localhost:9090

✅ Postman Collection File: postman_collection.json

Import this collection in Postman to test /upload, /list_tables, /get_table_details, /row_sum, and /column_sum with ready-to-use requests.

📸 Screenshots 

File upload

Table listing

Row/Column sum API usage

Error response for invalid input

⚠️ Missed Edge Cases
Case	Description	Fix
Empty or Corrupt Excel Files	App crashes if file is missing or invalid	Validate file at upload
No Numeric Data in Row/Column	Sum fails if text-only	Return 0 or meaningful error
Trailing Spaces in Names	"Revenue " ≠ "Revenue"	.strip() all names
Very Large Files	May crash due to memory	Stream reading or chunked loading
Concurrent Requests	Race condition with shared memory	Use threading-safe storage or DB
Currency/Fraction Formats	$1,000, 1 3/4 fail without parsing	_extract_numeric() handles now
Hidden Rows/Sheets	Ignored by default	Add ?include_hidden=true flag
Special Characters in Names	May break URLs	Use URL encoding

✅ Why This Matters
These improvements and edge-case handling ensure your API is:

⚡ Fast

🧠 Smart

🧱 Robust

🤝 User-Friendly

🔁 Scalable

📌 Folder Structure
├── excel_processor.py     
├── main.py                
├── requirements.txt      
├── postman_collection.json 
└── README.md             