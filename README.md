# Magical Athlete Game

A digital implementation of the chaotic racing board game **Magical Athlete**.

## Overview
Magical Athlete is a 4-race competitive game where players draft racers and compete across increasingly wild tracks. The player with the most points after all races wins!

## Game Features
- **4 Races** across different track difficulties (Mild Mile → Wild variants)
- **Snake Draft System** for racer selection
- **Unique Racer Abilities** with complex interactions
- **Simultaneous Action Selection** for dynamic gameplay
- **Power Priority System** for resolving conflicts

## Project Structure
```
├── README.md                 # This file
├── GAME_RULES.md            # Full game manual and rules
├── src/
│   ├── game.py              # Main game engine
│   ├── racer.py             # Racer class and abilities
│   ├── track.py             # Track definitions (Mild/Wild)
│   ├── player.py            # Player class
│   └── ui.py                # Command-line interface
├── data/
│   ├── racers.json          # Racer definitions and abilities
│   ├── tracks.json          # Track layout and spaces
│   └── game_config.json     # Game configuration
└── tests/
    └── test_game.py         # Unit tests
```

## Getting Started
```bash
python src/game.py
```

## Game Flow
1. **Setup**: Players draft 4 racers each from a shuffled pool
2. **Race Phase**: 
   - Players simultaneously select a racer
   - Take turns rolling and moving
   - Trigger special abilities
   - First 2 racers to finish earn points (1st: Gold, 2nd: Silver)
3. **After 4 Races**: Player with most points wins

## Key Mechanics
- **Main Move**: Roll die, move that many spaces
- **Trip**: Racer skips next main move
- **Warp**: Move without counting as movement
- **Passing**: Racer overtakes another (triggers abilities)
- **Power Priority**: Current player → Other players (clockwise) → Track spaces

## Resources
- Original game: [cmyk.games/ma](https://cmyk.games/ma)