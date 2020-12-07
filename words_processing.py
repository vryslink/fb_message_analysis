import itertools
from emoji_processing import is_emoji_word


def get_writers_words(messages, names):
    writers_words = {}
    for i in range(len(messages)):
        writer = names[i]
        words = messages[i].split()
        for word in words:
            writers_words[writer] = writers_words.get(
                writer, []) + [word.lower()]
    return writers_words


def get_chars(words_list):
    chars = {}
    for word in words_list:
        for c in word:
            chars[c] = chars.get(c, 0) + 1
    return chars


def get_bow(words_list):
    bag_of_words = {}
    for line in words_list:
        if line in bag_of_words:
            bag_of_words[line] += 1
        else:
            bag_of_words[line] = 1

    return dict(sorted(bag_of_words.items(), key=lambda item: item[1], reverse=True))


def get_n_grams(words_list, n=2):
    buffer = []
    n_grams = {}
    for word in words_list:
        buffer.append(word)

        if len(buffer) == n:
            n_gram_tuple = tuple(buffer)
            buffer = [buffer[-1]]

            if n_gram_tuple in n_grams:
                n_grams[n_gram_tuple] += 1
            else:
                n_grams[n_gram_tuple] = 1
    return n_grams


def get_messages_containing(messages, word):
    ms = []
    for m in messages:
        for w in m.split():
            if w.lower() == word.lower():
                ms.append(m)
    return ms


def get_most_n_grams(writers, messages, names, stopwords=[], count=10, n=2):
    writers_words = get_writers_words(messages, names)
    most_used_ngrams = {}
    for writer in writers:
        words = writers_words[writer]
        if stopwords:
            words = [word for word in writers_words[writer]
                     if word not in stopwords]

        my_words = get_n_grams(words, n=n)
        sorted_words = dict(
            sorted(my_words.items(), key=lambda item: item[1], reverse=True))
        sliced_words = dict(itertools.islice(sorted_words.items(), count))

        most_used_ngrams[writer] = sliced_words

    return most_used_ngrams


def most_used_words(writers, messages, names, stopwords=[], count=10):
    writers_words = get_writers_words(messages, names)
    most_used_words = {}
    for writer in writers:
        words = writers_words[writer]
        if stopwords:
            words = [word for word in writers_words[writer]
                     if word not in stopwords]

        my_words = get_bow(words)
        sorted_words = dict(
            sorted(my_words.items(), key=lambda item: item[1], reverse=True))
        sliced_words = dict(itertools.islice(sorted_words.items(), count))

        most_used_words[writer] = sliced_words

    return most_used_words


def get_freq_dict(writers, messages, names, stopwords=[]):
    writers_words = get_writers_words(messages, names)
    words = []
    for writer in writers:
        new_words = writers_words[writer]
        new_words = [word for word in new_words if not is_emoji_word(word)]

        if stopwords:
            words = [word for word in new_words if word not in stopwords]
        words += new_words

    my_words = get_bow(words)
    sorted_words = dict(
        sorted(my_words.items(), key=lambda item: item[1], reverse=True))

    return sorted_words
