import datetime


def str_to_time(s_time):
    return datetime.datetime.strptime(s_time, '%d. %m. %Y %H:%M')


def get_writer_messages_in_a_day(dates, writer, names, times, messages):
    dates_messages = [[] for _ in dates]
    for index, time in enumerate(times):
        if names[index] != writer:
            continue
        date = str_to_time(time).date()
        message = messages[index]
        for i, d in enumerate(dates):
            if d == date:
                dates_messages[i] = dates_messages[i] + [message]
    return dates_messages


def get_timedeltas(names, times):
    time_series = {}
    last_writer, last_time = None, None

    for i in range(len(names)):
        respondent = names[i]
        m_time = str_to_time(times[i])

        if not last_writer:
            last_writer = respondent
            last_time = m_time
            time_series[respondent] = time_series.get(respondent, []) + [0]
        else:
            time_delta = (m_time - last_time).total_seconds() / 60.0
            if respondent != last_writer:
                time_series[respondent] = time_series.get(
                    respondent, []) + [time_delta]
                last_writer = respondent
                last_time = m_time
            else:  # Not from the very last message
                time_series[respondent] = time_series.get(
                    respondent, []) + [-1]
                last_time = m_time
    return time_series


def get_avg_time_to_answear(writers, names, times):
    time_series = get_timedeltas(names, times)

    print("---Min time to answear---")
    min_times = {}
    for writer in writers:
        min_time = round(min(time_series[writer]) / 60, 1)
        min_times[writer] = min_time
        print(f"{writer}: {min_time} minutes")

    print("\n---Max time to answear---")
    max_times = {}
    for writer in writers:
        max_time = round(max(time_series[writer]) / 60, 1)
        max_times[writer] = max_time
        print(f"{writer}: {max_time} minutes")

    print("\n---Average time to answear---")
    avg_times = {}
    for writer in writers:
        avg_time = round(
            sum(time_series[writer]) / (len(time_series[writer]) * 60), 1)
        avg_times[writer] = avg_time
        print(f"{writer}: {avg_time} minutes")

    return avg_times


def get_immediate_responses_count(writers, names, times, immediate=5):
    time_series = get_timedeltas(names, times)

    zero_times = {}
    for writer in writers:
        zero_count = len([t for t in time_series[writer]
                          if (t < immediate and t >= 0)])
        zero_times[writer] = zero_count

    return zero_times


def get_long_responses_count(writers, names, times, immediate=60):
    time_series = get_timedeltas(names, times)

    zero_times = {}
    for writer in writers:
        zero_count = len(
            [t for t in time_series[writer] if (abs(t) > immediate)])
        zero_times[writer] = zero_count

    return zero_times


def get_longest_message_streak(names, messages):
    last_name = None
    longest_streak = {}
    longest_streak_messages = {}
    message_streak = []
    current_streak = 1
    for index, name in enumerate(names):
        if not last_name:
            last_name = name
        else:
            if last_name == name:
                current_streak += 1
                message_streak.append(messages[index])
            else:
                if longest_streak.get(last_name, 1) < current_streak:
                    longest_streak[last_name] = current_streak
                    longest_streak_messages[last_name] = message_streak

                current_streak = 1
                message_streak = []
            last_name = name

    return longest_streak_messages


def get_conversations_starters(writers, names, times, threshold=24 * 60):
    conv_started = {}
    for writer in writers:
        conv_started[writer] = 0
    last_time = None

    for i in range(len(names)):
        respondent = names[i]
        m_time = str_to_time(times[i])

        if i == 0:
            conv_started[respondent] = conv_started.get(respondent, 0) + 1
        else:
            time_delta = (m_time - last_time).total_seconds() / 60.0
            if time_delta > threshold:
                conv_started[respondent] = conv_started.get(respondent, 0) + 1

        last_time = m_time

    return conv_started


def get_writers_timedeltas(i, writers, names, times):
    timedeltas = get_timedeltas(names, times)
    return [t for t in timedeltas[writers[i]] if t != -1]


def get_weekdays(names, times):
    writers_weekdays = {}
    day_name = ['Pondělí', 'Úterý', 'Středa',
                'Čtvrtek', 'Pátek', 'Sobota', 'Neděle']
    for i in range(len(names)):
        t = times[i]
        writer = names[i]
        writers_weekdays[writer] = writers_weekdays.get(
            writer, []) + [day_name[str_to_time(t).weekday()]]

    return writers_weekdays
