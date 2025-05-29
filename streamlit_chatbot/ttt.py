import streamlit as st
import random
import time # Used for a small delay to make AI's move more noticeable

# --- Game Logic Functions (Adapted from previous AI example) ---

def init_board():
    """Initializes a new empty Tic-Tac-Toe board."""
    return [' '] * 9

def check_win(board, player):
    """
    Checks if the given player has won the game.
    Args:
        board (list): The current state of the Tic-Tac-Toe board.
        player (str): The player's symbol ('X' or 'O').
    Returns:
        bool: True if the player has won, False otherwise.
    """
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw(board):
    """
    Checks if the game is a draw (all squares filled, no winner).
    Args:
        board (list): The current state of the Tic-Tac-Toe board.
    Returns:
        bool: True if it's a draw, False otherwise.
    """
    return all(square != ' ' for square in board)

def get_available_moves(board):
    """
    Returns a list of indices of empty squares on the board.
    Args:
        board (list): The current state of the Tic-Tac-Toe board.
    Returns:
        list: A list of available move indices.
    """
    return [i for i, spot in enumerate(board) if spot == ' ']

def ai_move(board, ai_player, human_player):
    """
    Determines the AI's best move using a simple strategy.
    Args:
        board (list): The current state of the Tic-Tac-Toe board.
        ai_player (str): The AI's symbol ('X' or 'O').
        human_player (str): The human player's symbol ('X' or 'O').
    Returns:
        int: The index of the square the AI chooses.
    """
    available_moves = get_available_moves(board)

    # 1. Check if AI can win in the next move
    for move in available_moves:
        temp_board = list(board) # Create a copy to simulate
        temp_board[move] = ai_player
        if check_win(temp_board, ai_player):
            return move

    # 2. Check if human can win in the next move, and block them
    for move in available_moves:
        temp_board = list(board) # Create a copy to simulate
        temp_board[move] = human_player
        if check_win(temp_board, human_player):
            return move

    # 3. Try to take the center (most strategic spot)
    if 4 in available_moves:
        return 4

    # 4. Try to take a corner
    corners = [0, 2, 6, 8]
    random.shuffle(corners) # Randomize corner choice
    for move in corners:
        if move in available_moves:
            return move

    # 5. Take any available side spot
    sides = [1, 3, 5, 7]
    random.shuffle(sides) # Randomize side choice
    for move in sides:
        if move in available_moves:
            return move

    # Fallback: if somehow no strategic move, pick a random available move
    # This should only happen if the board is full and no other rule applies
    if available_moves:
        return random.choice(available_moves)
    return -1 # Should not happen in a valid game state where moves are available


# --- Streamlit Application Logic ---

# Initialize session state for the game if it doesn't exist
if 'game' not in st.session_state:
    st.session_state.game = {
        'board': init_board(),
        'current_player': 'X', # Human starts as 'X'
        'human_player': 'X',
        'ai_player': 'O',
        'game_over': False,
        'winner': None,
        'message': "Your turn (X)!",
        'ai_thinking': False # Flag to indicate AI is making a move
    }

def reset_game():
    """Resets the game state in session_state."""
    st.session_state.game = {
        'board': init_board(),
        'current_player': 'X',
        'human_player': 'X',
        'ai_player': 'O',
        'game_over': False,
        'winner': None,
        'message': "Your turn (X)!",
        'ai_thinking': False
    }
    st.rerun() # Rerun the app to reflect the reset state

def handle_click(index):
    """
    Handles a click on a board square.
    Updates the board, checks for win/draw, and triggers AI move if applicable.
    """
    game = st.session_state.game

    # Do nothing if game is over, square is already taken, or AI is thinking
    if game['game_over'] or game['board'][index] != ' ' or game['ai_thinking']:
        return

    # Human's move
    game['board'][index] = game['human_player']
    game['message'] = "" # Clear previous message

    # Check for human win or draw
    if check_win(game['board'], game['human_player']):
        game['winner'] = game['human_player']
        game['game_over'] = True
        game['message'] = f"🎉 Player {game['human_player']} wins! 🎉"
    elif check_draw(game['board']):
        game['winner'] = "Draw"
        game['game_over'] = True
        game['message'] = "It's a draw!"
    else:
        # If game not over, it's AI's turn
        game['current_player'] = game['ai_player']
        game['message'] = "AI (O) is thinking..."
        game['ai_thinking'] = True # Set flag for AI turn
        # Streamlit will rerun, and the AI move will be handled in the main loop
        st.rerun()

