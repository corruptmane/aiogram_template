from src.core.models import dto


async def main_menu_getter(user: dto.User, **_) -> dict:
    return {
        'full_name': user.full_name,
    }
