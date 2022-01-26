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
	return set(result) # eliminate duplicates
	
	
	
def get_hint(guess, target):
	return hint_value_from_string(get_hint_as_string(guess, target))
	
# return the number of time 'character' occurs in 'target_string'
def char_count(target_string, character):
	return sum(map(lambda x : 1 if character in x else 0, target_string))

# If a guess has multiple copies of a letter but the answer has just
# one copy, then only one of the letters will be illuminated.
def get_hint_as_string(guess, target):
	#TODO raise exception if guess and target are not 5 letters
	result = ['-','-','-','-','-'] 
	unique_chars_in_guess = set([char for char in guess])
	for guess_char in unique_chars_in_guess:
		exact_match_ctr = 0
		for i in range(0, len(guess)):
			if guess[i]==guess_char and target[i]==guess_char:
				result[i]='g'
				exact_match_ctr = exact_match_ctr + 1
		# count the number of time guess_char is in **target** and subtract 'exact_match_ctr'
		remaining_char_count = char_count(target, guess_char) - exact_match_ctr
		# go through and tag as 'y' up to remaining_char_count instances of guess_char 
		# where they don't exactly match target
		imperfect_match_ctr = 0
		for i in range(0, len(guess)):
			if imperfect_match_ctr >= remaining_char_count:
				break
			if guess[i]==guess_char and target[i]!=guess_char:
				# so 'guess_char' is at pos'n i in guess, it's not an exact
				# match, but since we did not 'break' (above), there is *some*
				# unlabeled place in target where 'guess_char' occurs

				result[i]='y'
				imperfect_match_ctr = imperfect_match_ctr + 1
				
	return "".join(result)
		
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
	
NUM_GOOD_GUESSES = 5

def optimize_guess(possible_guesses, possible_answers):
	result = [] # a list of dict's with keys, 'rank', 'guess', 'partition'
	for guess in possible_guesses:
		partition_for_guess = partition(guess, possible_answers)
		guess_rank = rank_partition(partition_for_guess)
		guess_entry = {'rank':guess_rank, 'guess':guess, 'partition':partition_for_guess}
		#print(f"Guess {guess} has rank {guess_rank}")
		inserted=False
		for i in range(0, len(result)):
			if guess_rank < result[i]['rank']:
				result.insert(i,guess_entry)
				inserted=True
				result = result[0:NUM_GOOD_GUESSES]
				break
		if not inserted and len(result)<NUM_GOOD_GUESSES:
			result.append(guess_entry)
			
	return result
	
FIRST_GUESS_FILE = "first_guess.json"

def rank_all_words():
	words = create_list()
	initial_guesses = read_initial_guess_file()
	stats = {}
	target_counter = 0
	for target in words:
		guesses = []
		possible_answers = words
		guess_counter = 0
		while guess_counter < 10:
			if guess_counter==0:
				best_guesses = initial_guesses
			else:
				best_guesses = optimize_guess(words, possible_answers)
			best_guess = best_guesses[0] # just pick the top guess
			wordle_hint = get_hint(best_guess['guess'], target)
			possible_answers = best_guess['partition'][wordle_hint]
			guess_counter = guess_counter + 1
			guesses.append(best_guess['guess'])
			if best_guess['guess']==target:
				break
		target_counter = target_counter + 1
		if target_counter % 100 == 0:
			print(f"target_counter {target_counter}")
		stats[guess_counter] = stats.get(guess_counter,0)+1
		#print(f"Target word {target} is guessed in {guess_counter} guesses: {guesses}.")
	print(stats)
			
def read_initial_guess_file():
	with open(FIRST_GUESS_FILE) as infile:
		initial_guesses = json.load(infile)
		# The JSON package turns our int keys into strings, so we have to fix them
		for initial_guess in initial_guesses:
			best_partition = {}
			for key in initial_guess["partition"].keys():
				best_partition[int(key)] = initial_guess["partition"][key]
			initial_guess["partition"] = best_partition
	return initial_guesses

def main():
	if False: # rank all words
		rank_all_words()
		return 0
	# interactive application
	words = create_list()
	if not exists(FIRST_GUESS_FILE):
		best_guesses = optimize_guess(words, words)
		with open(FIRST_GUESS_FILE, "w") as outfile:
			json.dump(best_guesses, outfile)
	initial_guesses = read_initial_guess_file()
			
	possible_answers = words
	for i in range(0,5):
		print(f"There are {len(possible_answers)} possible answers.")
		if len(possible_answers)<20:
			print(f"\t{possible_answers}")
		# get result of user placing guess
		if i==0:
			best_guesses = initial_guesses
		else:
			# best_guess = optimize_guess(words, possible_answers) <<< ANY word can be a guess
			best_guesses = optimize_guess(possible_answers, possible_answers) # <<< ONLY guess a possible answer
		
		print(f"\nTop guesses: ", end='')
		for guess in best_guesses:
			print(guess['guess'], end=' ')
		print('')
		chosen_guess = input("Enter your guess: ")
		best_partition = None
		for guess in best_guesses:
			if guess['guess']==chosen_guess:
				best_partition = guess["partition"]
		if best_partition is None:
			raise Exception("You must choose one of the suggested guesses.")
				
		wordle_response = input("Enter wordle's response (5 chars of 'g', 'y', or '-'): ")
		wordle_hint = hint_value_from_string(wordle_response)
		possible_answers = best_partition[wordle_hint]
		if len(possible_answers)<2:
			break
	if len(possible_answers)==1:
		print(f"The answer is: {possible_answers[0]}.")
	else:
		print(f"Possible answers: {possible_answers}.")

if __name__ == "__main__":
    main()
	