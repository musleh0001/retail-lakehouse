from functools import cached_property
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.

    Configuration priority:
    Environment variables override values from .env.
    """

    app_name: str = "retail-lakehouse"
    app_env: str = "development"
    log_level: str = "INFO"

    data_root: Path = Path("./data")

    spark_master: str = "local[*]"
    spark_app_name: str = "retail-lakehouse"

    generator_seed: int = 42

    customer_count: int = Field(default=1000, ge=1)
    product_count: int = Field(default=200, ge=1)
    order_count: int = Field(default=5000, ge=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    @cached_property
    def source_path(self) -> Path:
        return self.data_root / "source"

    @cached_property
    def bronze_path(self) -> Path:
        return self.data_root / "bronze"

    @cached_property
    def silver_path(self) -> Path:
        return self.data_root / "silver"

    @cached_property
    def gold_path(self) -> Path:
        return self.data_root / "gold"

    def create_directories(self):
        """Create all required project data directories."""

        directories = [
            self.source_path,
            self.source_path / "customers",
            self.source_path / "products",
            self.source_path / "categories",
            self.source_path / "orders",
            self.source_path / "order_items",
            self.source_path / "payments",
            self.bronze_path,
            self.silver_path,
            self.gold_path,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
