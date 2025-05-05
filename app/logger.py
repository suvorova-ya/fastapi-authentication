import logging

# Формат логов
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)

logger = logging.getLogger("auth_service")
