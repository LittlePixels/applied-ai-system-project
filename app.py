import streamlit as st
from logic_utils import get_range_for_difficulty, get_attempt_limit, generate_secret, parse_guess, check_guess, update_score


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# ── Sidebar (shared settings) ─────────────────────────────────────────────────
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

tab_human, tab_agents = st.tabs(["👤 Human Game", "🤖 Agent Battle"])

# ── Human Game Tab ────────────────────────────────────────────────────────────
with tab_human:
    if "secret" not in st.session_state:
        # Fix 9: generate_secret() moved to logic_utils.py; removed import random from app.py
        st.session_state.secret = generate_secret(difficulty)

    if "attempts" not in st.session_state:
        # Fix 5: was initialized to 1, causing first submit to count as attempt 2
        st.session_state.attempts = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "status" not in st.session_state:
        st.session_state.status = "playing"

    if "history" not in st.session_state:
        st.session_state.history = []

    st.subheader("Make a guess")

    # Fix 7: was hardcoded "between 1 and 100" regardless of difficulty
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )

    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("You already won. Start a new game to play again.")
        else:
            st.error("Game over. Start a new game to try again.")
    else:
        raw_guess = st.text_input(
            "Enter your guess:",
            key=f"guess_input_{difficulty}"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            submit = st.button("Submit Guess 🚀")
        with col2:
            new_game = st.button("New Game 🔁")
        with col3:
            show_hint = st.checkbox("Show hint", value=True)

        if new_game:
            st.session_state.attempts = 0
            st.session_state.secret = generate_secret(difficulty)
            # Fix 6: new game previously left status as "won"/"lost", making the game unplayable
            st.session_state.status = "playing"
            st.session_state.history = []
            st.success("New game started.")
            st.rerun()

        if submit:
            st.session_state.attempts += 1

            ok, guess_int, err = parse_guess(raw_guess)

            if not ok:
                st.session_state.history.append(raw_guess)
                st.error(err)
            else:
                st.session_state.history.append(guess_int)

                # Fix 2: was converting secret to str on even attempts, breaking numeric comparison
                secret = st.session_state.secret

                outcome, message = check_guess(guess_int, secret)

                if show_hint:
                    st.warning(message)

                st.session_state.score = update_score(
                    current_score=st.session_state.score,
                    outcome=outcome,
                    attempt_number=st.session_state.attempts,
                )

                if outcome == "Win":
                    st.balloons()
                    st.session_state.status = "won"
                    st.success(
                        f"You won! The secret was {st.session_state.secret}. "
                        f"Final score: {st.session_state.score}"
                    )
                else:
                    if st.session_state.attempts >= attempt_limit:
                        st.session_state.status = "lost"
                        st.error(
                            f"Out of attempts! "
                            f"The secret was {st.session_state.secret}. "
                            f"Score: {st.session_state.score}"
                        )

# ── Agent Battle Tab ──────────────────────────────────────────────────────────
with tab_agents:
    st.subheader("🤖 Agent vs Agent Battle")
    st.markdown(
        "**Proposer Agent** (Claude) secretly picks a number. "
        "**Guesser Agent** (Claude) uses hints to find it via binary search.\n\n"
        f"Range: **{low}–{high}** · Max attempts: **{attempt_limit}**"
    )

    if st.button("⚔️ Run Agent Battle"):
        from agents import run_agent_battle

        with st.spinner("Agents are battling…"):
            result = run_agent_battle(difficulty)

        secret = result["secret"]
        rounds = result["rounds"]
        winner = result["winner"]

        st.markdown(f"### Secret number chosen by Proposer: `{secret}`")
        st.markdown("---")

        for r in rounds:
            icon = "✅" if r["outcome"] == "Win" else ("🔼" if r["outcome"] == "Too Low" else "🔽")
            st.markdown(
                f"**Attempt {r['attempt']}** — Guesser guesses `{r['guess']}` → {icon} _{r['message']}_"
            )

        st.markdown("---")
        if winner == "Guesser":
            st.balloons()
            st.success(f"🎉 Guesser Agent won in {len(rounds)} attempt(s)!")
        else:
            st.error(f"💀 Proposer Agent wins! Guesser couldn't crack it in {attempt_limit} attempts.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
