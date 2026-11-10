"""Module 20: Dashboard Builder Engine"""
class DashboardBuilderEngine:
    @staticmethod
    def validate_layout_grid(grid_items: list) -> bool:
        for item in grid_items:
            w = item.get('width', 0)
            h = item.get('height', 0)
            if w <= 0 or w > 12 or h <= 0:
                return False
        return True

    @staticmethod
    def synthesize_role_dashboard(widgets: list, user_role: str) -> list:
        return [w for w in widgets if not w.get('restricted_roles') or user_role in w.get('restricted_roles')]
