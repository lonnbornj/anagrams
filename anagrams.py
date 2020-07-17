"""
Author: Jack Lonnborn
Date: May 2019

Takes the fun out of the weekend by solving the nine-letter-word block puzzle.
Returns all anagrams of a sequence of letters and its subsequences.
"""

from collections import defaultdict
import itertools
import pickle


def build_anagrams_dict():
    """
	Returns a dictionary `anagrams_dict` which has English words as keys,
	and lists of anagrams of those words as values.
	"""
    dict_filename = "dict.pkl"
    try:
        with open(dict_filename, "rb") as f:
            anagrams_dict = pickle.loads(f.read())
    except FileNotFoundError:
        from nltk.corpus import brown

        words = brown.words()
        anagrams_dict = defaultdict(list)
        for word in words:
            key = "".join(sorted(word))
            if not word in anagrams_dict[key]:
                anagrams_dict[key].append(word.lower())
        with open(dict_filename, "wb") as f:
            pickle.dump(anagrams_dict, f)
    return anagrams_dict


def permute(letters):
    """
	Returns a list containing all ordered permutations of all substrings
	which can be formed from the characters in `letters`.
	"""
    letters = sorted(letters)
    permutations = list()
    for length, _ in enumerate(letters):
        permutations.extend(
            ["".join(sorted(p)) for p in itertools.permutations(letters, length + 1)]
        )
    permutations = sorted(set(s for s in permutations if s))
    return permutations


def find_anagrams(permutations, anagrams_dict):
    """
	Takes a set of possible permutations of a string and its substrings, and
	returns a list containing all English language anagrams of these
	permutations, reverse ordered by length.
	"""
    anagrams = list()
    anagrams.extend(
        word
        for letters in permutations
        for word in anagrams_dict[letters]
        if len(letters) > 1 or letters == "a" or letters == "i"
    )
    anagrams = list(set(anagrams))
    anagrams.sort(key=lambda k: len(k), reverse=True)
    return anagrams


def main():
    anagrams_dict = build_anagrams_dict()
    letters = input("Input the letters in the puzzle:\n").lower()
    permutations = permute(letters)
    anagrams = find_anagrams(permutations, anagrams_dict)
    print("Found {} anagrams of (substrings of) '{}':".format(len(anagrams), letters))
    print(", ".join(a for a in anagrams))


if __name__ == "__main__":
    main()
