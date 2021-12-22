import json
from wiki_ru_wordnet import WikiWordnet
import re
import pymorphy2


morph = pymorphy2.MorphAnalyzer()
wikiwordnet = WikiWordnet()


def has_latin(text):
    return bool(re.search('[a-zA-Z]', text))


with open('decor_data.json', encoding='utf-8') as f:
    json_docs = json.load(f)
    words = []
    for item in json_docs:
        words.append(item["product_name"])

f.close()



list_of_syn = []
with open('word.txt', 'w', encoding='utf-8') as f:
    for sent in words:
        word = sent.split()
        for w in word:
            w = morph.parse(w)[0]
            w = w.normal_form
            if w.isalpha() and not (has_latin(w)) and w not in list_of_syn:
                list_of_syn.append(w)
                print(w)
                try:
                    synsets = wikiwordnet.get_synsets(w.lower())
                    synset1 = synsets[0]
                    synset1.get_words()
                    l_of_w = list(synset1.get_words())
                    syn_count = len(synset1.get_words())
                    if syn_count > 1:
                        for syn in synset1.get_words():
                            if syn_count == len(synset1.get_words()):
                                f.write(f'{syn.lemma()}|1.0')
                            else:
                                f.write(f',{syn.lemma()}|0.8')
                            syn_count -= 1
                        f.write('\n')
                except IndexError:
                    continue
f.close()

