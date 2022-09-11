import pickle
import dill
from collections import defaultdict
with open("text", "rb") as fp:  # Unpickling
    text = pickle.load(fp)  # получили двойной список, где в каждом списке - слова разбитого предложения


# %%
class N_gram_model:
    def __init__(self, n, data):
        self.n = n  # кол-во n-грам
        self.text = data

    def split_text_to_ngram(self, h):   # метод разделяет каждое предложение на n-gram размера h
        data = []
        cl_text = self.text
        for sent in cl_text:
            list_of_n_gram = []
            tokens = (h - 1) * ['<start>'] + sent
            k = 0
            while k != (len(tokens) - h + 1):
                context = tuple(tokens[k:k + h][:h - 1])
                cur_word = tuple([tokens[k:k + h][-1]])
                n_gram = (context,) + cur_word
                list_of_n_gram.append(n_gram)
                k += 1
            data.append(list_of_n_gram)
        return data

    def get_ngram_per_n(self):  # метод возвращает словарь значений n-gram c ключом для размера n (от n до 2)
        n_gram = {}
        n = self.n
        for k in range(n, 1, -1):
            n_gram[(k,)] = self.split_text_to_ngram(k)
        return n_gram

    @staticmethod
    def prob(data):
        '''
        метод возвращает вложенный словарь - вероятность встречи слова из сооответсвующего контекста
        # {context : {w1: p1, w2: p2}}
        '''
        counts = defaultdict(lambda: defaultdict(lambda: 0.0))
        for sent in data:
            for n_gram in sent:
                counts[n_gram[0]][n_gram[1]] += 1
        proba = defaultdict(lambda: defaultdict(lambda: 0.0))
        for context in counts.keys():
            denominator = 0
            for w in counts[context].keys():
                denominator += counts[context][w]
            for w in counts[context].keys():
                proba[context][w] = counts[context][w] / denominator
        return proba

    def fit(self):  # метод вычисляет вероятности встречи слов для каждого n-gram-a размера от n до 2
        model_ = {}
        n_gram = self.get_ngram_per_n()
        for key in n_gram:
            model_[key] = self.prob(n_gram[key])
        return model_


# %%
model = N_gram_model(5, text)

# %%
models = model.fit()

with open('output.dill', 'wb') as f:
    dill.dump(models, f)

