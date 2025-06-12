
# Import the main game logic and display function
from game import SolitaireGame
from display import display_game
from display import print_win_screen

def main():
    while True:
        game = SolitaireGame()
        while True:
            display_game(game)

            # Check for win condition
            if game.check_win():
                print_win_screen(game)
                user = input()
                if user.lower().strip() == 'q':
                    print("Goodbye!")
                    return
                else:
                    break  # restart

            # Get user input, turns to lowercase and strips of whitespace
            command = input("Enter command: ").lower().strip()

            # Quit the game
            if command == 'q':
                print("Goodbye!")
                return

            # Restart the game
            if command == 'r':
                break  # break inner loop to restart

            # Draw a card from the reserve (stock) pile
            elif command == 'd':
                game.draw_from_reserve()

            # Move the top card from the waste to the foundation
            elif command.startswith('fw'):
                game.move_waste_to_foundation()

            # Move the top card from a tableau column to the foundation
            elif command.startswith('f'):
                try:
                    col_num = int(command[1:]) - 1  # Convert to 0-based index
                    if 0 <= col_num < 7:
                        game.move_to_foundation(col_num)
                except (ValueError, IndexError):
                    pass

            # Move the top card from the waste to a tableau column
            elif command.startswith('mw'):
                col_str = command[2:]
                try:
                    col_num = int(col_str) - 1  # Convert to 0-based index
                    if 0 <= col_num < 7:
                        game.move_waste_to_column(col_num)
                except (ValueError, IndexError):
                    pass

            # Move cards between tableau columns
            elif command.startswith('m'):
                try:
                    if len(command) == 3:
                        source_col = int(command[1]) - 1  # Source column (0-based)
                        target_col = int(command[2]) - 1  # Target column (0-based)
                        if 0 <= source_col < 7 and 0 <= target_col < 7:
                            source = game.columns[source_col]
                            source_index = next((i for i, card in enumerate(source) if card.face_up), None)
                            if source_index is not None:
                                game.move_between_columns(source_col, source_index, target_col)
                except ValueError:
                    pass
            # Any other input is ignored (invalid command)

# Run the game only if this file is executed directly
if __name__ == "__main__":
    main()