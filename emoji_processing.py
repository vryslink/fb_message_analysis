import re

from emoji import UNICODE_EMOJI


def is_emoji_word(word):
    for c in word:
        if is_emoji(c):
            return True
    return False


def replace_hidden_emoji(m):
    new_m = []
    laugh_pattern = '^.*(:[dD])+.*$'
    smile_pattern = "^.*(:\))+.*$"
    smile = re.compile(smile_pattern)
    laugh = re.compile(laugh_pattern)
    for w in m.split():
        laugh_match = laugh.search(w)
        smile_match = smile.search(w)
        new_word = w

        if laugh_match:
            splitted = w.split(":")
            if splitted[-1].lower() == "d":
                new_word = new_word[:-2] + "😀"
        elif smile_match:
            splitted = w.split(":")
            if splitted[-1].lower() == ")":
                new_word = new_word[:-2] + "😊"

        new_m.append(new_word)
    return " ".join(new_m)


def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count > 1:
            return False
    return bool(count)


def is_emoji_in_message(message):
    for c in message:
        if is_emoji(c):
            return True
    return False


def extract_emojis(s):
    emojis = []
    for word in s:
        for c in word:
            if c in ["♂", "♀"]:
                continue
            if is_emoji(c):
                emojis.append(c)
    return emojis


def get_emoji_reaction(m, w):
    if m.endswith(w):
        emoji_position = len(m) - len(w) - 2
        emoji_ = m[emoji_position]
        if is_emoji(emoji_):
            return emoji_
    return None


def get_emoji_reactions(writers, messages):
    emoji_reactions = {}
    for message in messages:
        for w in writers:
            emoji = get_emoji_reaction(message, w)
            if emoji:
                emoji_reactions[w] = emoji_reactions.get(w, []) + [emoji]
    return emoji_reactions


def get_writers_emojis(names, messages_without_reactions):
    writers_emojis = {}
    for i, m in enumerate(messages_without_reactions):
        replaced_emojis = replace_hidden_emoji(m)
        emojis = extract_emojis(replaced_emojis.split())
        if emojis:
            writers_emojis[names[i]] = writers_emojis.get(
                names[i], []) + [emojis]
    return writers_emojis


def get_used_emojis(writers, names, messages_without_reactions):
    written_emojis = get_writers_emojis(names, messages_without_reactions)
    used_emojis = {}
    for writer in writers:
        used_emojis[writer] = {}
        if writer in written_emojis.keys():
            for e in written_emojis[writer]:
                for emoji_list in e:
                    for emoji in emoji_list:
                        used_emojis[writer][emoji] = used_emojis[writer].get(
                            emoji, 0) + 1
    return used_emojis
