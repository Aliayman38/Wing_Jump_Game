# WING JUMP - Advanced Flappy Bird Clone

A dynamic side-scrolling game built with **Python** and **Pygame**. This project goes beyond basic mechanics by incorporating a lives system and adaptive environments.

## 🌟 Features
**Lives System**: Unlike the original, the player has **3 attempts** (represented by heart icons) before the game ends.
**Dynamic Backgrounds**: The environment shifts from day to night as the score increases (Score > 15), enhancing the visual experience.
**Physics & Animation**: Implements gravity, bird rotation based on velocity, and sprite animation.
**Sound Effects**: Integrated audio for jumping, scoring, and colliding.

## 🛠️ Technical Implementation
**Object-Oriented Programming (OOP)**: Used classes for `Bird`, `pipe`, and `losing` button management.
**Sprite Groups**: Efficient collision detection using Pygame's `sprite.Group`.
**Game State Management**: Handled transitions between "Start", "Running", and "Game Over" states.

## 🕹️ Controls
**Mouse Click**: Start the game.
**Space Bar**: Jump.
