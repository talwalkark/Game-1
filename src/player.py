"""
Player class for Magical Athlete game.
Manages player state, racers, and points.
"""

from typing import List, Optional
from src.racer import Racer


class Player:
    """Represents a player in the game."""
    
    def __init__(self, name: str, player_id: int):
        """
        Initialize a player.
        
        Args:
            name: Player's display name
            player_id: Unique player identifier (0-indexed)
        """
        self.name = name
        self.player_id = player_id
        self.racers: List[Racer] = []  # Hand of racers (up to 4)
        self.points = 0  # Total points across all races
        self.current_racer: Optional[Racer] = None  # Active racer in current race
        self.race_placements = []  # Track of placements: [(race_num, placement, points), ...]
    
    def __repr__(self) -> str:
        return f"Player({self.name}, racers={len(self.racers)}, points={self.points})"
    
    def add_racer(self, racer: Racer) -> None:
        """Add a racer to this player's hand during draft."""
        if len(self.racers) >= 4:
            raise ValueError(f"Player {self.name} already has 4 racers")
        self.racers.append(racer)
    
    def select_racer(self, racer_index: int) -> Racer:
        """
        Select a racer for the current race.
        
        Args:
            racer_index: Index of racer in player's hand
            
        Returns:
            Selected racer
        """
        if racer_index < 0 or racer_index >= len(self.racers):
            raise IndexError(f"Racer index {racer_index} out of range")
        
        racer = self.racers[racer_index]
        if racer.used:
            raise ValueError(f"Racer {racer.name} already used in this game")
        
        self.current_racer = racer
        racer.used = True
        return racer
    
    def add_points(self, points: int, placement: str, race_num: int) -> None:
        """
        Add points from a race placement.
        
        Args:
            points: Points earned
            placement: "1st" or "2nd"
            race_num: Which race (1-4)
        """
        self.points += points
        self.race_placements.append((race_num, placement, points))
    
    def get_available_racers(self) -> List[Racer]:
        """Get racers that haven't been used yet."""
        return [r for r in self.racers if not r.used]
    
    def reset_for_new_race(self) -> None:
        """Reset player state for a new race."""
        self.current_racer = None
        for racer in self.racers:
            racer.reset_race()
    
    def get_score_summary(self) -> str:
        """Get a summary of player's race results."""
        summary = f"\n{self.name}: {self.points} total points\n"
        summary += "Race Results:\n"
        for race_num, placement, points in self.race_placements:
            summary += f"  Race {race_num}: {placement} place (+{points} pts)\n"
        return summary