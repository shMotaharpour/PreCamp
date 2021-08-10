import csv


def double_add(base, til, line):
    global shadow
    valve = line[til]
    if valve == '':
        return
    if 'آ' in valve:
        valve = valve.replace('آ', 'ا')
    parts = valve.split()
    if len(parts) > 1:
        valve_shadow = ''.join(parts)
        shadow[til][valve_shadow] = valve
        base[til].add(valve)
    else:
        base[til].add(valve)


def remove_doubled_name():
    global shadow, allowed_names
    for key in shadow:
        for word in shadow[key]:
            if word in allowed_names[key]:
                allowed_names[key] -= {word}


def ready_up():
    global match_player, scores, all_answer_data, match_data, allowed_names, shadow
    shadow = {}
    match_player = {}
    scores = {}
    all_answer_data = set()
    match_data = {}
    allowed_names = {}
    n_try = 10
    while n_try:
        try:
            with open('esm_famil_data.csv', encoding='utf8', newline='') as f:
                first_line = csv.reader(f)
                for row in first_line:
                    for til in row:
                        allowed_names[til] = set()
                        all_answer_data.add(til)
                        match_data[til] = {}
                        shadow[til] = {}
                    break
            with open('esm_famil_data.csv', encoding='utf8', newline='') as f:
                for row in csv.DictReader(f):
                    for title in match_data:
                        double_add(allowed_names, title, row)
            remove_doubled_name()
            break
        except IOError:
            print('Can not read the file')
            n_try -= 1
    else:
        print('aa')


def add_participant(participant: str = '', answers: dict = {}):
    global match_player, scores, all_answer_data, match_data, allowed_names, shadow
    try:
        scores[participant] = 0
        match_player[participant] = answers

        for key in match_data:
            if key not in answers:
                answers[key] = ' '
        for key, valve in answers.items():
            if 'آ' in valve:
                valve = valve.replace('آ', 'ا')
            parts = valve.split()
            if len(parts) == 0:
                all_answer_data -= {key}
            elif valve in allowed_names[key]:
                pass
            elif valve in shadow[key]:
                valve = shadow[key][valve]
            else:
                valve_shadow = ' '.join(parts)
                if valve_shadow in allowed_names[key]:
                    valve = valve_shadow
                # اینجا برای فاصله های بی مورد هرجایی استفاده میشه
                valve_shadow = ''.join(parts)
                if valve in shadow[key]:
                    valve = shadow[key][valve]
                elif valve_shadow in shadow[key]:
                    valve = shadow[key][valve_shadow]

            if valve in allowed_names[key]:
                if valve in match_data[key]:
                    match_data[key][valve].append(participant)
                else:
                    match_data[key][valve] = [participant]
            # else:  # فرض منطقی برابر بودن غلط نوشتن با هیچی ننوشتن
            #     all_answer_data -= {key}
    except NameError:
        print('First run ready_up')
    except:
        raise


def calculate_all():
    global match_player, scores, MATCH_DATA, ALL_ANS_DATA, all_answer_data, match_data, allowed_names
    for key in match_data:
        if key in all_answer_data:
            for ans, plys in match_data[key].items():
                if len(plys) == 1:
                    scores[plys[0]] += 10
                else:
                    for name in plys:
                        scores[name] += 5
        else:
            for ans, plys in match_data[key].items():
                if len(plys) == 1:
                    scores[plys[0]] += 15
                else:
                    for name in plys:
                        scores[name] += 10
    return scores


if __name__ == '__main__':
    ready_up()
    add_participant(participant='salib',
                    answers={'ghaza': 'جوجه '})
    add_participant(participant='salib2',
                    answers={'ghaza': 'جوجه کباب'})
    print(calculate_all())
