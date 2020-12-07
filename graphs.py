import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_processing import get_writers_messages
from emoji_processing import is_emoji_in_message, get_used_emojis
from message_reactions import get_emoji_reaction_count
from time_processing import get_writer_messages_in_a_day, get_weekdays, get_immediate_responses_count, get_conversations_starters, get_writers_timedeltas, str_to_time


def display_general_pies(writers, names, messages, nonames=False):
    writers_messages = get_writers_messages(messages, names)
    messages_count = [len(writers_messages[writers[i]])
                      for i in range(len(writers))]
    words_count = [sum([len(mes.split()) for mes in writers_messages[writers[i]]])
                   for i in range(len(writers))]
    chars_count = [sum([len(mes) for mes in writers_messages[writers[i]]])
                   for i in range(len(writers))]
    questions_count = [len([mes for mes in writers_messages[writer] if (
        '?' in mes)]) for writer in writers]
    emojis_count = [len([mes for mes in writers_messages[writer] if (
        is_emoji_in_message(mes))]) for writer in writers]
    lenghty_count = [len([mes for mes in writers_messages[writer] if (
        len(mes.split()) > 10)]) for writer in writers]

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]

    fig = go.FigureWidget(make_subplots(rows=2, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}, {
                          'type': 'domain'}]], subplot_titles=['Počet zpráv', 'Počet slov', 'Počet znaků', "Zprávy s otázkou", "Zprávy s emoji", "Zprávy > 10 slov"]))

    trace0 = go.Pie(labels=writers, values=messages_count,
                    name="Celkový počet zpráv")
    trace1 = go.Pie(labels=writers, values=words_count,
                    name='Celkový počet slov')
    trace2 = go.Pie(labels=writers, values=chars_count,
                    name="Celkový počet znaků")
    trace3 = go.Pie(labels=writers, values=questions_count,
                    name="Celkový počet otázek")
    trace4 = go.Pie(labels=writers, values=emojis_count,
                    name="Celkový počet emoji")
    trace5 = go.Pie(labels=writers, values=lenghty_count,
                    name="Celkový počet dlouhých zpráv")

    fig.add_trace(trace0, 1, 1)
    fig.add_trace(trace1, 1, 2)
    fig.add_trace(trace2, 1, 3)
    fig.add_trace(trace3, 2, 1)
    fig.add_trace(trace4, 2, 2)
    fig.add_trace(trace5, 2, 3)

    fig.update_traces(hoverinfo="label+percent", textinfo="value",
                      textfont_size=12, marker=dict(line=dict(color="black", width=2)))
    fig.update_layout(
        title_text="Statistiky o počtu zpráv, slov a znaků", width=1200, height=700)
    return fig


def display_conversations_pies(writers, names, times, nonames=False):
    colors = ["mediumturquoise", "darkorange"]
    immediate_responses = [i for i in get_immediate_responses_count(
        writers, names, times, 5).values()]
    long_responses = [i for i in get_immediate_responses_count(
        writers, names, times, 2 * 60).values()]
    conv_starters = [i for i in get_conversations_starters(
        writers, names, times, 36 * 60).values()]

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]

    fig = go.FigureWidget(make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {
                          'type': 'domain'}]], subplot_titles=['Do 5 minut', 'Do 2 hodin', "Starty konverzací"]))
    trace0 = go.Pie(labels=writers, values=immediate_responses,
                    name="méně než 5 minut")
    trace1 = go.Pie(labels=writers, values=long_responses,
                    name='méně jak 2 hodiny')
    trace2 = go.Pie(labels=writers, values=conv_starters,
                    name='více jak 24 hodin')

    fig.add_trace(trace0, 1, 1)
    fig.add_trace(trace1, 1, 2)
    fig.add_trace(trace2, 1, 3)

    fig.update_traces(hoverinfo="label+percent", textinfo="value",
                      textfont_size=15, marker=dict(line=dict(color="black", width=2)))
    fig.update_layout(title_text="Rychlosti odpovědí", width=1200)
    return fig


def display_messages_length_whisker_plots(messages, writers, names, nonames=False):
    writers_messages = get_writers_messages(messages, names)
    m_words = [[len(m.split()) for m in writers_messages[writer]]
               for writer in writers]

    fig = go.FigureWidget()

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]
    for i, writer in enumerate(writers):
        fig.add_trace(go.Violin(y=m_words[i],
                                name=writer,
                                box_visible=True,
                                meanline_visible=True,
                                points="all"))

    fig.update_layout(title="Rozložení počtu slov jednotlivých pisatelů",
                      yaxis_title="Poet slov", width=1200, height=600)

    return fig


