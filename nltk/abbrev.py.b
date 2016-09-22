import re
import sys

def get_count(words, text):
    return len(re.findall(words, text))

def get_n_word_grams(n, text):
    return re.finditer(r"(?:\s*\b[a-zA-Z]+\b\s*){%d}" % n, text)

def main():
    with open("cleaned") as f:
        text = (" ").join([line.strip() for line in f.readlines()])
    to_abbr = {}
    for word_grams in [4]:
        phrases = set([m.group().strip() for m in get_n_word_grams(word_grams, text)])
        tot_p = len(phrases)
        p_ctr = 0
        for phrase in phrases:
            to_abbr[phrase] = get_count(phrase, text)
            # print("Done with", phrase, to_abbr[phrase])
            p_ctr+=1
            print(p_ctr/tot_p, file=sys.stderr)
    print([(key, to_abbr[key]) for key in sorted(to_abbr, key=lambda x: to_abbr[x])])

main()
    
