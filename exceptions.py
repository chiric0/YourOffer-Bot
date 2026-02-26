import sys
from config import log

def handle_exception(exc_type, exc_value, exc_traceback):
    """Обработчик необработанных исключений.

    Args:
        exc_type: Тип исключения
        exc_value: Значение исключения
        exc_traceback: Трассировка стека
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log.error("Необработанное исключение:", exc_info=(exc_type, exc_value, exc_traceback)) 