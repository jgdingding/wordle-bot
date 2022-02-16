# Wordle Bot
Simple bot using basic linguistics and statistics to determine the best guess for Wordle

# Usage
`python3 wordle2.py`
Enter your guess and pattern with '.' representing gray, 'y' representing yellow, and 'g' representing green. 

## Example Run
```
python3 wordle2.py
Guess: crane
Result: g.y.g
Possible Words:
[('caste', 260),
 ('cause', 242),
 ('cable', 234),
 ('cache', 196),
 ('comae', 172),
 ('cavie', 164),
 ('coxae', 158),
 ('calve', 154),
 ('cadge', 150),
 ('cymae', 145)]
 
 
****************************************
```

# Heuristic
The number next to each word suggestion is based on a custom heuristic function. The function considers the following
1. Frequency of the letters used to make the word relative to the English language (by percentage)
1. Number of unique characters for the word (to extract as much information from each guess as possible)
1. Whether or not the word is considered "common"

# Simulator
`simulator.py` will run 3088 games of Wordle, with the bot choosing the best option according to the heuristic each time. 
Users can tweak their starting word and the heuristic function to try to optimize the bot.

*Note: wordlists are not the official Wordle lists, results may differ*
