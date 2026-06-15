"""
Track definitions for Magical Athlete game.
Tracks have different difficulty levels and space effects.
"""

from enum import Enum
from typing import List, Optional


class TrackDifficulty(Enum):
    """Track difficulty levels."""
    MILD = "mild"
    WILD = "wild"


class TrackSpace:
    """Represents a single space on the track."""
    
    def __init__(self, position: int, name: str = "", effect: str = "", difficulty: int = 0):
        """
        Initialize a track space.
        
        Args:
            position: Position number on track (0 = Start, N = Finish)
            name: Name of space (optional)
            effect: Description of space effect (optional)
            difficulty: Difficulty rating (0-3, higher = more chaotic)
        """
        self.position = position
        self.name = name
        self.effect = effect
        self.difficulty = difficulty
    
    def __repr__(self) -> str:
        return f"Space({self.position}, {self.name})"


class Track:
    """Represents a racing track."""
    
    def __init__(self, difficulty: TrackDifficulty, spaces: List[TrackSpace], finish_position: int):
        """
        Initialize a track.
        
        Args:
            difficulty: Mild or Wild
            spaces: List of all spaces on track
            finish_position: Position number of finish line
        """
        self.difficulty = difficulty
        self.spaces = spaces
        self.finish_position = finish_position
        self.current_racers = []  # Racers currently on this track
    
    def __repr__(self) -> str:
        return f"Track({self.difficulty.value}, {self.finish_position} spaces)"
    
    def is_finished(self, position: int) -> bool:
        """Check if racer has crossed finish line."""
        return position >= self.finish_position
    
    def get_space(self, position: int) -> Optional[TrackSpace]:
        """Get a specific track space by position."""
        if 0 <= position < len(self.spaces):
            return self.spaces[position]
        return None


# Example track definitions
MILD_MILE = Track(
    difficulty=TrackDifficulty.MILD,
    spaces=[
        TrackSpace(0, "Start", "Everyone starts here"),
        TrackSpace(1, "Straightaway", "No effect"),
        TrackSpace(2, "Straightaway", "No effect"),
        TrackSpace(3, "Straightaway", "No effect"),
        TrackSpace(4, "Turn", "Passing triggers abilities"),
        TrackSpace(5, "Straightaway", "No effect"),
        TrackSpace(6, "Straightaway", "No effect"),
        TrackSpace(7, "Straightaway", "No effect"),
        TrackSpace(8, "Finish", "Cross here to place"),
    ],
    finish_position=8
)

WILD_WARP = Track(
    difficulty=TrackDifficulty.WILD,
    spaces=[
        TrackSpace(0, "Start", "Everyone starts here"),
        TrackSpace(1, "Chaos Zone", "Triggers wild abilities"),
        TrackSpace(2, "Straightaway", "No effect"),
        TrackSpace(3, "Portal", "Warp to random space"),
        TrackSpace(4, "Trap", "Trip all racers here"),
        TrackSpace(5, "Straightaway", "No effect"),
        TrackSpace(6, "Mirror", "Duplicate one racer's move"),
        TrackSpace(7, "Vortex", "All racers shift position"),
        TrackSpace(8, "Finish", "Cross here to place"),
    ],
    finish_position=8
)


def get_tracks_for_game(num_races: int = 4) -> List[Track]:
    """
    Get the sequence of tracks for a game.
    Alternates between Mild and Wild.
    """
    tracks = []
    for i in range(num_races):
        if i % 2 == 0:
            tracks.append(MILD_MILE)
        else:
            tracks.append(WILD_WARP)
    return tracks
