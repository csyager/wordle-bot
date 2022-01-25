import difflib
import sys

class GuessResult():
	def __init__(self, guess: str, target: str):
		self.guess = guess
		self.result = {
			0: {
				'green': guess[0] == target[0],
				'yellow': guess[0] in target
			},
			1: {
				'green': guess[1] == target[1],
				'yellow': guess[1] in target
			},
			2: {
				'green': guess[2] == target[2],
				'yellow': guess[2] in target
			},
			3: {
				'green': guess[3] == target[3],
				'yellow': guess[3] in target
			},
			4: {
				'green': guess[4] == target[4],
				'yellow': guess[4] in target
			},
		}
		self.known_positions = {
			0: '',
			1: '',
			2: '',
			3: '',
			4: ''
		}
		self.characters_eliminated = []
		self.known_includes = []
		for i in range(5):
			c = guess[i]
			if c == target[i]:
				self.known_positions[i] = c
			if c in target and c not in self.known_includes:
				self.known_includes.append(c)
			if c not in target:
				self.characters_eliminated.append(c)
			

	def __str__(self):
		boxes = []
		for key in self.result:
			if self.result[key]['green']:
				boxes.append('G')
			elif self.result[key]['yellow']:
				boxes.append('Y')
			else:
				boxes.append('B')

		known_positions = []
		for key in self.known_positions:
			if self.known_positions[key] != '':
				known_positions.append(self.known_positions[key])
			else:
				known_positions.append("_")
		return ''.join(boxes) + '\n' + ''.join(known_positions) + "\nincludes: " + str(self.known_includes) + "\neliminated: " \
			+ str(self.characters_eliminated) + "\n--------------------------"
			
	
	def is_correct(self):
		return self.result[0]['green'] and self.result[1]['green'] and self.result[2]['green'] and self.result[3]['green'] and self.result[4]['green']


def get_char_frequency(word_list):
	counts = {}
	for word in word_list:
		for c in word:
			if c in counts:
				counts[c] += 1
			else:
				counts[c] = 1
	return counts

def get_char_frequency_by_position(word_list):
	counts = {
		0: {},
		1: {},
		2: {},
		3: {},
		4: {}
	}
	for word in word_list:
		for i in range(5):
			c = word[i]
			if c in counts[i]:
				counts[i][c] += 1
			else:
				counts[i][c] = 1
	return counts

def get_most_frequent_char_by_position(char_frequencies: dict):
	most_frequent = {}
	for key in char_frequencies:
		frequencies = char_frequencies[key]
		most_frequent[key] = max(frequencies, key=frequencies.get)
	return most_frequent

def most_frequent_chars_to_string(most_frequent_dict: dict, word_list: list):
	top_five_chars = sorted(most_frequent_dict, key=most_frequent_dict.get, reverse=True)[:5]
	scores = {}
	for word in word_list:
		score = 0
		for c in top_five_chars:
			if c in word:
				score += 1
		scores[word] = score
	return max(scores, key=scores.get)

def most_frequent_chars_by_position_to_string(most_frequent_dict: dict):
	builder = []
	for key in most_frequent_dict:
		builder.append(most_frequent_dict[key])
	return ''.join(builder)
	
def reduce_word_list(
	word_list: list, 
	guess_result: GuessResult
):
	new_word_list = []
	for word in word_list:
		if word == guess_result.guess:
			continue
		if any(char in word for char in guess_result.characters_eliminated):
			continue
		if guess_result.known_positions[0] != '' and word[0] != guess_result.known_positions[0]:
			continue
		if guess_result.known_positions[1] != '' and word[1] != guess_result.known_positions[1]:
			continue
		if guess_result.known_positions[2] != '' and word[2] != guess_result.known_positions[2]:
			continue
		if guess_result.known_positions[3] != '' and word[3] != guess_result.known_positions[3]:
			continue
		if guess_result.known_positions[4] != '' and word[4] != guess_result.known_positions[4]:
			continue
		if not all(char in word for char in guess_result.known_includes):
			continue
		new_word_list.append(word)
	return new_word_list


def guess(word_list, target) -> GuessResult:
	char_frequency_by_position = get_char_frequency_by_position(word_list)
	most_frequent_char_by_position = get_most_frequent_char_by_position(char_frequency_by_position)
	most_frequent_chars_str = most_frequent_chars_by_position_to_string(most_frequent_char_by_position)
	print(f"most_frequent_chars_str: {most_frequent_chars_str}")
	guess = difflib.get_close_matches(most_frequent_chars_str, word_list, n=1, cutoff=0.4)[0]
	print(f"Guessing {guess}")
	guess_result = GuessResult(guess, target)
	print(guess_result)
	return guess_result

def guess_by_overall_frequency(word_list, target) -> GuessResult:
	char_frequency = get_char_frequency(word_list)
	guess = most_frequent_chars_to_string(char_frequency, word_list)
	print(f"Guessing {guess}")
	guess_result = GuessResult(guess, target)
	print(guess_result)
	return guess_result

def play_game(word_list, target) -> bool:
	""" makes up to 6 guesses, eliminating words as it goes 
		returns true if the target is found
	"""
	for i in range(6):
		print(f"wordlist len: {len(word_list)}")
		guess_result = guess_by_overall_frequency(word_list, target)
		if guess_result.is_correct():
			print(f"Word {guess_result.guess} found on attempt {i}!")
			print("**************************")
			return True
		word_list = reduce_word_list(word_list, guess_result)
	
	print(f"Ran out of attempts :(")
	print(f"Target: {target}")
	print(f"Most recent guess: {guess_result.guess}")
	print("**************************")
	return False


def main():
	with open('valid_inputs.txt') as file:
		valid_inputs = [line.rstrip() for line in file]
	with open('answers.txt') as file:
		inputs = [line.rstrip() for line in file]
	valid_inputs = valid_inputs + inputs
	wins = []
	losses = []
	for input in inputs:
		print(f"Playing game with target {input}")
		found_target = play_game(valid_inputs, input)
		if found_target:
			wins.append(input)
		else:
			losses.append(input)
	
	print(f"Successes: {len(wins)}")
	print(f"Failures: {len(losses)}")

def main_with_target(target):
	with open('valid_inputs.txt') as file:
		valid_inputs = [line.rstrip() for line in file]
	with open('answers.txt') as file:
		inputs = [line.rstrip() for line in file]
	valid_inputs = valid_inputs + inputs
	print(f"Playing game with target {target}")
	play_game(valid_inputs, target)
	


if __name__ == '__main__':
	if len(sys.argv) == 1:
		main()
	else:
		main_with_target(sys.argv[1])