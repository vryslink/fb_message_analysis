
from stopwords import get_stopwords
from bs4 import BeautifulSoup

from emoji_processing import replace_hidden_emoji
from message_reactions import delete_reaction_end


stopwords = get_stopwords()


def read_file(filepath=None, text=None):
    if filepath:
        with open(filepath, "r") as f:
            lines = f.readlines()
    elif text:
        lines = [text]
    else:
        raise Exception("Neither text or filepath was entered")

    soup = BeautifulSoup(lines[0], "html.parser")
    names = [n.text for n in soup.findAll(
        "div", {"class": "_3-96 _2pio _2lek _2lel"})]
    messages = [m.text for m in soup.findAll("div", {"class": "_3-96 _2let"})]
    times = [t.text for t in soup.findAll("div", {"class": "_3-94 _2lem"})]

    names.reverse()
    times.reverse()
    messages.reverse()

    return list(zip(names, times, messages)), names, times, messages


def get_writers_messages(messages, names):
    writers_messages = {}
    for i in range(len(messages)):
        writers_messages[names[i]] = writers_messages.get(
            names[i], []) + [messages[i]]
    return writers_messages


def get_data(filepath=None, text=None):
    data, n, t, m = read_file(filepath, text)
    names, times, messages = [], [], []
    for i in range(len(data)):
        if t and n:
            names.append(n[i])
            times.append(t[i])
            messages.append(replace_hidden_emoji(m[i]))

    writers = list(set(names))
    messages_without_reactions = [replace_hidden_emoji(
        delete_reaction_end(m, writers)) for m in messages]

    return names, times, writers, messages, messages_without_reactions
