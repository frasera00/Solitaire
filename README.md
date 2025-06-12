# Solitaire (Console Version)

A classic Solitaire (Klondike) card game playable entirely in your terminal, written in Python.

---

## How to Start the Project

1. **Clone or Download the Repository**
   - Download the project folder and enter the main folder:
        ```
     cd Solitaire
     ```

2. **Install Python**
   - Make sure you have Python 3.7 or newer installed.
   - Check with:
     ```
     python3 --version
     ```

3. **(Optional) Create a Virtual Environment**
   - Recommended for dependency management:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install Dependencies**
   - Install dependencies with:
     ```
     pip install -r requirements.txt
     ```
   - *Note: This project uses only the Python standard library, so this step may be skipped.*

5. **Run the Game**
     ```
     python3 main.py
     ```
---

## Game User Instructions

### **Goal**
Move all cards to the four foundation piles (one for each suit), building up from Ace to King.

### **Game Layout**
- **Tableau:** 7 columns of cards, only the last card in each column is face up.
- **Reserve (Stock):** Remaining cards, face down.
- **Waste:** Cards drawn from the reserve, face up.
- **Foundations:** Four piles, one for each suit, to build from Ace to King.

### **Controls**
Type commands and press Enter:

| Command         | Action                                                        |
|-----------------|--------------------------------------------------------------|
| `d`             | Draw a card from the reserve (stock) to the waste pile       |
| `mXY`           | Move cards from column X to column Y (e.g., `m13` moves from C1 to C3) |
| `mwY`           | Move the top waste card to column Y (e.g., `mw3` to C3)      |
| `fX`            | Move the top card from column X to its foundation (e.g., `f1`)|
| `fw`            | Move the top waste card to its foundation                    |
| `r`             | Restart the game                                             |
| `q`             | Quit the game                                                |

- **Columns are numbered 1–7.**
- **You can only move cards according to Solitaire rules:**
  - Cards in tableau must alternate colors and descend in value.
  - Only Kings (or sequences starting with King) can be placed in empty columns.
  - Foundations must be built up by suit from Ace to King.
  - Only one card is drawn from the reserve at a time; when empty, the waste is recycled.

---

## Code Structure and Class Descriptions

### **Modules / Files**
- `card.py` – Defines the `Card` class (suit, value, face up/down, color, flip).
- `deck.py` – Defines the `Deck` class (builds, shuffles, and deals cards).
- `game.py` – Contains the `SolitaireGame` class (game state and logic).
- `display.py` – Functions for displaying the game state and win screen.
- `main.py` – The main game loop and user input handling.
- `Solitaire_game.ipynb` – Jupyter notebook version with explanations and code.

### **Key Classes and Functions**

#### **Card**
- Represents a single playing card.
- Attributes: `suit`, `value`, `face_up`.
- Methods: `flip()`, `color()`, `__str__()`.

#### **Deck**
- Manages a collection of 52 cards.
- Methods: `build()`, `shuffle()`, `deal()`.

#### **SolitaireGame**
- Manages the entire game state:
  - `columns`: 7 tableau columns.
  - `foundations`: 4 suit piles.
  - `reserve`: stock pile.
  - `waste`: face-up pile.
- Methods:
  - `setup_columns()`, `setup_reserve()`
  - `draw_from_reserve()`
  - `move_waste_to_column(col_num)`
  - `move_waste_to_foundation()`
  - `move_to_foundation(col_num)`
  - `move_between_columns(source_col, source_index, target_col)`
  - `can_move_to_column(card, column)`
  - `can_move_to_foundation(card, foundation)`
  - `check_win()`

#### **Display Functions**
- `display_game(game)`: Shows the current game state in the terminal.
- `print_win_screen(game)`: Shows a congratulatory ASCII art win screen.

#### **Main Loop**
- Handles user input, updates game state, checks for win/restart/quit.

---

## Additional Notes

- The game uses ANSI escape codes for colored output. If colors do not display, it may be due to incompatibilities with the terminal.
- All code is commented for clarity.
- For further details, see code comments in each file or the Jupyter notebook for step-by-step explanations.

---

Enjoy playing Solitaire in your terminal!