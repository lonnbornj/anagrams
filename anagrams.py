"""
Filename: anagrams.py
Author: Jack Lonnborn
Date: May 2019
Purpose: Takes the fun out of the weekend by solving the nine-letter-word block puzzle. Returns all anagrams of a sequence of letters and its subsequences.
"""

from collections import defaultdict
from itertools import permutations
import pickle


def build_anagrams_dict():
	"""
	Returns a dictionary `anagrams_dict` which has English words as keys, and lists of anagrams of those words as values.
	"""
	try:
		with open("dict.txt", "rb") as f:
			anagrams_dict = pickle.loads(f.read())
	except FileNotFoundError:
		from nltk.corpus import brown
		words = brown.words()
		anagrams_dict = defaultdict(list)
		for word in words:
			key = ''.join(sorted(word))
			if not word in anagrams_dict[key]:
				anagrams_dict[key].append(word.lower())
		with open("dict.txt", "wb") as f:
			pickle.dump(anagrams_dict, f)
	return anagrams_dict

def permute(letters):
	"""
	Returns a set containing all ordered permutations of all substrings which can be formed from the characters in `letters`.
	"""
	letters = sorted(letters)
	permutns = list()
	for i in range(len(letters)+1):
		permutns.extend([''.join(sorted(p)) for p in permutations(letters,i)])
	permutns = sorted(set(sorted(s for s in permutns if s)))
	return permutns

def find_anagrams(permutations, anagrams_dict):
	"""
	Takes a set of possible permutations of a string and its substrings, and returns a list containing all English language anagrams of these permutations, reverse ordered by length.
	"""
	anagrams = list()
	anagrams.extend(l for k in permutations for l in anagrams_dict[k] if len(l)>1 or l == 'a' or l == 'i')
	anagrams = list(set(anagrams))
	anagrams.sort(key = lambda k: len(k), reverse = True)
	return anagrams

def main():
	anagrams_dict = build_anagrams_dict()
	letters = input("Input the letters in the puzzle:\n").lower()
	permutations = permute(letters)
	anagrams = find_anagrams(permutations, anagrams_dict)
	print("\nFound {} anagrams of (substrings of) '{}':".format(len(anagrams), letters))
	print(', '.join(a for a in anagrams))

if __name__ == "__main__":
	main()