from retail_lakehouse.config.settings import settings


def check_config():
    print(f"Application: {settings.app_name}")
    print(f"Environment: {settings.app_env}")
    print(f"Data root: {settings.data_root}")
    print(f"Source: {settings.source_path}")
    print(f"Bronze: {settings.bronze_path}")
    print(f"Silver: {settings.silver_path}")
    print(f"Gold: {settings.gold_path}")

    print("\nDataset configuration:")
    print(f"Customers: {settings.customer_count}")
    print(f"Products: {settings.product_count}")
    print(f"Orders: {settings.order_count}")

    settings.create_directories()

    print("\nProject directories created successfully.")
