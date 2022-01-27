import string
from pprint import pprint as pp
import functools, itertools


def generate_wordset():
    """Reads a word file and loads a dict: {word: set(word)}"""
    with open("wordle-wordlist.txt") as f:
        # with open('wordlist.txt') as f:
        return {
            w: set(w)
            for w in f.read().strip().split("\n")
            if set(w).issubset(set(string.ascii_lowercase))
        }


def generate_letter_frequency(words):
    letter_frequency = {}
    for letter in string.ascii_lowercase:
        letter_frequency[letter] = 0
        for word in words:
            if letter in word:
                letter_frequency[letter] += 1
    return letter_frequency


def dict_to_sorted_list(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)


def ppdict(d, limit=-1):
    pp(dict_to_sorted_list(d)[:limit])


# filter wordlist to words without excluded chars
# filter wordlist to words with required chars
# score letters by frequency rank
# sort words by sum of letter score


def filter_wordsets(letterset, words):
    """return words that include all provided letters"""
    letterset = set(letterset)
    if len(letterset) == 0:
        return words
    return {w: ws for (w, ws) in words.items() if letterset <= ws}


def exclude_wordsets(letterset, words):
    """return words that include none of the provided letters"""
    letterset = set(letterset)
    if len(letterset) == 0:
        return words
    return {w: ws for (w, ws) in words.items() if ws.isdisjoint(letterset)}


def exclude_repeated_letters(words):
    return {w: ws for (w, ws) in words.items() if len(ws) == len(w)}


def filter_repeated_letters(words):
    return {w: ws for (w, ws) in words.items() if len(ws) != len(w)}


def generate_word_scores(words, letter_frequency):
    max_frequency = max(letter_frequency.values())
    letter_scores = {
        letter: letter_frequency[letter] / max_frequency for letter in letter_frequency
    }
    word_scores = {w: sum(map(letter_scores.get, w)) for w in words}
    return word_scores


def suggest_guesses(required, excluded, candidates):
    candidates = exclude_wordsets(excluded, candidates)
    candidates = filter_wordsets(required, candidates)

    if len(candidates) > 0:
        letter_frequency = generate_letter_frequency(candidates)
        scored_candidates = generate_word_scores(candidates, letter_frequency)
        print(f"\nBest guesses (10 of {len(candidates)})")
        ppdict(scored_candidates, limit=10)
    else:
        print("\nAll words filtered out! Check your inputs.")

    no_repeat_candidates = exclude_repeated_letters(candidates)
    if len(no_repeat_candidates) > 0:
        letter_frequency = generate_letter_frequency(no_repeat_candidates)
        scored_no_repeat_candidates = generate_word_scores(
            no_repeat_candidates,
            letter_frequency,
        )
        print(f"\nBest guesses w/o repeats (10 of {len(no_repeat_candidates)})")
        ppdict(scored_no_repeat_candidates, limit=10)
    else:
        print("\nWithout repeats, all words are filtered out")

    # print('Median words')
    # scores = sorted(scored_candidates.values())
    # median_index = len(scores)//2
    # median_score = scores[median_index]
    # print(median_score)
    # print(median_index)
    # pp(dict_to_sorted_list(scored_candidates)[median_index-5:median_index+5])


# def match_quality(guess, the_word):
#     result = {'guess': guess, 'the_word': the_word, 'exact': [], 'misplaced': [], 'wrong':[]}
#     for idx, letter in enumerate(guess):
#         if letter in the_word:
#             if guess[idx] == the_word[idx]:
#                 result['exact'].append(letter)
#             else:
#                 result['misplaced'].append(letter)
#         else:
#             result['wrong'].append(letter)
#     return result
#
#
# def is_guess_wrong(guess, the_word):
#     """ quick check for no matches at all in the guess """
#     return set(guess).isdisjoint(set(the_word))
#
#
# def filter_words_remaining(guess, words):
#     return [word for word in words if guess != word and not is_guess_wrong(guess, word)]


if __name__ == "__main__":
    words = generate_wordset()
    # wordsets = {frozenset(w): w for w in words}
    letter_incidence = generate_letter_frequency(words)
    print("suggest_guesses('', '', words) # required, excluded")
    suggest_guesses("", "", words)

    # pp(sorted(letter_incidence.items(), key=lambda x: x[1], reverse=True))
    # ppdict(letter_incidence)
    # print(match_quality("rusty", "raise"))
    # print(match_quality("indie", "rusty"))
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



##### Generate num letter matches per guess (or guess set)
# allwords = ['iratelousy', 'laternoisy', 'starelunch', 'arisetouch', 'aroseuntil', 'learnsouth']
# allwords = ['irate', 'later', 'stare', 'arise', 'arose', 'learn']
# info_gathered = {}
# for twoword in allwords:
#     s = frozenset(twoword)
#     keyfunc = lambda x: len(s.intersection(words[x]))
#     info_gathered[twoword] = [
#         (k, len([words[v_] for v_ in v]))
#         for k, v in itertools.groupby(sorted(words, key=keyfunc), key=keyfunc)
#     ]
#
# for k, v in info_gathered.items():
#     print(', '.join([k, *reversed([str(i) for i in dict(v).values()])]))
