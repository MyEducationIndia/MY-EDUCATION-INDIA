"""Module 20: Dynamic Menu Engine"""
class DynamicMenuEngine:
    @staticmethod
    def build_navigation_tree(menu_items: list, user_permissions: list) -> list:
        allowed_items = []
        for it in menu_items:
            req_perm = it.get('required_permission')
            if not req_perm or req_perm in user_permissions or 'ALL' in user_permissions:
                allowed_items.append(it)
        parents = [it for it in allowed_items if not it.get('parent_item_id')]
        for p in parents:
            p['children'] = [it for it in allowed_items if it.get('parent_item_id') == p.get('id')]
        return parents
