# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
The first bugs i've encountered when the game started was in the settings. The Easy, Normal, and Difficult levels all had the wrong configuration for their levels. For instance,

Hard should be range 1 100 5 attempts
Easy should be attempts 8
Normal should be range 1 to 50 with 6 attempts.

These are not the correct configuration for the game, and are in the opposite of each category. This needs to be fixed in order for the game to be started properly.

- What did the game look like the first time you ran it?
UI wise the number game looks very basic. I do not see anything else wrong with it, other than the logic behind the hinting.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When the number is higher, it says to go lower. When the number is lower, it says to go higher.
Score keeps going into negative when wrong attempt is done instead of keeping it at 0.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
