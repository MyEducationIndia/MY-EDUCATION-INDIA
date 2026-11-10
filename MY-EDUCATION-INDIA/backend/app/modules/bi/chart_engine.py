"""
Module 18: Apache ECharts Option Builder
"""
from typing import List, Dict, Any

class EChartsOptionBuilder:
    @staticmethod
    def build_bar_chart(title: str, categories: List[str], series_data: List[float]) -> Dict[str, Any]:
        return {
            "title": {"text": title},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": categories},
            "yAxis": {"type": "value"},
            "series": [{"data": series_data, "type": "bar", "itemStyle": {"color": "#4f46e5"}}]
        }

    @staticmethod
    def build_pie_chart(title: str, data_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "title": {"text": title, "left": "center"},
            "tooltip": {"trigger": "item"},
            "series": [{
                "type": "pie",
                "radius": "60%",
                "data": data_pairs,
                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}}
            }]
        }
