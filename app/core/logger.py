import sys
from pathlib import Path
from loguru import logger

# Cria pasta de logs se não existir
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove handlers padrão do loguru
logger.remove()

# 1. Output para o Terminal (Colorido e formatado)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 2. Output para Arquivo Rotativo em Disco (Para auditoria de compliance)
logger.add(
    LOG_DIR / "finguard.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8"
)

# Exporta a instância pronta do logger
__all__ = ["logger"]