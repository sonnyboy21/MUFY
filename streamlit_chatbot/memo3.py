import streamlit as st
import random
import time

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide default streamlit styling */
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 2rem;
        border-radius: 15px;
        border: 3px solid #e1e5e9;
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        box-shadow: 5px 5px 10px #d1d9e6, -5px -5px 10px #ffffff;
        transition: all 0.3s ease;
        margin: 2px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 7px 7px 15px #d1d9e6, -7px -7px 15px #ffffff;
        border-color: #4CAF50;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 3px 3px 8px #d1d9e6, -3px -3px 8px #ffffff;
    }
    
    /* Matched cards styling */
    .matched-card {
        background: linear-gradient(145deg, #c8e6c9, #a5d6a7) !important;
        border-color: #4CAF50 !important;
        animation: pulse 0.5s ease-in-out;
    }
    
    /* Card back styling */
    .card-back {
        background: linear-gradient(145deg, #90caf9, #64b5f6) !important;
        border-color: #2196F3 !important;
    }
    
    /* Revealed card styling */
    .revealed-card {
        background: linear-gradient(145deg, #fff3e0, #ffe0b2) !important;
        border-color: #FF9800 !important;
        animation: flip 0.6s ease-in-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes flip {
        0% { transform: rotateY(0deg); }
        50% { transform: rotateY(90deg); }
        100% { transform: rotateY(0deg); }
    }
    
    /* Game title styling */
    .game-title {
        text-align: center;
        font-size: 3rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FECA57);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        margin-bottom: 20px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 5px 5px 10px #d1d9e6, -5px -5px 10px #ffffff;
        margin: 5px;
    }
    
    /* Game board container */
    .game-board {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Difficulty buttons */
    .difficulty-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .difficulty-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize the game state
def init_game(difficulty='medium'):
    if difficulty == 'easy':
        emojis = ["🐶", "🐱", "🐭", "🐹"]
        grid_size = (2, 4)
    elif difficulty == 'medium':
        emojis = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"]
        grid_size = (4, 4)
    else:  # hard
        emojis = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐸", "🦁", "🐯", "🐨"]
        grid_size = (4, 6)
    
    cards = emojis + emojis  # Create pairs
    random.shuffle(cards)
    total_cards = len(cards)
    
    return {
        'cards': cards,
        'revealed': [False] * total_cards,
        'matched': [False] * total_cards,
        'first_card': None,
        'second_card': None,
        'moves': 0,
        'matches': 0,
        'game_complete': False,
        'show_second_card': False,
        'last_move_time': 0,
        'difficulty': difficulty,
        'grid_size': grid_size,
        'total_pairs': len(emojis),
        'start_time': time.time(),
        'best_score': None
    }

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = init_game()

if 'best_scores' not in st.session_state:
    st.session_state.best_scores = {'easy': None, 'medium': None, 'hard': None}

def reset_game(difficulty=None):
    if difficulty is None:
        difficulty = st.session_state.game_state['difficulty']
    st.session_state.game_state = init_game(difficulty)

def handle_card_click(index):
    game = st.session_state.game_state
    
    if game['matched'][index] or game['revealed'][index]:
        return
    
    if game['show_second_card'] and time.time() - game['last_move_time'] < 1.5:
        return
    
    if game['first_card'] is None:
        game['first_card'] = index
        game['revealed'][index] = True
    
    elif game['second_card'] is None and index != game['first_card']:
        game['second_card'] = index
        game['revealed'][index] = True
        game['moves'] += 1
        game['show_second_card'] = True
        game['last_move_time'] = time.time()
        
        if game['cards'][game['first_card']] == game['cards'][game['second_card']]:
            game['matched'][game['first_card']] = True
            game['matched'][game['second_card']] = True
            game['matches'] += 1
            
            game['first_card'] = None
            game['second_card'] = None
            game['show_second_card'] = False
            
            if game['matches'] == game['total_pairs']:
                game['game_complete'] = True
                # Update best score
                current_score = game['moves']
                difficulty = game['difficulty']
                if (st.session_state.best_scores[difficulty] is None or 
                    current_score < st.session_state.best_scores[difficulty]):
                    st.session_state.best_scores[difficulty] = current_score

def check_and_hide_cards():
    game = st.session_state.game_state
    
    if (game['show_second_card'] and 
        game['first_card'] is not None and 
        game['second_card'] is not None and
        time.time() - game['last_move_time'] > 1.5):
        
        if not game['matched'][game['first_card']]:
            game['revealed'][game['first_card']] = False
            game['revealed'][game['second_card']] = False
        
        game['first_card'] = None
        game['second_card'] = None
        game['show_second_card'] = False

def get_time_elapsed():
    return int(time.time() - st.session_state.game_state['start_time'])

def get_card_class(index):
    game = st.session_state.game_state
    if game['matched'][index]:
        return "matched-card"
    elif game['revealed'][index]:
        return "revealed-card"
    else:
        return "card-back"

# Main app
st.markdown('<h1 class="game-title">🧠 Memory Card Game</h1>', unsafe_allow_html=True)

# Difficulty selection
st.subheader("🎯 Select Difficulty")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Easy (2x4)", key="easy_btn"):
        reset_game('easy')
        st.rerun()

with col2:
    if st.button("🟡 Medium (4x4)", key="medium_btn"):
        reset_game('medium')
        st.rerun()

with col3:
    if st.button("🔴 Hard (4x6)", key="hard_btn"):
        reset_game('hard')
        st.rerun()

# Game stats
game = st.session_state.game_state
st.markdown("---")



# New game button
if st.button("🔄 New Game", key="new_game"):
    reset_game()
    st.rerun()

# Check if we need to hide cards
check_and_hide_cards()

# Display the game board with enhanced styling
st.markdown('<div class="game-board">', unsafe_allow_html=True)

rows, cols_per_row = game['grid_size']
for row in range(rows):
    cols = st.columns(cols_per_row)
    for col in range(cols_per_row):
        index = row * cols_per_row + col
        
        if index < len(game['cards']):
            with cols[col]:
                card_emoji = game['cards'][index] if (game['matched'][index] or game['revealed'][index]) else "❓"
                
                # Add special styling for different card states
                button_class = get_card_class(index)
                
                if st.button(
                    card_emoji, 
                    key=f"card_{index}",
                    disabled=game['matched'][index],
                    help=f"Card {index + 1}"
                ):
                    handle_card_click(index)

st.markdown('</div>', unsafe_allow_html=True)

# Game completion with enhanced celebration
if game['game_complete']:
    st.balloons()
    
    # Calculate performance
    time_taken = get_time_elapsed()
    performance = "🌟 Perfect!" if game['moves'] == game['total_pairs'] else "🎯 Great job!"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: linear-gradient(45deg, #FFD700, #FFA500); 
                border-radius: 15px; margin: 20px 0;">
        <h1>🎉 Congratulations!</h1>
        <h2>{performance}</h2>
        <p><strong>Time:</strong> {time_taken} seconds</p>
        <p><strong>Moves:</strong> {game['moves']}</p>
        <p><strong>Efficiency:</strong> {round((game['total_pairs'] / game['moves']) * 100)}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Play Again"):
        reset_game()
        st.rerun()

# Auto-refresh for card animations
if game['show_second_card']:
    time.sleep(0.1)
    st.rerun()

# Enhanced instructions
with st.expander("ℹ️ How to Play & Tips"):
    st.markdown("""
    ### 🎮 **How to Play**
    1. **Click cards** to reveal the hidden emojis
    2. **Find matching pairs** - when you find two identical emojis, they stay face up
    3. **Memory challenge** - non-matching cards flip back after 1.5 seconds
    4. **Complete the game** by finding all pairs in as few moves as possible!
    
    ### 🧠 **Pro Tips**
    - 💡 **Focus on corners first** - easier to remember positions
    - 🔄 **Create mental patterns** - group similar locations
    - ⚡ **Work systematically** - don't randomly click everywhere
    - 🎯 **Perfect score** = number of moves equals number of pairs
    
    ### 🏆 **Difficulty Levels**
    - 🟢 **Easy**: 2×4 grid (4 pairs) - Perfect for beginners
    - 🟡 **Medium**: 4×4 grid (8 pairs) - Balanced challenge  
    - 🔴 **Hard**: 4×6 grid (12 pairs) - Memory master level
    """)

# Add some fun stats
with st.expander("📊 Session Stats"):
    total_games = sum(1 for score in st.session_state.best_scores.values() if score is not None)
    if total_games > 0:
        st.write(f"🎮 **Games Played:** {total_games}")
        for difficulty, score in st.session_state.best_scores.items():
            if score is not None:
                st.write(f"🏆 **Best {difficulty.title()}:** {score} moves")
    else:
        st.write("🎯 Complete your first game to see stats!")