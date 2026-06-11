"""
Day 10 - Task 3: Configuration Manager
=======================================
Demonstrates JSON config files, required-key validation, safe .get() defaults,
and programmatic config updates — all critical patterns in real AI pipelines.
Connection to AI Engineering: Every production ML system (model serving,
training jobs, data pipelines) externalises its settings in a config file.
This module shows how to read, validate, update, and persist those settings.

Author: Sehar Andleeb
Internship: Xeven Solutions, Lahore — AI Engineering
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
Date: Day 10 of 30-Day AI Engineering Roadmap
"""

import json
import os
from copy import deepcopy
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants — required keys and their expected types
# ---------------------------------------------------------------------------
CONFIG_FILE = "config.json"

REQUIRED_KEYS: dict = {
    "database": dict,
    "api": dict,
    "features": dict,
}

# Default config — used when config.json does not exist yet
DEFAULT_CONFIG: dict = {
    "app": {
        "name": "XevenAI Platform",
        "version": "1.0.0",
        "environment": "development",   # development | staging | production
        "debug": True,
        "log_level": "INFO",
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "xeven_ai_db",
        "user": "admin",
        "password": "CHANGE_ME",        # placeholder — never hardcode real creds
        "pool_size": 5,
        "timeout_seconds": 30,
    },
    "api": {
        "base_url": "https://api.xeven.ai/v1",
        "key": "sk-PLACEHOLDER-KEY",   # placeholder
        "rate_limit_rpm": 60,
        "timeout_seconds": 10,
        "retry_attempts": 3,
    },
    "features": {
        "enable_caching": True,
        "enable_logging": True,
        "enable_metrics": False,
        "max_upload_mb": 50,
        "supported_languages": ["en", "ur", "ar"],
    },
    "model": {
        "default": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 1.0,
    },
}


# ---------------------------------------------------------------------------
# Core config I/O
# ---------------------------------------------------------------------------

def create_default_config(filepath: str = CONFIG_FILE) -> dict:
    """
    Write the DEFAULT_CONFIG to disk and return it.

    Args:
        filepath: Destination JSON file path.

    Returns:
        A deep copy of DEFAULT_CONFIG.
    """
    config = deepcopy(DEFAULT_CONFIG)
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=4, ensure_ascii=False)
        print(f"[INFO] Default config written to '{filepath}'.")
    except OSError as exc:
        print(f"[ERROR] Could not create config file: {exc}")
    return config


