import re
from typing import Set

ALLOWED_NUMBER_TOKENS: Set[str] = {
    "{PREFIX}",
    "{SUFFIX}",
    "{INSTITUTE}",
    "{BRANCH}",
    "{COURSE}",
    "{DEPT}",
    "{YEAR}",
    "{MONTH}",
    "{NUMBER}",
}


def validate_format_template(template: str) -> None:
    if "{NUMBER}" not in template:
        raise ValueError("Number format template must contain the running counter token '{NUMBER}'.")

    # Extract all {TOKENS}
    tokens = re.findall(r"\{[A-Z_]+\}", template)
    for tok in tokens:
        if tok not in ALLOWED_NUMBER_TOKENS:
            raise ValueError(f"Invalid format token '{tok}'. Allowed tokens: {', '.join(sorted(ALLOWED_NUMBER_TOKENS))}")


def validate_date_range(start_date, end_date) -> None:
    if start_date >= end_date:
        raise ValueError(f"Start date ({start_date}) must be strictly before end date ({end_date}).")
