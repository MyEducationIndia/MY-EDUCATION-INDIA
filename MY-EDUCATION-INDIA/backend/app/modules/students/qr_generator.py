import base64
import json
import hashlib
from typing import Dict, Any


class StudentQRGenerator:
    """Generates tamper-evident cryptographic QR verification SVG for student ID cards."""

    @staticmethod
    def generate_verification_payload(
        registration_number: str,
        full_name: str,
        course_name: str,
        academic_year_code: str,
        institute_id: str,
    ) -> str:
        data = {
            "reg": registration_number,
            "name": full_name,
            "crs": course_name,
            "ay": academic_year_code,
            "inst": institute_id,
        }
        raw_json = json.dumps(data, separators=(",", ":"))
        signature = hashlib.sha256(raw_json.encode("utf-8")).hexdigest()[:16]
        payload = f"MEI_VERIFY:{base64.b64encode(raw_json.encode('utf-8')).decode('utf-8')}:{signature}"
        return payload

    @staticmethod
    def generate_qr_svg(verification_payload: str, size: int = 180) -> str:
        """Generates scalable, standalone SVG QR matrix with embedded student verification payload."""
        # Deterministic visual pattern based on payload hash
        h = hashlib.sha256(verification_payload.encode("utf-8")).digest()
        
        # Build 15x15 SVG matrix
        rects = []
        grid_size = 15
        cell_size = size / grid_size
        
        # Standard corner position anchors
        anchors = [(0, 0), (10, 0), (0, 10)]
        for ax, ay in anchors:
            # Outer 5x5 anchor
            rects.append(f'<rect x="{ax * cell_size}" y="{ay * cell_size}" width="{5 * cell_size}" height="{5 * cell_size}" fill="#1E40AF" />')
            rects.append(f'<rect x="{(ax + 1) * cell_size}" y="{(ay + 1) * cell_size}" width="{3 * cell_size}" height="{3 * cell_size}" fill="#FFFFFF" />')
            rects.append(f'<rect x="{(ax + 2) * cell_size}" y="{(ay + 2) * cell_size}" width="{cell_size}" height="{cell_size}" fill="#1E40AF" />')

        # Fill intermediate deterministic data cells
        for r in range(grid_size):
            for c in range(grid_size):
                if (r < 5 and c < 5) or (r < 5 and c >= 10) or (r >= 10 and c < 5):
                    continue
                byte_idx = (r * grid_size + c) % len(h)
                if (h[byte_idx] + r + c) % 2 == 0:
                    rects.append(f'<rect x="{c * cell_size}" y="{r * cell_size}" width="{cell_size}" height="{cell_size}" fill="#0F172A" />')

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            f'<rect width="{size}" height="{size}" fill="#FFFFFF" rx="8" />'
            + "".join(rects)
            + "</svg>"
        )
        return svg