def load_config(filepath: str = CONFIG_FILE) -> dict:
    """
    Load configuration from a JSON file, falling back to defaults if missing.

    Args:
        filepath: Path to the JSON config file.

    Returns:
        Parsed config dictionary (guaranteed to be a dict).
    """
    if not os.path.exists(filepath):
        print(f"[WARN] Config file '{filepath}' not found. Creating defaults.")
        return create_default_config(filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            config = json.load(fh)
        print(f"[INFO] Config loaded from '{filepath}'.")
        return config
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Malformed JSON in '{filepath}': {exc}. Using defaults.")
        return deepcopy(DEFAULT_CONFIG)
    except OSError as exc:
        print(f"[ERROR] Cannot read '{filepath}': {exc}. Using defaults.")
        return deepcopy(DEFAULT_CONFIG)


def save_config(config: dict, filepath: str = CONFIG_FILE) -> bool:
    """
    Persist the config dictionary back to disk.

    Args:
        config: The in-memory configuration dict.
        filepath: Destination file path.

    Returns:
        True on success, False on failure.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=4, ensure_ascii=False)
        print(f"[INFO] Config saved to '{filepath}'.")
        return True
    except OSError as exc:
        print(f"[ERROR] Cannot save config: {exc}")
        return False


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_config(config: dict) -> tuple:
    """
    Check that all required top-level keys exist and are the correct type.

    Args:
        config: The config dictionary to validate.

    Returns:
        Tuple of (is_valid: bool, issues: list[str]).
        issues is an empty list when valid.
    """
    issues: list = []

    for key, expected_type in REQUIRED_KEYS.items():
        if key not in config:
            issues.append(f"Missing required key: '{key}'.")
        elif not isinstance(config[key], expected_type):
            issues.append(
                f"Key '{key}' must be {expected_type.__name__}, "
                f"got {type(config[key]).__name__}."
            )

    is_valid = len(issues) == 0
    return is_valid, issues


# ---------------------------------------------------------------------------
# Safe access helpers
# ---------------------------------------------------------------------------

def get_value(config: dict, section: str, key: str, default: Any = None) -> Any:
    """
    Safely retrieve a value from a config section using .get() chaining.

    Args:
        config: The config dictionary.
        section: Top-level section key (e.g. "database").
        key: Sub-key within the section (e.g. "port").
        default: Fallback value if section or key is absent.

    Returns:
        The stored value, or `default` if not found.
    """
    # .get() returns None (not KeyError) — O(1) both levels
    section_dict = config.get(section, {})
    return section_dict.get(key, default)


def get_feature_flag(config: dict, flag_name: str, default: bool = False) -> bool:
    """
    Retrieve a feature flag value from the 'features' section.

    Args:
        config: The config dictionary.
        flag_name: Name of the feature flag (e.g. "enable_caching").
        default: Default boolean if the flag is not found.

    Returns:
        Boolean flag value.
    """
    return bool(get_value(config, "features", flag_name, default))


# ---------------------------------------------------------------------------
# Programmatic updates
# ---------------------------------------------------------------------------

def update_config_value(
    config: dict,
    section: str,
    key: str,
    value: Any,
) -> bool:
    """
    Update a single config value and optionally create the section.

    Args:
        config: In-memory config dict (modified in-place).
        section: Target section name.
        key: Key within that section.
        value: New value to set.

    Returns:
        True on success, False if section is not a dict.
    """
    # Auto-create section if it doesn't exist
    if section not in config:
        config[section] = {}

    if not isinstance(config[section], dict):
        print(f"[ERROR] Section '{section}' is not a dict.")
        return False

    old_value = config[section].get(key, "<not set>")
    config[section][key] = value
    print(f"[INFO] config['{section}']['{key}'] updated: {old_value!r} → {value!r}.")
    return True


def switch_environment(config: dict, env: str) -> bool:
    """
    Switch the application environment and apply preset adjustments.

    Allowed environments: 'development', 'staging', 'production'.
    Production automatically: disables debug, raises log level to WARNING.

    Args:
        config: In-memory config dict.
        env: Target environment string.

    Returns:
        True on success, False for unknown environment.
    """
    valid_envs = {"development", "staging", "production"}
    if env not in valid_envs:
        print(f"[ERROR] Unknown environment '{env}'. Choose from {valid_envs}.")
        return False

    update_config_value(config, "app", "environment", env)

    if env == "production":
        update_config_value(config, "app", "debug", False)
        update_config_value(config, "app", "log_level", "WARNING")
        update_config_value(config, "features", "enable_metrics", True)
        print("[INFO] Production presets applied (debug=False, metrics=True).")
    elif env == "development":
        update_config_value(config, "app", "debug", True)
        update_config_value(config, "app", "log_level", "DEBUG")

    return True


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_config_summary(config: dict) -> None:
    """
    Pretty-print a human-readable summary of the current configuration.

    Sensitive fields (password, key) are masked.

    Args:
        config: The config dictionary.
    """
    SENSITIVE = {"password", "key"}  # fields to mask in output

    def _mask(k: str, v: Any) -> Any:
        """Mask the value if the key is sensitive."""
        if k.lower() in SENSITIVE and isinstance(v, str) and v:
            return "***" + v[-4:]  # show last 4 chars only
        return v

    print("\n" + "=" * 55)
    print(f"{'CONFIGURATION SUMMARY':^55}")
    print("=" * 55)

    for section, values in config.items():
        print(f"\n  [{section.upper()}]")
        if isinstance(values, dict):
            for k, v in values.items():
                display_v = _mask(k, v)
                print(f"    {k:<25} : {display_v}")
        else:
            print(f"    {values}")

    # Validation status
    is_valid, issues = validate_config(config)
    status_icon = "✓ VALID" if is_valid else f"✗ INVALID ({len(issues)} issue(s))"
    print(f"\n  Validation status : {status_icon}")
    if issues:
        for issue in issues:
            print(f"    • {issue}")

    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Day 10 — Configuration Manager         ║")
    print("╚══════════════════════════════════════════╝\n")

    # ── Load config (creates defaults if absent) ─────────────────────────────
    config = load_config()

    # ── Validate ─────────────────────────────────────────────────────────────
    is_valid, issues = validate_config(config)
    print(f"\n[VALIDATE] Config valid: {is_valid}")
    for issue in issues:
        print(f"  ✗ {issue}")

    # ── Safe access with defaults ─────────────────────────────────────────────
    print("\n--- Safe value access ---")
    db_port = get_value(config, "database", "port", default=5432)
    api_timeout = get_value(config, "api", "timeout_seconds", default=10)
    missing_val = get_value(config, "database", "nonexistent_key", default="N/A")
    caching_on = get_feature_flag(config, "enable_caching", default=False)

    print(f"  DB port         : {db_port}")
    print(f"  API timeout     : {api_timeout}s")
    print(f"  Missing key     : {missing_val!r}   ← .get() default")
    print(f"  Caching enabled : {caching_on}")

    # ── Programmatic updates ──────────────────────────────────────────────────
    print("\n--- Programmatic updates ---")
    update_config_value(config, "model", "temperature", 0.4)
    update_config_value(config, "model", "max_tokens", 4096)
    update_config_value(config, "features", "enable_metrics", True)
    update_config_value(config, "app", "version", "1.1.0")

    # ── Switch environment ────────────────────────────────────────────────────
    print("\n--- Switching to production ---")
    switch_environment(config, "production")

    # ── Display final summary ─────────────────────────────────────────────────
    print_config_summary(config)

    # ── Persist updated config ────────────────────────────────────────────────
    save_config(config)
    print("[DONE] configuration_manager.py complete.\n")
