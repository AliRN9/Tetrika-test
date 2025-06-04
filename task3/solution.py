def merge_intervals(times: list, lesson_start, lesson_end):
    """
    разбиваем список на пары (вход-выход)
    обрезаем каждый интервал, чтобы он не выходил за пределы времени урока,


    :param times: list
    :param lesson_start: int
    :param lesson_end: int
    :return:
    """
    result = []
    for start, end in zip(times[::2], times[1::2]):
        new_start = max(start, lesson_start)
        new_end = min(end, lesson_end)
        if new_start < new_end:
            result.append((new_start, new_end))

    return merge_overlapping(result)


def merge_overlapping(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def intersect_intervals(pupil: list[tuple[int, int]], tutor: list[tuple[int, int]]) -> int:
    i = j = 0
    all_time = 0

    while i < len(pupil) and j < len(tutor):
        p_start, p_end = pupil[i]
        t_start, t_end = tutor[j]

        start = max(p_start, t_start)
        end = min(p_end, t_end)

        if start < end:
            all_time += (end - start)

        if p_end < t_end:
            i += 1
        else:
            j += 1
    return all_time


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    if not lesson:
        return 0
    lesson_start, lesson_end = lesson

    pupil_times = merge_intervals(intervals['pupil'], lesson_start, lesson_end)
    if not pupil_times:
        return 0

    tutor_times = merge_intervals(intervals['tutor'], lesson_start, lesson_end)
    if not tutor_times:
        return 0

    return intersect_intervals(pupil_times, tutor_times)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print('All tests passed.')
