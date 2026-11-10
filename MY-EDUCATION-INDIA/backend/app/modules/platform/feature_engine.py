"""Module 20: Dynamic Feature Engine"""
class DynamicFeatureEngine:
    @staticmethod
    def is_module_active(module_key: str, registered_modules: list, institute_id: str) -> bool:
        for mod in registered_modules:
            if mod.get('module_key') == module_key:
                return mod.get('is_installed', True) and mod.get('is_enabled', True)
        return True
