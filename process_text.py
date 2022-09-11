import re
import pickle

with open("1866_dostoevskiy_prestuplenie_i_nakazanie.txt", "r") as file:
    data1 = file.read()
with open("idiot.txt", "r") as file:
    data2 = file.read()
with open("avidreaders.ru__geroy-nashego-vremeni.txt", "r") as fi:
    data3 = fi.read()
data = data1 + data2 + data3


def get_text(text):
    text = " ".join(text.split())
    text = re.split("\. |\.\.\. |\? |\! |\« |\» ", text)
    a = [ch for ch in "ауоыиэяюёеъь"]
    b = [ch for ch in "бвгджзйклмнпрстфхцчшщ"]
    text = [re.sub(r'[^\w\s]', ' ', sent) for sent in text]
    text_ = []
    for sent in text:
        sent = sent.split()
        sent = [word.lower() for word in sent]
        sent_ = []
        for word in sent:
            w = []
            for ch in word:
                if ch in a or ch in b:
                    w.append(ch)
            w = "".join(w)
            w = w.replace("ѐ", "e")
            if len(w) != 0:
                sent_.append(w)
        text_.append(sent_)
    return text_


text = get_text(data)

with open("text", "wb") as fp:
    pickle.dump(text, fp)

# %%
