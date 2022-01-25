import os, re, json
from os.path import exists

word_file = "yougowords_5letter.txt"

def create_list():
	regex = re.compile('[^a-zA-Z]')
	result = []
	with open(word_file,'r') as file:   
		for line in file:       
			for word in line.split():       
				# to lower case
				word = word.lower()
				# strip non-alpha char's
				#First parameter is the replacement, second parameter is your input string
				word = regex.sub('', word)
				# skip non-5 letter words (the file has some 'and's in it)
				if len(word)==5:
					result.append(word)
	return result

def get_hint(guess, target):
	multiplier = 3
	result = 0
	for i in range(0,len(target)):
		result = result * 3
		if guess[i]==target[i]:
			result = result + 2 # green
		elif target.find(guess[i]) >= 0:
			result = result + 1 # yellow
		# else grey
	return result
		
# '--yg-' -> 1*9+2*3 = 15
def hint_value_from_string(s):
	multiplier = 3
	result = 0
	for i in range(0,len(s)):
		result = result * 3
		if s[i]=='g':
			result = result + 2 # green
		elif s[i]=='y':
			result = result + 1 # yellow
		# else grey
	return result
	

# A guess partitions a set of possible targets according to the hint
# that Wordle returns
def partition(guess, possible_answers):
	partition = {}
	for target in possible_answers:
		hint = get_hint(guess, target) # returns a number 1->243
		hint_set = partition.get(hint, [])
		hint_set.append(target)
		partition[hint]=hint_set
	return partition

def rank_partition(partition):
	result = 0
	total = 0
	for value in partition.values():
		n = len(value)
		result = result + n*n
		total = total + n
	return result/total

def optimize_guess(possible_guesses, possible_answers):
	min_rank = None
	best_guess = None
	best_partition = None
	for guess in possible_guesses:
		partition_for_guess = partition(guess, possible_answers)
		guess_rank = rank_partition(partition_for_guess)
		if min_rank == None or guess_rank < min_rank:
			min_rank = guess_rank
			best_guess = guess
			best_partition = partition_for_guess
	return {"guess":best_guess, "partition":best_partition}
	
FIRST_GUESS_FILE = "first_guess.json"

def main():
	words = create_list()
	if not exists(FIRST_GUESS_FILE):
		optimal_partition = optimize_guess(words, words)
		with open(FIRST_GUESS_FILE, "w") as outfile:
			json.dump(optimal_partition, outfile)
	with open(FIRST_GUESS_FILE) as infile:
		initial_guess = json.load(infile)
	possible_answers = words
	for i in range(0,5):
		print(f"There are {len(possible_answers)} possible answers.")
		if len(possible_answers)<20:
			print(f"\t{possible_answers}")
		# get result of user placing guess
		if i==0:
			best_guess = initial_guess
			best_partition = {}
			for key in initial_guess["partition"].keys():
				best_partition[int(key)] = initial_guess["partition"][key]
		else:
			# best_guess = optimize_guess(words, possible_answers) <<< ANY word can be a guess
			best_guess = optimize_guess(possible_answers, possible_answers) # <<< ONLY guess a possible answer
			best_partition = best_guess["partition"]
		print(f"Guess {best_guess['guess']}")
		
		wordle_response = input("Enter wordle's response: ")
		wordle_hint = hint_value_from_string(wordle_response)
		possible_answers = best_partition[wordle_hint]
		if len(possible_answers)<2:
			break
	print(f"Possible answers: {possible_answers}.")

if __name__ == "__main__":
    main()
	