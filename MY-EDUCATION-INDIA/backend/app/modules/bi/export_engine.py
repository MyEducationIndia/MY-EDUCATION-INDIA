"""
Module 18: Data Export Engine
"""
import io
import csv
import json
from typing import List, Dict, Any

class DataExportEngine:
    @staticmethod
    def to_csv_string(records: List[Dict[str, Any]]) -> str:
        if not records:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue()

    @staticmethod
    def to_json_string(records: List[Dict[str, Any]]) -> str:
        return json.dumps(records, default=str, indent=2)
