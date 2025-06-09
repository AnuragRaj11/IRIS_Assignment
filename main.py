from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse
import shutil
import tempfile
import os

from excel_processor import ExcelProcessor

app = FastAPI(title="Enhanced Excel Processor API", version="2.1")

processor = ExcelProcessor()

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    """
    Upload an Excel file (.xlsx).
    """
    try:
        suffix = os.path.splitext(file.filename)[-1]
        if suffix not in (".xls", ".xlsx"):
            raise HTTPException(status_code=400, detail="Only .xls and .xlsx files are supported.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        processor.load_excel(temp_path)

        os.remove(temp_path)  # cleanup temp file

        return {"message": "Excel file uploaded successfully", "tables": processor.list_tables()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list_tables")
def list_tables():
    """
    List all table/sheet names in the uploaded Excel file.
    """
    tables = processor.list_tables()
    if not tables:
        raise HTTPException(status_code=404, detail="No Excel file uploaded or no tables found.")
    return {"tables": tables}


@app.get("/get_table_details")
def get_table_details(
    table_name: str = Query(..., description="Name of the table/sheet"),
    limit: int = Query(100, ge=1, le=1000, description="Number of rows to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Return row names (first column values) for the specified table with pagination.
    """
    try:
        rows = processor.get_table_details(table_name, limit=limit, offset=offset)
        return {"table_name": table_name, "row_names": rows}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/row_sum")
def row_sum(
    table_name: str = Query(..., description="Name of the table/sheet"),
    row_name: str = Query(..., description="Row name (value from first column)"),
):
    """
    Calculate sum of all numeric values in the specified row.
    """
    try:
        total = processor.row_sum(table_name, row_name)
        return {"table_name": table_name, "row_name": row_name, "sum": total}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/column_sum")
def column_sum(
    table_name: str = Query(..., description="Name of the table/sheet"),
    column_name: str = Query(..., description="Column name"),
):
    """
    Calculate sum of all numeric values in the specified column.
    """
    try:
        total = processor.column_sum(table_name, column_name)
        return {"table_name": table_name, "column_name": column_name, "sum": total}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/")
def root():
    return {
        "message": "Welcome to the Enhanced Excel Processor API. Please upload an Excel file at /upload and then use the other endpoints."
    }
