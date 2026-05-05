from abc import ABC, abstractmethod
from json import JSONDecodeError
from pydantic import BaseModel, Field, ValidationError, model_validator


class ConfigError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Config Error: {msg}")


class ConfigFileError(ConfigError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Config File Error: {msg}")


class ConfigJSONError(ConfigError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Config Json Error: {msg}")


class Config(BaseModel):
    highscore_filename: str = Field(
        default="leaderboard.json",
        description="Leaderboard input/output source",
    )
    level: list[dict[str, int]] = Field(
        default=[{"width": 20, "height": 20}] * 10,
        description="List of levels dimensions (width,height)",
    )
    lives: int = Field(
        ge=1, default=20, description="Number of lives of the player"
    )
    pacgum_points: int = Field(
        ge=0, default=10, description="Points earned for each pacgum eaten"
    )
    super_pacgum_points: int = Field(
        ge=0, default=50, description="Points earned for each super-pacgum"
    )
    ghost_points: int = Field(
        ge=0, default=200, description="Points earned for each ghost eatten"
    )
    seed: str = Field(
        default="forty-two",
        description="Seed on which the random generation is based",
    )
    max_time: int = Field(
        ge=1, default=90, description="Max duration of each level"
    )
    signature: str = Field(
        default="",
        description="Signature of the config (automatically generated)",
    )

    @model_validator(mode="after")
    def validate_data(self) -> "Config":
        """Validate the data more precisely after setting variables"""
        import hashlib

        # Verify there is enough levels
        if len(self.level) < 10:
            raise ConfigError("Not enough levels in config(must be >= 10)")

        # Create signature
        signature_str = (
            f"{self.lives}{self.pacgum_points}{self.super_pacgum_points}"
            f"{self.ghost_points}{self.seed}{self.max_time}"
        )
        for i in range(len(self.level)):
            signature_str = (
                signature_str
                + str(self.level[i]["width"])
                + str(self.level[i]["height"])
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
    def warn_missing_key(key: str) -> None:
        print(
            f"[Warning] No value set for {key} in your config. "
            "Continuing with default values."
        )

    @staticmethod
    def warn_invalid_key(key: str) -> None:
        print(
            f"[Warning] Invalid value for {key} in your config. "
            "Continuing with default values."
        )

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
        for param in [
            "highscore_filename",
            "level",
            "lives",
            "pacgum_points",
            "super_pacgum_points",
            "ghost_points",
            "seed",
            "max_time",
        ]:
            if isinstance(data, dict) and param not in data.keys():
                print(
                    f"[Warning] No value set for {param} in your config."
                    f"Continuing with default values."
                )

        # Verify every data type. Remove it if invalid
        # int
        for param in [
            "lives",
            "pacgum_points",
            "super_pacgum_points",
            "ghost_points",
            "max_time",
        ]:
            if param in data.keys() and type(data[param]) is not int:
                data.pop(param)  # remove item if not valid
                ConfigLoader.warn_invalid_key(param)
        # string
        for param in ["highscore_filename", "seed"]:
            if param in data.keys() and type(data[param]) is not str:
                data.pop(param)  # remove item if not valid
                ConfigLoader.warn_invalid_key(param)

        # Verify 'level' key validity. Remove it if invalid
        if "level" in data.keys():
            if type(data["level"]) is not list:
                ConfigLoader.warn_missing_key("level")
                data.pop("level")
        if "level" in data.keys():
            for lvl in data["level"]:
                if (
                    type(lvl) is not dict
                    or "width" not in lvl.keys()
                    or "height" not in lvl.keys()
                ):
                    print(
                        "[Warning] Removed an invalid " "level in your config."
                    )
                    ConfigLoader.warn_invalid_key("level")
                    data.pop("level")
                    data["level"].remove(lvl)
                else:
                    if (
                        type(lvl["width"]) is not int
                        or lvl["width"] < 1
                        or lvl["width"] > 50
                        or type(lvl["height"]) is not int
                        or lvl["height"] < 1
                        or lvl["height"] > 50
                    ):
                        print(
                            "[Warning] Removed an invalid "
                            "level in your config."
                        )
                        data["level"].remove(lvl)
        if "level" in data.keys():
            if len(data["level"]) < 10:
                print(
                    "[Warning] Not enough levels in config. "
                    "Using default levels."
                )
                data.pop("level")

        # Create the Config object
        try:
            config = Config(**data)
        except (ValidationError, ConfigError):
            raise ConfigJSONError("Invalid data provided in your JSON file")

        return config
