import re


def parse_answer_sets(raw_answer_sets):
    """
        parse_answer_set: takes unformatted queue of answerset values and removes formatting, making a list of lists

        Arguments:
         * answer_sets (list(str)) - a list of unformatted strings
    """
    answer_set_regex = re.compile(r'{([\W\w]*)}')
    answer_set = []
    answer_sets = []
    for line in raw_answer_sets:
        regex_object = answer_set_regex.search(line)
        if regex_object:
            answer_set = [answer_set_token.strip() for answer_set_token in regex_object.group(1).split(',')]
        answer_sets.append(answer_set)
    return answer_sets
