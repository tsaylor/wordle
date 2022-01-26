# Quickstart

Run `python -i scratch.py` and then `suggest_guesses('', '', wordsets)` to generate two lists of scored guesses, one including duplicate letters and the other without. Words without duplicates are better guesses initially because they provide more information about the answer (more colored squares), but the answer may include duplicate letters, so consider both lists. As you make guesses, add green and yellow letters to the first argument, and black letters to the second. Eventually you'll only have a few words left and can guess the answer.

# How it works

`suggest_guesses(required, excluded, candidates)`
* required - a string containing any letters that the answer must have (yellow and green boxes).
* excluded - a string containing any letters that the answer may not have (black boxes).
* candidates - a dict of the word list where the words are values and the keys are `frozenset`s of that word.

`suggest_guesses` filters all possible guesses in Wordle based on the letters you know are in or not in the answer, and it rates them based on frequently the letters of the guess are seen in possible answers.

To score a guess it counts the number of words that contain each letter, normalizes those counts to the most frequently appearing letter, then sums the frequency of each letter in the word to generate the word score. The maximum score is 5.

For example, if the full word list were "artsy", "rural", and "shave", letter scoring would look like this:

| letter | freq | normalized |
| :----- | :--- | :--------- |
| a      | 3    | 1          |
| s      | 2    | .666666666 |
| r      | 2    | .666666666 |
| t      | 1    | .333333333 |
| y      | 1    | .333333333 |
| u      | 1    | .333333333 |
| l      | 1    | .333333333 |
| h      | 1    | .333333333 |
| v      | 1    | .333333333 |
| e      | 1    | .333333333 |

Then word scoring would sum those values like this:

| word  | score       |
| :---- | :---------- |
| artsy | 3           |
| rural | 3           |
| shave | 2.666666666 |

Before guessing anything, you could run `suggest_guesses('', '', wordsets)` and you'd get a list of suggested guesses very much like the above table. Then if you guessed "hoard", you might get yellow squares for "a" and "r" and black for everything else, so you could run `suggest_guesses('ar', 'hod', wordsets)` to get new suggestions. Since we know "h" isn't in the answer, "shave" will be removed and everything is recalculated, like this:

| letter | freq | normalized |
| :----- | :--- | :--------- |
| a      | 2    | 1          |
| r      | 2    | 1          |
| t      | 1    | .5         |
| s      | 1    | .5         |
| y      | 1    | .5         |
| u      | 1    | .5         |
| l      | 1    | .5         |

| word  | score       |
| :---- | :---------- |
| rural | 4           |
| artsy | 3.5         |

"rural" is now the highest rated guess, but it has a duplicate letter. If we guess "rural" it may be correct, but if it's wrong we've missed an opportunity to learn about another letter. (This would matter a lot more if we were using the full list of 2315 words instead of the three in this example.) 
