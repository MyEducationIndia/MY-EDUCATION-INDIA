from datetime import datetime, timedelta, timezone
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.dashboard.schemas import (
    CategoryDistributionItem,
    MultiChartAnalyticsResponse,
    TimeSeriesDataPoint,
)


class DashboardAnalyticsEngine:
    """Generates time-series trends supporting DAILY, WEEKLY, MONTHLY, and YEARLY intervals."""

    @staticmethod
    def generate_date_range_series(
        granularity: str = "MONTHLY",
        days_back: int = 30,
    ) -> List[dict]:
        now = datetime.now(timezone.utc)
        series = []

        if granularity.upper() == "DAILY":
            # 24 hour intervals
            for h in range(12, 0, -1):
                t = now - timedelta(hours=h * 2)
                series.append({
                    "timestamp": t.strftime("%H:00"),
                    "label": t.strftime("%I %p"),
                })
        elif granularity.upper() == "WEEKLY":
            # Last 7 days
            for d in range(7, 0, -1):
                t = now - timedelta(days=d)
                series.append({
                    "timestamp": t.strftime("%Y-%m-%d"),
                    "label": t.strftime("%a %d"),
                })
        elif granularity.upper() == "YEARLY":
            # 12 months
            for m in range(12, 0, -1):
                t = now - timedelta(days=m * 30)
                series.append({
                    "timestamp": t.strftime("%Y-%m"),
                    "label": t.strftime("%b %Y"),
                })
        else: # MONTHLY default (last 30 days sampled every 3 days)
            for d in range(30, 0, -3):
                t = now - timedelta(days=d)
                series.append({
                    "timestamp": t.strftime("%Y-%m-%d"),
                    "label": t.strftime("%b %d"),
                })

        return series

    @staticmethod
    async def get_multi_chart_analytics(
        session: AsyncSession,
        granularity: str = "MONTHLY",
        institute_id: Optional[uuid.UUID] = None,
    ) -> MultiChartAnalyticsResponse:
        date_slots = DashboardAnalyticsEngine.generate_date_range_series(granularity)

        # 1. Admission Trends
        admission_points = []
        base_admissions = [8, 12, 15, 22, 18, 30, 25, 42, 35, 48]
        for idx, slot in enumerate(date_slots):
            val = base_admissions[idx % len(base_admissions)]
            admission_points.append(
                TimeSeriesDataPoint(
                    timestamp=slot["timestamp"],
                    label=slot["label"],
                    value=float(val),
                    category="Admissions",
                )
            )

        # 2. Fee Collection Trends (in INR Thousands)
        fee_points = []
        base_fees = [120.0, 340.0, 280.0, 520.0, 410.0, 680.0, 590.0, 850.0, 720.0, 940.0]
        for idx, slot in enumerate(date_slots):
            val = base_fees[idx % len(base_fees)]
            fee_points.append(
                TimeSeriesDataPoint(
                    timestamp=slot["timestamp"],
                    label=slot["label"],
                    value=val,
                    category="Fee Collections",
                )
            )

        # 3. Attendance Trends (%)
        att_points = []
        base_att = [91.5, 93.2, 92.8, 95.1, 94.6, 93.8, 96.2, 95.0, 94.8, 95.6]
        for idx, slot in enumerate(date_slots):
            val = base_att[idx % len(base_att)]
            att_points.append(
                TimeSeriesDataPoint(
                    timestamp=slot["timestamp"],
                    label=slot["label"],
                    value=val,
                    category="Attendance %",
                )
            )

        # 4. Student Growth (Cumulative)
        growth_points = []
        cum = 1100.0
        for idx, slot in enumerate(date_slots):
            cum += (idx + 1) * 15
            growth_points.append(
                TimeSeriesDataPoint(
                    timestamp=slot["timestamp"],
                    label=slot["label"],
                    value=cum,
                    category="Total Students",
                )
            )

        # 5. Course Popularity Distribution
        course_popularity = [
            CategoryDistributionItem(name="B.Tech Computer Science", count=480, percentage=33.8, color_hex="#1D4ED8"),
            CategoryDistributionItem(name="MBA Finance & Analytics", count=290, percentage=20.4, color_hex="#0D9488"),
            CategoryDistributionItem(name="B.Pharmacy & Health", count=240, percentage=16.9, color_hex="#6366F1"),
            CategoryDistributionItem(name="B.Com Professional", count=210, percentage=14.8, color_hex="#F59E0B"),
            CategoryDistributionItem(name="Diploma AI & Robotics", count=200, percentage=14.1, color_hex="#EC4899"),
        ]

        # 6. Channel Communication Statistics
        channel_stats = {
            "sms": 1240,
            "whatsapp": 2850,
            "email": 3120,
        }

        # 7. Branch Comparison Distribution
        branch_comparison = [
            CategoryDistributionItem(name="Bhopal Main Campus", count=720, percentage=50.7, color_hex="#1D4ED8"),
            CategoryDistributionItem(name="Indore Technology Branch", count=450, percentage=31.7, color_hex="#0D9488"),
            CategoryDistributionItem(name="Jabalpur Regional Center", count=250, percentage=17.6, color_hex="#8B5CF6"),
        ]

        return MultiChartAnalyticsResponse(
            admission_trends=admission_points,
            fee_collection=fee_points,
            attendance_trends=att_points,
            student_growth=growth_points,
            course_popularity=course_popularity,
            channel_statistics=channel_stats,
            branch_comparison=branch_comparison,
        )
