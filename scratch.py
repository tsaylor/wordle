import string
from pprint import pprint as pp
import functools, itertools

def generate_wordlist():
    with open('wordle-wordlist.txt') as f:
    # with open('wordlist.txt') as f:
        return [w for w in f.read().strip().split('\n') if set(w).issubset(set(string.ascii_lowercase))]


def generate_letter_frequency(words):
    letter_incidence = {}
    for letter in string.ascii_lowercase:
        letter_incidence[letter] = 0
        for word in words:
            if letter in word:
                letter_incidence[letter] += 1
    return letter_incidence

# for a in string.ascii_lowercase:
#     for b in string.ascii_lowercase:
#         for c in string.ascii_lowercase:
#             for d in string.ascii_lowercase:
#                 for e in string.ascii_lowercase:

def match_quality(guess, the_word):
    result = {'guess': guess, 'the_word': the_word, 'exact': [], 'misplaced': [], 'wrong':[]}
    for idx, letter in enumerate(guess):
        if letter in the_word:
            if guess[idx] == the_word[idx]:
                result['exact'].append(letter)
            else:
                result['misplaced'].append(letter)
        else:
            result['wrong'].append(letter)
    return result


def is_guess_wrong(guess, the_word):
    """ quick check for no matches at all in the guess """
    return set(guess).isdisjoint(set(the_word))


def filter_words_remaining(guess, words):
    return [word for word in words if guess != word and not is_guess_wrong(guess, word)]


def dict_to_sorted_list(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)

def ppdict(d, limit=-1):
    pp(dict_to_sorted_list(d)[:limit])


# filter wordlist to words without excluded chars
# filter wordlist to words with required chars
# score letters by frequency rank
# sort words by sum of letter score

def filter_wordsets(letterset, wordsets_):
    """ return words that include all provided letters """
    letterset = set(letterset)
    if len(letterset) == 0:
        return wordsets_
    return {ws: w for (ws, w) in wordsets_.items() if letterset <= ws}

def exclude_wordsets(letterset, wordsets_):
    """ return words that include none of the provided letters """
    letterset = set(letterset)
    if len(letterset) == 0:
        return wordsets_
    return {ws: w for (ws, w) in wordsets_.items() if ws.isdisjoint(letterset)}

def exclude_repeated_letters(wordsets_):
    return {ws: w for (ws, w) in wordsets_.items() if len(ws) == len(w)}

def filter_repeated_letters(wordsets_):
    return {ws: w for (ws, w) in wordsets_.items() if len(ws) != len(w)}

def generate_word_scores(words, letter_frequency):
    max_frequency = max(letter_frequency.values())
    letter_scores = {letter: letter_frequency[letter]/max_frequency for letter in letter_frequency}
    word_scores = {w: sum(map(letter_scores.get, w)) for w in words}
    return word_scores

def suggest_guesses(required, excluded, candidates):
    # print("total: ", len(wordsets))
    candidates = exclude_wordsets(excluded, candidates)
    # print("w/o exclusions: ", len(candidates))
    candidates = filter_wordsets(required, candidates)
    # print("w/ requireds: ", len(candidates))

    if len(candidates) > 0:
        scored_candidates = generate_word_scores(
            candidates.values(),
            generate_letter_frequency(candidates.values())
        )
        print(f"\nBest guesses (10 of {len(candidates)})")
        ppdict(scored_candidates, limit=10)
    else:
        print("\nAll words filtered out! Check your inputs.")

    no_repeat_candidates = exclude_repeated_letters(candidates)
    # print("w/o repeats: ", len(candidates))
    if len(no_repeat_candidates) > 0:
        scored_candidates = generate_word_scores(
            no_repeat_candidates.values(),
            generate_letter_frequency(no_repeat_candidates.values())
        )
        print(f"\nBest guesses w/o repeats (10 of {len(no_repeat_candidates)})")
        ppdict(scored_candidates, limit=10)
    else:
        print("\nWithout repeats, all words are filtered out")


if __name__ == "__main__":
    words = generate_wordlist()
    wordsets = {frozenset(w): w for w in words}
    letter_incidence = generate_letter_frequency(words)
    # pp(sorted(letter_incidence.items(), key=lambda x: x[1], reverse=True))
    # ppdict(letter_incidence)
    # print(match_quality("rusty", "raise"))
    # print(match_quality("indie", "rusty"))
    print("suggest_guesses('', '', wordsets) # required, excluded")
    suggest_guesses('', '', wordsets)
    # print(filter_words_remaining("proxy", words))
    # words_remaining = {guess: len(filter_words_remaining(guess, words)) for guess in words}
    # ppdict(words_remaining)

    # guess_quality = []
    # for guess in words:
    #     partial_matches = len(filter_words_remaining(guess, words))
    #     total_misses = len(words) - 1 - partial_matches
    #     guess_quality.append({
    #         'guess': guess,
    #         'partial_matches': partial_matches,
    #         'total_misses': total_misses
    #     })
    # pp(guess_quality)
    # for guess in guess_quality:
    #     print("{}, {}, {}".format(*guess.values()))

    # info_from_guess = []
    # for guess in words:
    #     exact = 0
    #     misplaced = 0
    #     for the_word in words:
    #         mq = match_quality(guess, the_word)
    #         exact += len(mq['exact'])
    #         misplaced += len(mq['misplaced'])
    #     info_from_guess.append((guess, exact/len(words), misplaced/len(words)))
    # for guess in info_from_guess:
    #     print("{}, {}, {}".format(*guess))

    # words_without_letter = {}
    # for l in itertools.combinations(string.ascii_lowercase, 3):
    #     letters = set(l)
    #     c = len([w for w in wordsets if letters.isdisjoint(w)])
    #     words_without_letter[l] = c
    # ppdict(words_without_letter)
    #
    # words_with_letter = {}
    # for l in itertools.combinations(string.ascii_lowercase, 3):
    #     letters = set(l)
    #     c = len([w for w in wordsets if letters <= w])
    #     if c > 10:
    #         words_with_letter[l] = c
    # ppdict(words_with_letter)
