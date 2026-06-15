"""
Ability system for Magical Athlete game.
Implements racer-specific powers and interactions.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


class AbilityTrigger(Enum):
    """When an ability triggers."""
    MANDATORY = "mandatory"  # Always activates
    OPTIONAL = "optional"    # Player can choose
    TRIGGER = "trigger"      # Triggers on condition


@dataclass
class AbilityEffect:
    """Represents the effect of an ability."""
    target: str  # "self", "opponent", "all", "on_space"
    effect_type: str  # "move", "trip", "warp", "buff", "debuff"
    amount: int = 0
    condition: Optional[str] = None


class RacerAbility:
    """Base class for racer abilities."""
    
    def __init__(self, name: str, description: str, trigger: AbilityTrigger):
        self.name = name
        self.description = description
        self.trigger = trigger
    
    def can_activate(self, game_state: Dict[str, Any]) -> bool:
        """Check if ability can be activated given current game state."""
        return True
    
    def execute(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ability. Returns modified game state."""
        return game_state


class CoachAbility(RacerAbility):
    """Coach: Everyone on my space gets +1 to their main move."""
    
    def __init__(self):
        super().__init__(
            "Team Boost",
            "Everyone on my space gets +1 to their main move, including me.",
            AbilityTrigger.MANDATORY
        )


class BananaAbility(RacerAbility):
    """Banana: Trip any racer that stops on my space, or when I stop on theirs."""
    
    def __init__(self):
        super().__init__(
            "Slip Hazard",
            "Trip any racer that stops on my space, or when I stop on theirs.",
            AbilityTrigger.MANDATORY
        )


class LeaptoadAbility(RacerAbility):
    """Leaptoad: While moving, I skip spaces with other racers on them."""
    
    def __init__(self):
        super().__init__(
            "Space Skipper",
            "While moving, I skip spaces with other racers on them.",
            AbilityTrigger.MANDATORY
        )


class LegsAbility(RacerAbility):
    """Legs: I can skip rolling for my main move and move 5 instead."""
    
    def __init__(self):
        super().__init__(
            "Power Stride",
            "I can skip rolling for my main move and move 5 instead.",
            AbilityTrigger.OPTIONAL
        )


class CopycatAbility(RacerAbility):
    """Copycat: I have the power of the racer currently in the lead."""
    
    def __init__(self):
        super().__init__(
            "Mimic Leader",
            "I have the power of the racer currently in the lead. If there's a tie, I pick.",
            AbilityTrigger.MANDATORY
        )


class CheerleaderAbility(RacerAbility):
    """Cheerleader: Make last place racers move 2, you move 1."""
    
    def __init__(self):
        super().__init__(
            "Support Squad",
            "At the start of my turn, I can make the racer(s) in last place move 2. If I do, I move 1.",
            AbilityTrigger.OPTIONAL
        )


class DicemongerAbility(RacerAbility):
    """Dicemonger: Anyone can reroll. When they do, Dicemonger moves 1."""
    
    def __init__(self):
        super().__init__(
            "Reroll Dealer",
            "Anyone can reroll their main move once per turn. When another racer does it, I move 1.",
            AbilityTrigger.MANDATORY
        )


class GunkAbility(RacerAbility):
    """Gunk: Other racers get -1 to their main move."""
    
    def __init__(self):
        super().__init__(
            "Slowing Ooze",
            "Other racers get -1 to their main move.",
            AbilityTrigger.MANDATORY
        )


class HugeBabyAbility(RacerAbility):
    """Huge Baby: No one else can be on my space except start."""
    
    def __init__(self):
        super().__init__(
            "Personal Space",
            "No one can ever be on my space, besides the start space. When that would happen, put them behind me.",
            AbilityTrigger.MANDATORY
        )


class MagicianAbility(RacerAbility):
    """Magician: I can warp a racer to my space."""
    
    def __init__(self):
        super().__init__(
            "Teleport",
            "At the start of my turn, I can warp a racer to my space.",
            AbilityTrigger.OPTIONAL
        )


class FlashAbility(RacerAbility):
    """The Flash: Move twice, each move triggers abilities separately."""
    
    def __init__(self):
        super().__init__(
            "Double Time",
            "On your main move, move twice. Each move triggers abilities separately.",
            AbilityTrigger.MANDATORY
        )


class HareAbility(RacerAbility):
    """Hare: Move 4 if rolling 1 or 2."""
    
    def __init__(self):
        super().__init__(
            "Predict Jump",
            "When I roll for my main move, I can move 4 if I roll a 1 or 2 (predicting).",
            AbilityTrigger.OPTIONAL
        )


# Ability Registry - maps racer names to ability classes
ABILITY_REGISTRY: Dict[str, type] = {
    "Coach": CoachAbility,
    "Banana": BananaAbility,
    "Leaptoad": LeaptoadAbility,
    "Legs": LegsAbility,
    "Copycat": CopycatAbility,
    "Cheerleader": CheerleaderAbility,
    "Dicemonger": DicemongerAbility,
    "Gunk": GunkAbility,
    "Huge Baby": HugeBabyAbility,
    "Magician": MagicianAbility,
    "The Flash": FlashAbility,
    "Hare": HareAbility,
}


def get_ability(racer_name: str) -> Optional[RacerAbility]:
    """Get ability instance by racer name."""
    ability_class = ABILITY_REGISTRY.get(racer_name)
    if ability_class:
        return ability_class()
    return None
