from abc import ABC, abstractmethod
from json import JSONDecodeError
from pydantic import BaseModel, Field, ValidationError, model_validator


class ConfigError(Exception):
    pass


class ConfigFileError(ConfigError):
    pass


class ConfigJSONError(ConfigError):
    pass


class Config(BaseModel):
    highscore_filename: str = Field(default="leaderboard.json")
    lvl_width: int = Field(ge=1, le=100, default=16)
    lvl_height: int = Field(ge=1, le=100, default=10)
    lives: int = Field(ge=1, default=20)
    pacgum_points: int = Field(ge=0, default=10)
    super_pacgum_points: int = Field(ge=0, default=50)
    ghost_points: int = Field(ge=0, default=200)
    seed: str = Field(default="forty-two")
    max_time: int = Field(ge=1, default=90)
    signature: str = Field(default="")

    @model_validator(mode="after")
    def validate_data(self) -> "Config":
        """Validate the data more precisely after setting variables"""
        import hashlib

        # Create signature
        signature_str = (
            f"{self.lvl_width}{self.lvl_height}"
            f"{self.lives}{self.pacgum_points}{self.super_pacgum_points}"
            f"{self.ghost_points}{self.seed}{self.max_time}"
        )
        hash_obj = hashlib.sha256(signature_str.encode("utf-8"))
        self.signature = hash_obj.hexdigest()

        return self


class ABCConfigLoader(ABC):
    """Interface class for creating classes loading config files"""

    @staticmethod
    @abstractmethod
    def load_config(source: str) -> Config:
        """Load a Config from a given source that will be parsed"""

        pass


class ConfigLoader(ABCConfigLoader):
    """Interface of ABCConfigLoader for loading a local json file"""

    @staticmethod
    def remove_comments(input_str: str) -> str:
        """Remove the comments from a given string"""
        import re

        output_str = re.sub(
            r'("(?:\\.|[^"\\])*")|#.*',
            lambda m: m.group(1) if m.group(1) else "",
            input_str,
        )
        return output_str

    @staticmethod
    @abstractmethod
    def load_config(source: str) -> Config:
        """Load the config from the source (json file path)"""
        import json

        # Load JSON file as string
        try:
            with open(source, "r") as f:
                content = f.read()
        except (FileNotFoundError, IsADirectoryError):
            raise ConfigFileError("Configuration file not found")
        except PermissionError:
            raise ConfigFileError("You don't have rights to read this file")

        # Remove comments by removing all chars between a "#" and the next "\n"
        json_string = ConfigLoader.remove_comments(content)

        # Transform into python dict object
        try:
            data = json.loads(json_string)
        except (JSONDecodeError, UnicodeDecodeError):
            raise ConfigFileError("Invalid JSON format")

        # Print warning message for unset variables
        for item in ["highscore_filename", "lvl_width",
                     "lvl_height", "lives", "pacgum_points",
                     "super_pacgum_points", "ghost_points",
                     "seed", "max_time"]:
            if isinstance(data, dict) and item not in data.keys():
                print(f"[Warning] No value set for {item} in your config."
                      f"Continuing with default values.")

        # Create the Config object
        try:
            config = Config(**data)
        except (ValidationError, ConfigError):
            raise ConfigJSONError("Invalid data provided in your JSON file")

        return config
