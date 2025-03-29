import os

__PROJECT_ROOT__ = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
__STATIC_DIR__ = os.path.join(__PROJECT_ROOT__, "static")
__RESOURCE_DIR__ = os.path.join(__PROJECT_ROOT__, "resource")
__TEMPLATE_DIR__ = os.path.join(__PROJECT_ROOT__, "template")

def get_static_file_path(file_path: str) -> str:
    return os.path.join(__STATIC_DIR__, file_path)
def get_resource_file_path(file_path: str) -> str:
    return os.path.join(__RESOURCE_DIR__, file_path)
def get_template_file_path(file_path: str) -> str:
    return os.path.join(__TEMPLATE_DIR__, file_path)
def get_project_root() -> str:
    return __PROJECT_ROOT__
def get_static_dir() -> str:
    return __STATIC_DIR__
def get_resource_dir() -> str:
    return __RESOURCE_DIR__
def get_template_dir() -> str:
    return __TEMPLATE_DIR__
def get_file_path(file_path: str) -> str:
    if os.path.isabs(file_path):
        return file_path
    else:
        return os.path.join(__PROJECT_ROOT__, file_path)