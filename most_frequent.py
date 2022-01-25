import json
with open('answers.txt') as file:
	word_list = [line.rstrip() for line in file]

counts = {}
for word in word_list:
	for c in word:
		if c in counts:
			counts[c] += 1
		else:
			counts[c] = 1

counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
print(json.dumps(counts))