def display_answer_time_histogram(writers, names, times, nonames=False):
    hist_data = [get_writers_timedeltas(i, writers, names, times)
                 for i in range(len(writers))]

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]
    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Histogram(histfunc="count", x=hist_data[i], name=writers[i], xbins=dict(
            start=0.0,
            end=30.0,
            size=1)))

    fig.update_layout(barmode="overlay", title="Jak rychle odpovídám? (0 až 30 min)",
                      xaxis_title='Doba odpovědi (min)', yaxis_title='Počet odpovědí', width=1200)
    fig.update_traces(opacity=0.5)

    return fig


def display_messages_in_weekdays_histogram(writers, names, times, nonames=False):
    day_name = ['Pondělí', 'Úterý', 'Středa',
                'Čtvrtek', 'Pátek', 'Sobota', 'Neděle']
    writers_weekdays = get_weekdays(names, times)
    hist_data = [writers_weekdays[writers[i]] for i in range(len(writers))]

    for i in range(len(writers)):
        days = hist_data[i]
        new_days = []
        weekdays_counter = [0] * len(day_name)
        for d in days:
            for k, weekday in enumerate(day_name):
                if d == weekday:
                    weekdays_counter[k] += 1

        for j, counter in enumerate(weekdays_counter):
            new_days = new_days + [day_name[j] for _ in range(counter)]
        hist_data[i] = new_days

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]

    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Histogram(histfunc="count",
                                   x=hist_data[i], name=writers[i]))

    fig.update_layout(barmode="stack", title="Agregovaný počet zpráv ve dnech",
                      xaxis_title='Den v týdnu', yaxis_title='Počet zpráv', width=1000)

    return fig


def display_half_hours_histogram(writers, names, times, nonames=False):
    hours = [str_to_time(t).hour + (str_to_time(t).minute / 60) for t in times]
    writers_hours = [[] for _ in writers]

    for i, h in enumerate(hours):
        writer = names[i]
        for j, ww in enumerate(writers):
            if ww == writer:
                writers_hours[j].append(h)

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]

    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Histogram(x=writers_hours[i], xbins=dict(
            start=0, end=24, size=1), name=writers[i]))

    fig.update_layout(barmode="stack", title_text="Agregovaný počet zpráv v půlhodinových intervalech",
                      xaxis_title="Hodiny", yaxis_title="Počet zpráv", width=1000)

    return fig


def display_messages_in_time_scatter(writers, names, times, messages, nonames=False):
    dates = sorted(list(set([str_to_time(t).date() for t in times])))
    day_messages = {}
    len_day_messages = {}
    for writer in writers:
        day_messages[writer] = get_writer_messages_in_a_day(
            dates, writer, names, times, messages)
        len_day_messages[writer] = [len(ms) for ms in day_messages[writer]]

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]
        new_len_day = {}
        for i, w in enumerate(list(len_day_messages.keys())):
            new_len_day[writers[i]] = len_day_messages[w]
        len_day_messages = new_len_day

    dates = ["{}-{}-{}".format(o.year, o.month, o.day) for o in dates]

    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Scatter(
            x=dates, y=len_day_messages[writers[i]], name=writers[i]))

    fig.update_traces(mode="markers+lines",
                      marker_size=10, marker_line_width=2)
    fig.update_layout(title="Počet zpráv v čase",
                      yaxis_zeroline=False, xaxis_zeroline=False, width=1200)

    return fig


def display_emoji_histogram(writers, names, messages, nonames=False):
    used_emojis = get_used_emojis(writers, names, messages)

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]
        new_used_emoji = {}
        for i, w in enumerate(list(used_emojis.keys())):
            new_used_emoji[writers[i]] = used_emojis[w]
        used_emojis = new_used_emoji

    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Histogram(histfunc="sum", y=list(used_emojis[writers[i]].values(
        )), x=list(used_emojis[writers[i]].keys()), name=writers[i]))

    fig.update_layout(title="Jaké emoji používám?",
                      xaxis_title='Emoji', yaxis_title='Počet', width=1200)
    return fig


def display_emoji_reactions(writers, names, messages, nonames=False):
    emoji_reactions = get_emoji_reaction_count(writers, names, messages)

    if nonames:
        writers = ["Author_" + f"{i}" for i in range(len(writers))]
        new_emoji_react = {}
        for i, w in enumerate(list(emoji_reactions.keys())):
            new_emoji_react[writers[i]] = emoji_reactions[w]
        emoji_reactions = new_emoji_react

    fig = go.FigureWidget()
    for i in range(len(writers)):
        fig.add_trace(go.Histogram(histfunc="sum", y=list(emoji_reactions[writers[i]].values(
        )), x=list(emoji_reactions[writers[i]].keys()), name=writers[i]))

    fig.update_layout(title="Jaké reakce jsem dostal?",
                      xaxis_title='Emoji', yaxis_title='Počet', width=1000)
    return fig
