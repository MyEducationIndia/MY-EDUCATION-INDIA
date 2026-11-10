"""
Module 18: Universal Report Query Engine
"""
from typing import List, Dict, Any

class UniversalReportQueryEngine:
    @staticmethod
    def apply_in_memory_filters(records: List[Dict], filters: List[Dict]) -> List[Dict]:
        filtered = records
        for f in filters:
            field = f.get("field")
            op = f.get("op", "==")
            val = f.get("value")
            if op == "==":
                filtered = [r for r in filtered if r.get(field) == val]
            elif op == "!=":
                filtered = [r for r in filtered if r.get(field) != val]
            elif op == ">":
                filtered = [r for r in filtered if (r.get(field) or 0) > val]
            elif op == "<":
                filtered = [r for r in filtered if (r.get(field) or 0) < val]
            elif op == "in":
                filtered = [r for r in filtered if r.get(field) in val]
        return filtered

    @staticmethod
    def aggregate_field(records: List[Dict], field: str, func_name: str) -> float:
        vals = [r.get(field, 0.0) for r in records if isinstance(r.get(field), (int, float))]
        if not vals:
            return 0.0
        if func_name.upper() == "SUM":
            return round(sum(vals), 2)
        elif func_name.upper() == "AVG":
            return round(sum(vals) / len(vals), 2)
        elif func_name.upper() == "COUNT":
            return float(len(vals))
        elif func_name.upper() == "MAX":
            return max(vals)
        elif func_name.upper() == "MIN":
            return min(vals)
        return 0.0
