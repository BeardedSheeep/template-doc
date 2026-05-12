from template_doc.settings import get_settings


def main() -> None:
    settings = get_settings()
    print(f"{settings.app_name} [{settings.environment}]")
