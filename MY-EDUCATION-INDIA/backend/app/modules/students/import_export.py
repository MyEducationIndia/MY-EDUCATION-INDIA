import csv
import io
from typing import Any, Dict, List, Tuple


class StudentImportExportProcessor:
    """Bulk CSV/Excel importer and exporter with row-level validation."""

    EXPECTED_CSV_HEADERS: List[str] = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "date_of_birth",
        "gender",
        "course_name",
        "batch_name",
        "academic_year_code",
    ]

    @staticmethod
    def parse_csv_stream(csv_content: str) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        valid_rows = []
        errors = []
        reader = csv.DictReader(io.StringIO(csv_content))

        for row_idx, row in enumerate(reader, start=2): # Header is line 1
            missing = [h for h in StudentImportExportProcessor.EXPECTED_CSV_HEADERS if not row.get(h, "").strip()]
            if missing:
                errors.append({
                    "row": row_idx,
                    "error": f"Missing required fields: {', '.join(missing)}",
                    "data": row,
                })
                continue

            valid_rows.append({k: v.strip() for k, v in row.items()})

        return valid_rows, errors

    @staticmethod
    def generate_csv_template() -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(StudentImportExportProcessor.EXPECTED_CSV_HEADERS)
        writer.writerow([
            "Aarav",
            "Sharma",
            "aarav.sharma@example.com",
            "+919876543210",
            "2005-08-15",
            "MALE",
            "B.Tech Computer Science",
            "2026-Batch-A",
            "2026-2027",
        ])
        return output.getvalue()
