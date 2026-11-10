import re
from typing import Any, Dict


class CertificatePDFCompiler:
    """Interpolates dynamic placeholders into certificate template markup and compiles print-ready HTML/PDF."""

    @staticmethod
    def interpolate_placeholders(template_html: str, data: Dict[str, Any]) -> str:
        output = template_html
        for key, val in data.items():
            pattern = re.compile(rf"\{{\{{\s*{key}\s*\}}\}}", re.IGNORECASE)
            output = pattern.sub(str(val), output)
        return output

    @staticmethod
    def inject_print_css(interpolated_html: str, css_styles: str, orientation: str = "LANDSCAPE") -> str:
        page_rule = f"@page {{ size: {orientation.lower()}; margin: 0; }}"
        wrapped_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{page_rule}
body {{ margin: 0; padding: 0; font-family: 'Helvetica Neue', Arial, sans-serif; }}
{css_styles}
</style>
</head>
<body>
{interpolated_html}
</body>
</html>"""
        return wrapped_html