# --- Streamlit UI ---

st.set_page_config(layout="centered", page_title="Tic-Tac-Toe AI")

st.title("✖️⭕ Tic-Tac-Toe AI 🧠")
st.write("Play against a simple AI opponent!")

# Display game status message
if st.session_state.game['message']:
    if "wins" in st.session_state.game['message'] or "draw" in st.session_state.game['message']:
        st.success(st.session_state.game['message'])
    elif st.session_state.game['ai_thinking']:
        st.info(st.session_state.game['message'])
    else:
        st.write(st.session_state.game['message'])

# Create the game board grid
board = st.session_state.game['board']
game_over = st.session_state.game['game_over']

# Use columns for a 3x3 grid layout
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        index = i * 3 + j
        with cols[j]:
            # Display the content of the square or an empty string if not played
            square_content = board[index] if board[index] != ' ' else ' '
            
            # Disable buttons if game is over or square is taken
            disabled = game_over or board[index] != ' ' or st.session_state.game['ai_thinking']

            # Use a larger font size for the button text
            button_style = f"font-size: 3em; height: 100px; width: 100%;"
            
            # Add some visual flair for X and O
            if square_content == 'X':
                button_label = "❌"
            elif square_content == 'O':
                button_label = "⭕"
            else:
                button_label = " " # Empty space for clickable button

            if st.button(
                button_label,
                key=f"square_{index}",
                on_click=handle_click,
                args=(index,),
                disabled=disabled,
                help=f"Click to play square {index}",
                use_container_width=True
            ):
                pass # The on_click handler does the work

# --- AI Turn Handling ---
# This block runs after the human's click has been processed and the UI updated
# (or after a reset). If it's AI's turn and game is not over, AI makes a move.
if st.session_state.game['ai_thinking'] and not st.session_state.game['game_over']:
    # Add a small delay to simulate thinking time for the AI
    time.sleep(0.8) # Adjust this value for faster/slower AI response

    ai_move_index = ai_move(
        st.session_state.game['board'],
        st.session_state.game['ai_player'],
        st.session_state.game['human_player']
    )

    if ai_move_index != -1: # Ensure a valid move was returned
        st.session_state.game['board'][ai_move_index] = st.session_state.game['ai_player']

        # Check for AI win or draw after its move
        if check_win(st.session_state.game['board'], st.session_state.game['ai_player']):
            st.session_state.game['winner'] = st.session_state.game['ai_player']
            st.session_state.game['game_over'] = True
            st.session_state.game['message'] = f"🤖 AI ({st.session_state.game['ai_player']}) wins! Better luck next time!"
        elif check_draw(st.session_state.game['board']):
            st.session_state.game['winner'] = "Draw"
            st.session_state.game['game_over'] = True
            st.session_state.game['message'] = "It's a draw!"
        else:
            st.session_state.game['current_player'] = st.session_state.game['human_player']
            st.session_state.game['message'] = "Your turn (X)!"

    st.session_state.game['ai_thinking'] = False # Reset AI thinking flag
    st.rerun() # Rerun to show AI's move and update messages

# Reset button
if st.session_state.game['game_over']:
    if st.button("Play Again?", key="play_again_button"):
        reset_game()

# Instructions
with st.expander("ℹ️ How to Play"):
    st.write("""
    1.  You are **X** and the AI is **O**.
    2.  Click on an empty square to place your **X**.
    3.  The AI will then make its move.
    4.  The goal is to get three of your marks in a row, column, or diagonal.
    5.  If all squares are filled and no one wins, it's a draw!
    """)