import re
from nltk.corpus import stopwords
import pandas as pd
from nltk.corpus import wordnet as wn


class Extractor():
    pattern = re.compile(r"\b[^\W\d_]+\b")
    def __init__(self,text,lang="spanish"):
        self.text = text
        self.lang = lang
        self.tokens = None

    def tokenizer(self):
        stop_words = stopwords.words(self.lang)
        self.tokens = [w for w in re.findall(Extractor.pattern,self.text) if not w.lower() in stop_words and w.isalpha()] #word_tokenize(self.text)
        return self.tokens

    def create_synset(self):
        bag_word = set(self.tokens)
        main_list = []
        for w in bag_word:
            synset = wn.synsets(w, lang=self.lang[0:3])
            synset_list = []
            for s in synset:
                for l in s.lemmas('spa'):
                    synset_list.append(l.name())
            main_list.append([w, list(set(synset_list))])
        syn_df = pd.DataFrame(main_list,columns=["Term","Synonyms"])
        syn_df = syn_df[syn_df["Synonyms"].map(len) != 0]
        return syn_df


with open("text.txt","r",encoding="utf-8") as file:
    f = file.read()
    t_ext = Extractor(f)
    t_ext.tokenizer()
    print(t_ext.create_synset())

