from emoji_processing import is_emoji, get_emoji_reaction, replace_hidden_emoji


def is_reacted_message(m, writers):
    for w in writers:
        if m.endswith(w):
            emoji_position = len(m) - len(w) - 2
            emoji_ = m[emoji_position]
            if is_emoji(emoji_):
                return emoji_
    return None


def delete_reaction_end(m, writers):
    for w in writers:
        emoji = get_emoji_reaction(m, w)
        if emoji:
            return m[:len(m)-len(w)-2]
    return m


def get_messages_which_was_reacted_to(writers, names, messages, w):
    reacted_messages = []
    reactions = []
    reactors = []
    for i, m in enumerate(messages):
        if is_reacted_message(m, writers) and names[i] == w:
            reacted_messages.append(replace_hidden_emoji(
                delete_reaction_end(m, writers)))
            for writer in writers:
                emoji = get_emoji_reaction(m, writer)
                if emoji:
                    reactions.append(emoji)
                    reactors.append(writer)
                    break
    return list(zip(reacted_messages, reactions, reactors))


def get_reactions_to_messages(writers, names, messages):
    reactions = {}
    for writer in writers:
        reactions[writer] = get_messages_which_was_reacted_to(
            writers, names, messages, writer)
    return reactions


def get_emoji_reaction_count(writers, names, messages):
    emoji_reactions = {}
    reactions = get_reactions_to_messages(writers, names, messages)
    for writer in writers:
        emoji_reactions[writer] = {}
        for r in reactions[writer]:
            reaction = r[1]
            emoji_reactions[writer][reaction] = emoji_reactions[writer].get(
                reaction, 0) + 1
    return emoji_reactions
