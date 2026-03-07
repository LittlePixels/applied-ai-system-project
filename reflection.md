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

A combination of Claude and ChatGPT for this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

On line 97-100 on app.py the bug in the state makes the string instead of an integer on even attempts, thus making the hint go haywire because it's string based instead of integer-based.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

On line 66-72 in logic_utils.py, the AI only swapped the emoji strings but left the outcome labels("Too High"/"Too Low" untouched. The outcome label is what drives the core, but the update_score in the lines would apply the wrong scoring logic, penalizing when guessed too high instead of too low. I verified the result by changing the logic to go when it's Too High to a Go LOWER and when it's Too Low to Go Higher.)

--- 

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

Tracing the logic such as guess > secret, meaning the guess is too high and the player needed to go lower. The original code said "Go HIGHER", which is the wrong condition. I verified by reading what the corrected code returns and confirms matching the expected behavior in passing the pytest ouput(test_guess_too_high, test_guess_too_low)
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  There seems to be a error inside of the test code. From what I have observed using pytest. All three failed with this error:
  AssertionError: assert ('Win', '🎉 Correct!') == 'Win'
The test was comparing the entire tuple to a string. The test revealed a bug within the test, and not neccessarily with the code this time considering that it has already been fixed prior due to the above mentioned.

- Did AI help you design or understand any tests? How?
Yes! By using the AI the way that the project has been made in sintructions, it has designed to break down the concepts and verify what has been seen by sight within the code. For instance, the test pointed out the failure with what had to do with the higher and lower code section on line 97-100 on app.py. This fix then clashed with the py-test, but looking further with the AI, it determined that there was a bug within the test AI as mentioned above, thus prompting it to be fixed by changing a part of the pytest app to align with the changes made in the code.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number only changed when it was prompted on certain guesses, such as the even guesses. This took the code and converted it to a string before comparing the test. For example, instead of comparing two numbers 60 > 42 it compared 60 > "42". The hints were inaccurate because the comparison logic was broken behind the scenes.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
The session state is what exist in the current memory, similar to how RAM works and survives in the rerun. In Streamlit, reruns are the entire script works again from the very top, which is called a 'rerun'.
- What change did you make that finally gave the game a stable secret number?
The number has always been stable, it was simply adjusting the string conversion on app.py 97-100 that made it consistent with the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Defiantly the way prompts are used, along with current debugging skills. This project has been teaching me how to use AI properly that it can debug certain parts of a program without having to rely blindly on prompts and taking them at their word. By learning how to diagnose properly with AI, and citing out what parts are correct and what parts can be improved, i've learned to slice into the code and use my current debugging skills along with the AI debugging to better assest a project.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
I would try the different setting available with AI. Some AI prompts have it where it automatically "fixes" things. I've decided to make it do step by step this project in order to assess the options done so that I have a clean, working project to work upon and that it runs fine.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Unlike the english-only generated code, it makes me look at what is BEHIND the code and solve it as a developer, having to look at actual code lines and pin point by using AI prompts such as #fix app.py 97-100 to pinpoint exactly where the error line is in the code and notify the AI how to fix it.
