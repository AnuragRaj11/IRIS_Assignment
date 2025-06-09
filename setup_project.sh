#!/bin/bash

# Project directory name
PROJECT_DIR="enhanced-excel-processor-api"

echo "Creating project directory structure..."

# Create main project folder
mkdir -p $PROJECT_DIR

# Change into project directory
cd $PROJECT_DIR || exit

# Create folders
mkdir -p screenshots

# Create blank code files
touch main.py
touch excel_processor.py

# Create blank postman_collection.json
echo "{}" > postman_collection.json

# Create blank requirements.txt with minimal dependencies
cat > requirements.txt << EOL
fastapi
uvicorn[standard]
pandas
openpyxl
python-multipart
EOL

# Create README.md with improved README content
cat > README.md << 'EOL'
# 📊 Enhanced Excel Processor API (FastAPI)

A **FastAPI** application that dynamically reads, processes, and analyzes Excel (`.xls` and `.xlsx`) files, providing RESTful endpoints to interact with sheet tables, rows, and columns. This API intelligently handles complex Excel data formats and edge cases, making data extraction and numeric summarization smooth and reliable.

---

## ✨ Features

- 📂 Upload Excel files (`.xls` or `.xlsx`) dynamically via API  
- 🧾 Detect and extract tables from any Excel sheet  
- 🗂️ List all available sheets/tables in the uploaded file  
- 🔍 Retrieve row names (first column values) for any table  
- ➕ Compute sums of numeric values in:  
  - Specific rows (`/row_sum`)  
  - Specific columns (`/column_sum`)  
- 🧠 Robust parsing of complex numeric formats:  
  - Scientific notation (`1.23E+5`)  
  - Currency values (`$1,000`)  
  - Percentages (`10%`)  
  - Mixed fractions (`1 3/4`)  
- 📜 Supports pagination for large tables (`limit` and `offset` query params)  
- 🚫 Graceful handling of empty, missing, or corrupt Excel files  
- 🧼 Strong input validation and error handling  
- ⚙️ Optional inclusion of hidden sheets and rows (`?include_hidden=true`)  
- 🔄 Thread-safe file processing for concurrent requests  
- 📡 Interactive API documentation via Swagger UI  

---

## 📦 Installation

\`\`\`bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create and activate a virtual environment
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

---

## 🚀 Running the API

Start the FastAPI server:

\`\`\`bash
uvicorn main:app --reload --port 9090
\`\`\`

Open your browser and visit the interactive API docs:  
[http://127.0.0.1:9090/docs](http://127.0.0.1:9090/docs)

---

## 🔗 API Endpoints

| Endpoint             | Method | Description                                               | Query/Form Params                        |
|----------------------|--------|-----------------------------------------------------------|-----------------------------------------|
| \`/upload\`            | POST   | Upload an Excel file (.xls or .xlsx)                       | \`file\` (form-data)                      |
| \`/list_tables\`       | GET    | List all available sheet/table names                       | None                                    |
| \`/get_table_details\` | GET    | Get row names (first column values) for a sheet            | \`table_name\` (str), \`limit\` (int, opt), \`offset\` (int, opt) |
| \`/row_sum\`           | GET    | Calculate sum of numeric values in a specific row          | \`table_name\` (str), \`row_name\` (str)   |
| \`/column_sum\`        | GET    | Calculate sum of numeric values in a specific column       | \`table_name\` (str), \`column_name\` (str)|

---

## 🧪 Testing

You can quickly test all endpoints using the included Postman collection: \`postman_collection.json\`.

- Base URL: \`http://localhost:9090\`
- Import the collection and run the provided requests for uploading files, listing tables, fetching row names, and summing rows/columns.

---

## ⚠️ Handling Edge Cases

This API is designed to gracefully handle common and tricky scenarios:

- **Invalid or Corrupt Files:** Uploads are validated to prevent crashes on malformed Excel files.  
- **Empty or Non-Numeric Rows/Columns:** Summation endpoints return \`0\` or meaningful warnings when no numeric data is found.  
- **Trailing Spaces in Names:** All table and row names are trimmed to avoid mismatches caused by whitespace.  
- **Large Files:** Pagination with \`limit\` and \`offset\` parameters prevents memory overloads and improves performance.  
- **Concurrent Requests:** Thread-safe processing avoids race conditions during multiple simultaneous uploads or queries.  
- **Complex Numeric Formats:** Supports parsing of currencies (\`$1,000\`), scientific notation (\`1.23E+5\`), percentages (\`10%\`), and mixed fractions (\`1 3/4\`).  
- **Hidden Sheets and Rows:** Optionally included via \`?include_hidden=true\` query flag for thorough data access.  
- **Special Characters:** Table and row names containing special characters or emojis are sanitized and URL-encoded to prevent parsing issues.

---

## 📂 Project Structure

\`\`\`
├── excel_processor.py       # Core logic for Excel file processing
├── main.py                  # FastAPI app and endpoints
├── requirements.txt         # Python dependencies
├── postman_collection.json  # Postman collection for API testing
├── README.md                # This documentation
└── screenshots/             # Screenshots demonstrating usage and API responses
\`\`\`

---

## 🔮 Future Improvements

- Support streaming or chunked reading for very large Excel files  
- Implement caching or database-backed storage for uploaded files to improve concurrency  
- Add advanced analytics endpoints (average, median, filtering, min/max)  
- Build a frontend UI for easier interaction and visualization  
- Add automated tests for edge cases and API endpoints  

---

## 🤝 Contributions & Feedback

Contributions, bug reports, and feature requests are welcome! Feel free to open issues or submit pull requests.

EOL

echo "Project setup completed."
echo "Run 'source venv/bin/activate' (Linux/macOS) or 'venv\\Scripts\\activate' (Windows) to activate the environment."
echo "Then run 'pip install -r requirements.txt' to install dependencies."
