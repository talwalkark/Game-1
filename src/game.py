"""
Main game engine for Magical Athlete.
Orchestrates game flow, race management, and scoring.
"""

import random
from typing import List, Tuple, Optional
from src.player import Player
from src.racer import Racer
from src.track import Track, get_tracks_for_game


class MagicalAthleteGame:
    """Main game engine."""
    
    TOTAL_RACES = 4
    FIRST_PLACE_POINTS = 10
    SECOND_PLACE_POINTS = 5
    
    def __init__(self, player_names: List[str]):
        """
        Initialize a new game.
        
        Args:
            player_names: List of player names
        """
        self.players = [Player(name, i) for i, name in enumerate(player_names)]
        self.num_players = len(self.players)
        self.current_race = 0
        self.tracks = get_tracks_for_game(self.TOTAL_RACES)
        self.game_over = False
        self.race_results = []  # List of (race_num, finishers)
    
    def __repr__(self) -> str:
        return f"Game({len(self.players)} players, race {self.current_race + 1}/{self.TOTAL_RACES})"
    
    # ============= SETUP PHASE =============
    
    def draft_racers(self, all_available_racers: List[Racer]) -> None:
        """
        Execute the snake draft for racer selection.
        
        Args:
            all_available_racers: Pool of all available racers
        """
        # Shuffle and select cards (2x players × 2 rounds = 4 racers each)
        available_racers = all_available_racers.copy()
        random.shuffle(available_racers)
        
        # Determine draft order (highest roll first)
        draft_order = self._determine_draft_order()
        
        # Two rounds of drafting
        for round_num in range(2):
            if round_num % 2 == 1:
                # Reverse order for snake draft
                draft_order = draft_order[::-1]
            
            for player_idx in draft_order:
                if available_racers:
                    racer = available_racers.pop()
                    self.players[player_idx].add_racer(racer)
    
    def _determine_draft_order(self) -> List[int]:
        """Determine draft order by die rolls (highest first)."""
        rolls = [(i, random.randint(1, 6)) for i in range(self.num_players)]
        rolls.sort(key=lambda x: x[1], reverse=True)
        return [idx for idx, roll in rolls]
    
    # ============= RACE PHASE =============
    
    def start_new_race(self) -> None:
        """Start a new race."""
        if self.current_race >= self.TOTAL_RACES:
            raise ValueError("All races completed")
        
        # Reset all players for new race
        for player in self.players:
            player.reset_for_new_race()
        
        self.current_race += 1
        print(f"\n{'='*50}")
        print(f"RACE {self.current_race} - {self.tracks[self.current_race - 1].difficulty.value.upper()}")
        print(f"{'='*50}\n")
    
    def run_race(self) -> Tuple[Player, Player]:
        """
        Run a complete race.
        
        Returns:
            Tuple of (1st place player, 2nd place player)
        """
        self.start_new_race()
        
        # Players select racers simultaneously
        self._select_racers()
        
        # Main race loop
        finishers = []
        turn_order = self._determine_turn_order()
        turn_count = 0
        
        while len(finishers) < 2 and turn_count < 1000:  # Safety limit
            for player_idx in turn_order:
                player = self.players[player_idx]
                racer = player.current_racer
                
                if racer and not self._check_finished(racer):
                    # Player takes their turn
                    die_roll = random.randint(1, 6)
                    print(f"{player.name}'s {racer.name} rolls {die_roll}...")
                    racer.move(die_roll)
                    print(f"  → Now at position {racer.position}")
                    
                    # Check if finished
                    if self._check_finished(racer):
                        finishers.append((len(finishers) + 1, player, racer))
                        print(f"  🏁 {racer.name} finishes in position {len(finishers)}!\n")
                    
                    if len(finishers) >= 2:
                        break
            
            turn_count += 1
        
        # Award points
        self._award_points(finishers)
        return finishers[0][1], finishers[1][1]
    
    def _select_racers(self) -> None:
        """Have players select racers for this race."""
        print("Players selecting racers for this race...")
        for player in self.players:
            available = player.get_available_racers()
            if not available:
                raise ValueError(f"{player.name} has no racers left!")
            
            # In CLI version, would prompt; here we auto-select first available
            racer = player.select_racer(0)
            print(f"{player.name} selected {racer.name}")
    
    def _determine_turn_order(self) -> List[int]:
        """Determine turn order for race (random or based on last race)."""
        order = list(range(self.num_players))
        random.shuffle(order)
        return order
    
    def _check_finished(self, racer: Racer) -> bool:
        """Check if racer has crossed finish line."""
        current_track = self.tracks[self.current_race - 1]
        return current_track.is_finished(racer.position)
    
    def _award_points(self, finishers: List[Tuple[int, Player, Racer]]) -> None:
        """Award points to finishers."""
        if len(finishers) > 0:
            first_player = finishers[0][1]
            first_player.add_points(self.FIRST_PLACE_POINTS, "1st", self.current_race)
            print(f"✓ {first_player.name} gets {self.FIRST_PLACE_POINTS} points for 1st place")
        
        if len(finishers) > 1:
            second_player = finishers[1][1]
            second_player.add_points(self.SECOND_PLACE_POINTS, "2nd", self.current_race)
            print(f"✓ {second_player.name} gets {self.SECOND_PLACE_POINTS} points for 2nd place")
    
    # ============= GAME END =============
    
    def is_game_over(self) -> bool:
        """Check if all races are complete."""
        return self.current_race >= self.TOTAL_RACES
    
    def get_winner(self) -> Player:
        """Get the winner (most points)."""
        if not self.is_game_over():
            raise ValueError("Game not over yet")
        
        return max(self.players, key=lambda p: p.points)
    
    def get_final_standings(self) -> str:
        """Get formatted final standings."""
        if not self.is_game_over():
            raise ValueError("Game not over yet")
        
        standings = "\n" + "="*50 + "\n"
        standings += "FINAL STANDINGS\n"
        standings += "="*50 + "\n"
        
        sorted_players = sorted(self.players, key=lambda p: p.points, reverse=True)
        for rank, player in enumerate(sorted_players, 1):
            standings += f"{rank}. {player.name}: {player.points} points\n"
            standings += player.get_score_summary()
        
        return standings


def main():
    """Run a sample game."""
    print("Welcome to Magical Athlete!\n")
    
    # For testing, use hardcoded players
    game = MagicalAthleteGame(["Alice", "Bob", "Charlie"])
    
    print(f"Starting game with {len(game.players)} players\n")
    
    # For now, just show the game is ready
    print(f"Game initialized: {game}")
    print(f"Ready to start race phase with {game.TOTAL_RACES} races\n")


if __name__ == "__main__":
    main()