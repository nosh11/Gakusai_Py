import os


__PROJECT_ROOT__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # プロジェクトのルートディレクトリを取得
__ASSETS_DIR__ = os.path.join(__PROJECT_ROOT__, "assets")
__RESOURCE_DIR__ = os.path.join(__PROJECT_ROOT__, "resource")
__TEMPLATE_DIR__ = os.path.join(__PROJECT_ROOT__, "template")
__USERDATA_DIR__ = os.path.join(__PROJECT_ROOT__, "userdata")


def get_user_data_dir() -> str:
    return __USERDATA_DIR__
def get_user_data_file_path(file_path: str) -> str:
    return os.path.join(__USERDATA_DIR__, file_path)
def get_asset_file_path(file_path: str) -> str:
    return os.path.join(__ASSETS_DIR__, file_path)
def get_resource_file_path(file_path: str) -> str:
    return os.path.join(__RESOURCE_DIR__, file_path)
def get_template_file_path(file_path: str) -> str:
    return os.path.join(__TEMPLATE_DIR__, file_path)
def get_project_root() -> str:
    return __PROJECT_ROOT__
def get_static_dir() -> str:
    return __ASSETS_DIR__
def get_resource_dir() -> str:
    return __RESOURCE_DIR__
def get_template_dir() -> str:
    return __TEMPLATE_DIR__
def get_file_path(file_path: str) -> str:
    if os.path.isabs(file_path):
        return file_path
    else:
        return os.path.join(__PROJECT_ROOT__, file_path)