import streamlit as st
import random
import time

# Initialize the game state
def init_game():
    # Create pairs of emojis for the cards
    emojis = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"]
    cards = emojis + emojis  # Create pairs
    random.shuffle(cards)
    
    return {
        'cards': cards,
        'revealed': [False] * 16,  # Track which cards are face up
        'matched': [False] * 16,   # Track which cards are matched
        'first_card': None,        # First card clicked
        'second_card': None,       # Second card clicked
        'moves': 0,
        'matches': 0,
        'game_complete': False,
        'show_second_card': False,
        'last_move_time': 0
    }

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = init_game()

def reset_game():
    st.session_state.game_state = init_game()

def handle_card_click(index):
    game = st.session_state.game_state
    
    # Don't allow clicks on already matched or revealed cards
    if game['matched'][index] or game['revealed'][index]:
        return
    
    # If we're showing second card briefly, don't allow new clicks
    if game['show_second_card'] and time.time() - game['last_move_time'] < 1.5:
        return
    
    # If this is the first card selection
    if game['first_card'] is None:
        game['first_card'] = index
        game['revealed'][index] = True
    
    # If this is the second card selection
    elif game['second_card'] is None and index != game['first_card']:
        game['second_card'] = index
        game['revealed'][index] = True
        game['moves'] += 1
        game['show_second_card'] = True
        game['last_move_time'] = time.time()
        
        # Check if cards match
        if game['cards'][game['first_card']] == game['cards'][game['second_card']]:
            # Match found!
            game['matched'][game['first_card']] = True
            game['matched'][game['second_card']] = True
            game['matches'] += 1
            
            # Reset for next turn
            game['first_card'] = None
            game['second_card'] = None
            game['show_second_card'] = False
            
            # Check if game is complete
            if game['matches'] == 8:  # 8 pairs total
                game['game_complete'] = True
        
        # If no match, cards will be hidden after delay (handled in display)

def check_and_hide_cards():
    game = st.session_state.game_state
    
    if (game['show_second_card'] and 
        game['first_card'] is not None and 
        game['second_card'] is not None and
        time.time() - game['last_move_time'] > 1.5):
        
        # Hide non-matching cards
        if not game['matched'][game['first_card']]:
            game['revealed'][game['first_card']] = False
            game['revealed'][game['second_card']] = False
        
        # Reset for next turn
        game['first_card'] = None
        game['second_card'] = None
        game['show_second_card'] = False

# Main app
st.title("🧠 Memory Card Game")
st.write("Find all the matching pairs!")

# Game stats
game = st.session_state.game_state
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Moves", game['moves'])
with col2:
    st.metric("Matches", f"{game['matches']}/8")
with col3:
    if st.button("🔄 New Game"):
        reset_game()
        st.rerun()

# Check if we need to hide cards
check_and_hide_cards()

# Display the game board
st.write("---")

# Create 4x4 grid of cards
for row in range(4):
    cols = st.columns(4)
    for col in range(4):
        index = row * 4 + col
        
        with cols[col]:
            # Determine what to show on the card
            if game['matched'][index] or game['revealed'][index]:
                # Show the emoji
                if st.button(
                    game['cards'][index], 
                    key=f"card_{index}",
                    help=f"Card {index + 1}",
                    disabled=game['matched'][index]
                ):
                    handle_card_click(index)
            else:
                # Show card back
                if st.button(
                    "❓", 
                    key=f"card_{index}",
                    help=f"Card {index + 1}"
                ):
                    handle_card_click(index)

# Game completion message
if game['game_complete']:
    st.balloons()
    st.success(f"🎉 Congratulations! You won in {game['moves']} moves!")
    if st.button("🎯 Play Again"):
        reset_game()
        st.rerun()

# Auto-refresh to handle card hiding
if game['show_second_card']:
    time.sleep(0.1)
    st.rerun()

# Instructions
with st.expander("ℹ️ How to Play"):
    st.write("""
    1. Double click on cards to reveal them
    2. Try to find matching pairs of emojis
    3. When you find a match, the cards stay face up
    4. If cards don't match, they'll flip back over after a moment
    5. Try to complete the game in as few moves as possible!
    """)