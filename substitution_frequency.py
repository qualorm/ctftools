from collections import Counter

with open('public/study-guide.txt','r') as f:
    data = ''.join([line.strip() for line in f.readlines()])

frequencies = Counter(data)
print(frequencies)

letters_by_freq = [k for k,_ in sorted(frequencies.items(), key=lambda item: item[1],reverse=True)]

alphabet = list('abcdefghijklmnopqrstuvwxyz')
# dictionary = dict(zip(letters_by_freq, 'etainoshrdlucmfwygpbvkqxjz')) # overall frequency
# dictionary = dict(zip(letters_by_freq, 'eariotnslcudmhgbfywkvxzjq')) # letters in oxford dict
dictionary = dict(zip(letters_by_freq, 'eianosrtlcupdmhgbfyvkwxzqj')) # by hand

print(dictionary)

with open('public/flag.txt', 'r') as g:
    ct = g.read().strip()

flag = ''
for c in ct:
    if c == '_':
        flag += c
        continue
    flag += dictionary[c]

print('picoCTF{' + flag + '}')
'''
https://quipqiup.com/
'''
