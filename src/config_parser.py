from pydantic import BaseModel, Field, model_validator

class ConfigError(Exception):
    pass

class ConfigParser(BaseModel):
    highscore_filename: str
    lvl_width: int = Field(ge=1, le=100)
    lvl_height: int = Field(ge=1, le=100)
    lives: int = Field(ge=1)
    pacgum_points: int = Field(ge=0)
    super_pacgum_points: int = Field(ge=0)
    ghost_points: int = Field(ge=0)
    seed: str
    max_time: int = Field(ge=1)
    signature: str = Field(default="")

    @model_validator(mode='after')
    def validate_data(self) -> "ConfigParser":
        """ Validate the data more precisely after setting variables """

        return self
