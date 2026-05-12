from abc import abstractmethod, ABC
from pydantic import BaseModel, ValidationError, model_validator
import json


class LeaderboardError(Exception):
    """Error related to the leaderboard"""

    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Leaderboard Error: {msg}")


class LeaderboardFileError(Exception):
    """Error related to the leaderboard"""

    def __init__(self, msg: str = "") -> None:
        super().__init__(f"LeaderboardFile Error: {msg}")


class Leaderboard(BaseModel):
    """Leaderboard object containing the data of the current leaderboard"""

    signature: str
    scores: list[dict[str, str | int]]  # keys: username->str, score->int

    @model_validator(mode="after")
    def validate_data(self) -> "Leaderboard":
        """Validate input data before storing it"""
        # Check if too many scores
        if len(self.scores) > 10:
            raise LeaderboardError("Too many scores in the leaderboard")

        # Check each score
        for score in self.scores:
            # Case if one of the keys not found
            if "username" not in score.keys() or "score" not in score.keys():
                raise LeaderboardError("Invalid score")
            # Case if username is not str
            if type(score["username"]) is not str:
                raise LeaderboardError("Invalid username data type provided")
            # Case if score is not int
            if type(score["score"]) is not int:
                raise LeaderboardError("Invalid username data type provided")
            if len(score["username"]) > 10:
                raise LeaderboardError("A username is too " "long in the leaderboard")
            # Case of negative score
            if score["score"] < 0:
                raise LeaderboardError(
                    "Invalid negative score" " provided in the leaderboard"
                )

        return self


class ABSLeaderboardManager(ABC):
    """Interface for creating different leaderboard managers"""

    @staticmethod
    @abstractmethod
    def load_leaderboard(source: str, signature: str) -> Leaderboard:
        """Load a leaderboard object from a given source"""
        pass

    @staticmethod
    @abstractmethod
    def save_score(username: str,
                   score: int,
                   target: str,
                   signature: str,
                   leaderboard: Leaderboard) -> None:
        """Save the leaderboard data to the given target"""
        pass


class LeaderboardManager(ABSLeaderboardManager):
    """Local leaderboard loader and saver (json input / output)"""

    @staticmethod
    @abstractmethod
    def load_leaderboard(source: str, signature: str) -> Leaderboard:
        """Load the given json file (path in source) and returns the
        leaderboard with the corresponding signature"""

        # Load the file
        try:
            with open(source, "r") as f:
                file_content = f.read()
        except (FileNotFoundError, PermissionError):
            raise LeaderboardFileError("Unable to load the leaderboard")

        # JSON conversion
        try:
            data = json.loads(file_content)
        except json.JSONDecodeError:
            raise LeaderboardFileError("Invalid JSON format")

        # Verify each leaderboard
        if type(data) is not list:
            raise LeaderboardFileError(
                "Invalid JSON format (needs to be a list of dicts)"
            )
        for leaderboard in data:
            # Verify that the leaderboard is a dict
            if type(leaderboard) is not dict:
                raise LeaderboardFileError(
                    "Invalid JSON format (needs to be a list of dicts)"
                )
            # Verify keys presence for each leaderboard
            if (
                "signature" not in leaderboard.keys()
                or "scores" not in leaderboard.keys()
            ):
                raise LeaderboardFileError(
                    "Invalid JSON format (needs signature and score keys)"
                )
            if type(leaderboard["signature"]) is not str:
                raise LeaderboardFileError("Leaderboard must be a string")

        # Create Leaderboards objects
        leaderboards: list[Leaderboard] = []
        for leaderboard in data:
            try:
                leaderboards.append(
                    Leaderboard(
                        signature=leaderboard["signature"], scores=leaderboard["scores"]
                    )
                )
            except ValidationError:
                raise LeaderboardFileError("Invalid JSON format")

        # Return the leaderboard if identified
        for leaderboard in leaderboards:
            if leaderboard.signature == signature:
                return leaderboard

        # Return blank leaderboard since no leaderboard has the given signature
        return Leaderboard(signature=signature, scores=[])

    @staticmethod
    @abstractmethod
    def save_score(username: str,
                   score: int,
                   target: str,
                   signature: str,
                   leaderboard: Leaderboard) -> None:
        """Saves the score in the leaderboard"""
        # Create update of current leaderboard
        leaderboard.scores.append({
            'username': username,
            'score': score
        })

        # Open JSON target
        with open(target, 'r') as f:
            content = f.read()
        json_data = json.loads(content)

        # Search for corresponding signature in data
        for leaderboards in json_data:
            if leaderboards['signature'] == signature:
                # Erase this leaderboard's data with new leaderboard
                leaderboards['scores'] = leaderboard.scores
                with open(target, 'w') as f:
                    json.dump(json_data, f, indent=4)
                return None
        
        # No corresponding signature found. Creating new leaderboard
        json_data.append({
            'signature': leaderboard.signature,
            'scores': leaderboard.scores
        })
        with open(target, 'w') as f:
            json.dump(json_data, f, indent=4)
        return None
