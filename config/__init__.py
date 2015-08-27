from .development import DevelopmentConfig
from .testing import TestingConfig
try:
    from .production import ProductionConfig
except ImportError:
    pass