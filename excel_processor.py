import re
import pandas as pd
from typing import Dict, List, Optional


class ExcelProcessor:
    """
    ExcelProcessor loads an Excel file, parses sheets into DataFrames,
    and provides utilities to analyze tables and their data.
    """

    def __init__(self):
        self.sheet_map: Dict[str, pd.DataFrame] = {}

    def load_excel(self, file_path: str):
        """Load Excel file and parse all sheets into DataFrames."""
        try:
            ext = file_path.lower().split('.')[-1]
            engine = "openpyxl" if ext == "xlsx" else "xlrd"
            xl = pd.ExcelFile(file_path, engine=engine)
            self.sheet_map = {
                sheet: xl.parse(sheet).dropna(how='all', axis=0).dropna(how='all', axis=1)
                for sheet in xl.sheet_names
            }
        except Exception as e:
            raise ValueError(f"Failed to load Excel file: {e}")

    def list_tables(self) -> List[str]:
        """Return list of sheet/table names."""
        return list(self.sheet_map.keys())

    def get_table_details(self, table_name: str, limit: int = 100, offset: int = 0) -> List[str]:
        """Return list of row names (first column) from table with pagination."""
        if table_name not in self.sheet_map:
            raise ValueError(f"Table '{table_name}' not found.")
        df = self.sheet_map[table_name]
        if df.empty:
            return []

        first_col = df.iloc[:, 0].dropna().astype(str).str.strip()
        return first_col[offset:offset + limit].tolist()

    def _extract_numeric(self, s: str) -> Optional[float]:
        """
        Extract numeric value from string supporting:
        - Currency ($1,000.50)
        - Percent (10%)
        - Scientific notation (1.23E+5)
        - Fractions (1 3/4)
        """
        if pd.isna(s):
            return None
        s = str(s).strip()

        frac_match = re.match(r"^(\d+)\s+(\d+)/(\d+)$", s)
        if frac_match:
            whole, num, denom = map(int, frac_match.groups())
            return whole + num / denom

        cleaned = re.sub(r"[$, ]", "", s)
        is_percent = False
        if cleaned.endswith("%"):
            is_percent = True
            cleaned = cleaned.rstrip("%")

        try:
            val = float(cleaned)
            return val / 100 if is_percent else val
        except ValueError:
            return None

    def row_sum(self, table_name: str, row_name: str) -> float:
        """Calculate sum of all numeric values in specified row."""
        if table_name not in self.sheet_map:
            raise ValueError(f"Table '{table_name}' not found.")
        df = self.sheet_map[table_name]
        first_col = df.iloc[:, 0].astype(str).str.strip()

        matched_rows = df[first_col == row_name]
        if matched_rows.empty:
            raise ValueError(f"Row '{row_name}' not found in table '{table_name}'.")

        row_values = matched_rows.iloc[0, 1:]
        numeric_values = [self._extract_numeric(v) for v in row_values if self._extract_numeric(v) is not None]
        return sum(numeric_values)

    def column_sum(self, table_name: str, column_name: str) -> float:
        """Calculate sum of all numeric values in specified column."""
        if table_name not in self.sheet_map:
            raise ValueError(f"Table '{table_name}' not found.")
        df = self.sheet_map[table_name]

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in table '{table_name}'.")

        col_values = df[column_name]
        numeric_values = [self._extract_numeric(v) for v in col_values if self._extract_numeric(v) is not None]
        return sum(numeric_values)
