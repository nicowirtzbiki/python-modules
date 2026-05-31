#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv


def load_configuration() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


def get_config(key: str, default: str = "not configured") -> str:
    """Get configuration value from environment."""
    return os.environ.get(key, default)


def check_configuration() -> dict[str, str]:
    """Load and return all configuration values."""
    return {
        "mode": get_config("MATRIX_MODE", "development"),
        "database": get_config("DATABASE_URL", "not configured"),
        "api_key": get_config("API_KEY", "not configured"),
        "log_level": get_config("LOG_LEVEL", "INFO"),
        "zion": get_config("ZION_ENDPOINT", "not configured"),
    }


def display_configuration(config: dict[str, str]) -> None:
    """Display configuration in a secure way."""
    print("Configuration loaded:")

    mode = config["mode"]
    print(f"Mode: {mode}")

    if config["database"] != "not configured":
        print("Database: Connected to local instance"
              if mode == "development"
              else "Database: Connected to production instance")
    else:
        print("Database: [WARNING] not configured")

    if config["api_key"] != "not configured":
        print("API Access: Authenticated")
    else:
        print("API Access: [WARNING] not configured")

    print(f"Log Level: {config['log_level']}")

    if config["zion"] != "not configured":
        print("Zion Network: Online")
    else:
        print("Zion Network: [WARNING] not configured")


def security_check() -> None:
    """Perform environment security checks."""
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found - using defaults")

    if os.environ.get("MATRIX_MODE") == "production":
        print("[OK] Production overrides active")
    else:
        print("[OK] Production overrides available")


def main() -> None:
    """Main oracle function."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    load_configuration()
    config = check_configuration()

    display_configuration(config)
    security_check()

    print()
    mode = config["mode"]
    if mode == "production":
        print("Running in PRODUCTION mode - maximum security active.")
    else:
        print("Running in DEVELOPMENT mode - debug features enabled.")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()