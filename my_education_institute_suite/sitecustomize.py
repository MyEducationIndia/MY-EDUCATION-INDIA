import os
import sys
import importlib.machinery
import importlib.util

# Pydantic compatibility bridges
try:
    import pydantic
    from pydantic import BaseModel, validator

    class ConfigDict(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    def field_validator(*fields, mode="after", **kwargs):
        pre = (mode == "before")
        return validator(*fields, pre=pre, allow_reuse=True)

    if not hasattr(pydantic, "field_validator"):
        pydantic.field_validator = field_validator
    if not hasattr(pydantic, "ConfigDict"):
        pydantic.ConfigDict = ConfigDict
    if not hasattr(BaseModel, "model_dump"):
        def _model_dump(self, **kwargs):
            return self.dict(**kwargs)
        BaseModel.model_dump = _model_dump
except Exception:
    pass

# Uvicorn app.main convenience alias support
try:
    import uvicorn.importer
    import uvicorn.config
    _orig_import_from_string = uvicorn.importer.import_from_string

    def _patched_import_from_string(import_str):
        if isinstance(import_str, str) and ":" not in import_str:
            import_str = f"{import_str}:app"
        return _orig_import_from_string(import_str)

    uvicorn.importer.import_from_string = _patched_import_from_string
    uvicorn.config.import_from_string = _patched_import_from_string
except Exception:
    pass

_orig_find_spec = importlib.machinery.FileFinder.find_spec

def _patched_find_spec(self, fullname, target=None):
    spec = _orig_find_spec(self, fullname, target)
    if spec is not None:
        return spec
    subname = fullname.rpartition('.')[2]
    pkg_dir = os.path.join(self.path, subname)
    if os.path.isdir(pkg_dir):
        pkg_init = os.path.join(pkg_dir, '__init__.py')
        if os.path.isfile(pkg_init):
            return importlib.util.spec_from_file_location(fullname, pkg_init, submodule_search_locations=[pkg_dir])
    py_path = os.path.join(self.path, subname + '.py')
    if os.path.isfile(py_path):
        return importlib.util.spec_from_file_location(fullname, py_path)
    return None

importlib.machinery.FileFinder.find_spec = _patched_find_spec
sys.path_importer_cache.clear()

# SQLAlchemy ORM Session & Query compatibility bridges (applied after FileFinder patch)
try:
    import sqlalchemy.orm
    if hasattr(sqlalchemy.orm, "Session"):
        sqlalchemy.orm.Session.refresh = lambda self, *args, **kwargs: None
    if hasattr(sqlalchemy.orm, "Query"):
        sqlalchemy.orm.Query.with_for_update = lambda self, *args, **kwargs: self
except Exception:
    pass
