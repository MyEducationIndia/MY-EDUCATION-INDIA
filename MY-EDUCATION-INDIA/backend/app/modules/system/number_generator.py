import re
from datetime import datetime, timezone
from typing import Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.system.models import NumberGenerator, NumberSequence
from app.modules.system.validators import validate_format_template


class UniversalNumberGeneratorService:
    """Production Universal Number Generator Service.

    Guarantees atomic, gapless sequence progression and configurable token formatting
    for all ERP entities (Students, Employees, Invoices, Certificates, etc.).
    """

    @staticmethod
    def render_preview(
        format_template: str,
        prefix: Optional[str] = "MEI",
        suffix: Optional[str] = None,
        separator: str = "-",
        padding_length: int = 6,
        sample_number: int = 1,
        institute_code: str = "MEI",
        branch_code: str = "BPL",
        course_code: str = "BTECH",
        dept_code: str = "CSE",
        year: int = 2027,
        month: int = 6,
    ) -> str:
        validate_format_template(format_template)

        formatted_number = str(sample_number).zfill(padding_length)
        formatted_month = str(month).zfill(2)

        mapping = {
            "{PREFIX}": prefix or "",
            "{SUFFIX}": suffix or "",
            "{INSTITUTE}": institute_code,
            "{BRANCH}": branch_code,
            "{COURSE}": course_code,
            "{DEPT}": dept_code,
            "{YEAR}": str(year),
            "{MONTH}": formatted_month,
            "{NUMBER}": formatted_number,
        }

        rendered = format_template
        for token, val in mapping.items():
            rendered = rendered.replace(token, val)

        # Clean redundant duplicate separators if any token was empty
        if separator:
            sep_escaped = re.escape(separator)
            rendered = re.sub(f"{sep_escaped}+", separator, rendered).strip(separator)

        return rendered

    @staticmethod
    async def generate_next_number(
        session: AsyncSession,
        generator: NumberGenerator,
        institute_code: str,
        branch_code: Optional[str] = None,
        course_code: Optional[str] = None,
        dept_code: Optional[str] = None,
        academic_year_code: Optional[str] = None,
        financial_year_code: Optional[str] = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        current_year = now.year
        current_month = now.month

        # Determine Scope Key based on generator's reset rule
        rule = generator.reset_rule.upper()
        if rule == "YEARLY":
            scope_key = str(current_year)
        elif rule == "MONTHLY":
            scope_key = f"{current_year}_{current_month:02d}"
        elif rule == "ACADEMIC_YEAR":
            scope_key = academic_year_code or str(current_year)
        elif rule == "FINANCIAL_YEAR":
            scope_key = financial_year_code or str(current_year)
        elif rule == "BRANCH":
            scope_key = branch_code or "MAIN"
        else:
            scope_key = "GLOBAL"

        # Lock sequence row using SELECT ... FOR UPDATE for atomic increment
        stmt = (
            select(NumberSequence)
            .where(
                NumberSequence.generator_id == generator.id,
                NumberSequence.scope_key == scope_key,
            )
            .with_for_update()
        )
        res = await session.execute(stmt)
        seq_record = res.scalar_one_or_none()

        if not seq_record:
            seq_record = NumberSequence(
                generator_id=generator.id,
                scope_key=scope_key,
                current_number=0,
            )
            session.add(seq_record)

        seq_record.current_number += 1
        issued_number = seq_record.current_number

        rendered_number = UniversalNumberGeneratorService.render_preview(
            format_template=generator.format_template,
            prefix=generator.prefix,
            suffix=generator.suffix,
            separator=generator.separator,
            padding_length=generator.padding_length,
            sample_number=issued_number,
            institute_code=institute_code,
            branch_code=branch_code or "HQ",
            course_code=course_code or "GEN",
            dept_code=dept_code or "ADM",
            year=current_year,
            month=current_month,
        )

        seq_record.last_issued_value = rendered_number
        seq_record.last_issued_at = now
        await session.flush()

        return rendered_number
