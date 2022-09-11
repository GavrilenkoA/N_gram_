import dill
import numpy as np

with open("output.dill", "rb") as fp:
    models = dill.load(fp)


def get_proba_distrib(model, context):
    return model[context]


def generate(all_model, n, num_of_sent, len_sent):
    """
    Функция генерирует слово в зависимости длины контекста, начинает с самого длинного (n-1)
    и если не находит спускается вплоть до длины конекста 1
    Для каждой длины контекста посчитана модель
    """
    gen_text = []
    for k in range(num_of_sent):
        sentence = []
        while len(sentence) < len_sent:
            prefix = (n - 1) * ['<start>']
            cur_prefix = prefix.copy()
            cur_prefix = tuple(cur_prefix)
            for key in all_model:
                if cur_prefix in all_model[key]:
                    proba = get_proba_distrib(all_model[key], cur_prefix)
                    break
                else:
                    cur_prefix = cur_prefix[1:]
            w = np.random.choice((list(proba.keys())), 1, p=list(proba.values()))
            sentence.append(w[0])
            prefix.append(w[0])
            prefix.pop(0)
        sentence = " ".join(sentence)
        gen_text.append(sentence)
    gen_text = " ".join(gen_text)
    return gen_text


#%%

#%%

# %%

text = generate(models, 5, 1000, 17)  # генерация 1000 предложений длины 17
# %%
with open("generated_text", "w") as fi:
    fi.write(text)