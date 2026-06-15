"""
Racer class definition for Magical Athlete game.
Each racer has unique abilities that affect gameplay.
"""

from enum import Enum
from typing import List, Callable, Optional


class AbilityType(Enum):
    """Types of racer abilities."""
    OPTIONAL = "optional"  # CAN use ability
    MANDATORY = "mandatory"  # MUST use ability
    TRIGGER = "trigger"  # Triggers on specific condition


class Racer:
    """Represents a racer in the game."""
    
    def __init__(self, name: str, ability_name: str, ability_description: str, 
                 ability_type: AbilityType = AbilityType.MANDATORY):
        """
        Initialize a racer.
        
        Args:
            name: Racer's name
            ability_name: Name of unique ability
            ability_description: Description of what ability does
            ability_type: Whether ability is optional or mandatory
        """
        self.name = name
        self.ability_name = ability_name
        self.ability_description = ability_description
        self.ability_type = ability_type
        self.position = 0  # Current space on track
        self.is_tripped = False  # If tripped, skips next main move
        self.has_moved_this_turn = False
        self.used = False  # Used in current race
        
    def __repr__(self) -> str:
        return f"Racer({self.name}, pos={self.position}, tripped={self.is_tripped})"
    
    def move(self, spaces: int) -> None:
        """Move racer forward by given number of spaces."""
        if self.is_tripped:
            self.is_tripped = False
            # Skip this move - don't advance position
            return
        self.position += spaces
        self.has_moved_this_turn = True
    
    def trip(self) -> None:
        """Trip this racer - they skip their next main move."""
        self.is_tripped = True
    
    def warp(self, new_position: int) -> None:
        """
        Warp to a new position without counting as a movement.
        Doesn't trigger movement-based abilities.
        """
        self.position = new_position
        # Note: has_moved_this_turn remains False since warp doesn't count as movement
    
    def reset_turn_state(self) -> None:
        """Reset per-turn flags."""
        self.has_moved_this_turn = False
    
    def reset_race(self) -> None:
        """Reset racer for new race."""
        self.position = 0
        self.is_tripped = False
        self.has_moved_this_turn = False
        self.used = False


# Example racer definitions - to be loaded from JSON in production
EXAMPLE_RACERS = [
    Racer(
        "The Flash",
        "Double Time",
        "On your main move, move twice. Each move triggers abilities separately.",
        AbilityType.MANDATORY
    ),
    Racer(
        "Turtle",
        "Slow and Steady",
        "You CAN slow down any opponent's next main move to 1 space.",
        AbilityType.OPTIONAL
    ),
    Racer(
        "Chaos Knight",
        "Unpredictable",
        "After you move, roll again. You must move that many MORE spaces.",
        AbilityType.MANDATORY
    ),
    Racer(
        "Teleporter",
        "Blink",
        "You CAN warp to any empty space on the track.",
        AbilityType.OPTIONAL
    ),
]