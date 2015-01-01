

class Rule(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def parse_rule_string(self, rule_string):
        body = rule_string.split(':-')
        if len(body) == 1:  # atom or disjunctive atom
            self.head = {token.strip() for token in body[0].strip().split(' v ')}
        elif len(body) == 2:  # rule or constraint
            self.head = {token.strip().replace(' ', '') for token in body[0].split(' v ')}
            if len(self.head) == 1 and '' in self.head:
                self.head = None
            self.tail = set()
            for token in body[1].split(','):
                if token.strip().startswith('not '):
                    token = token.replace(' ', '')
                self.tail.add(token.strip())
        return self

    def get_rule_head_string(self):
        return ' v '.join([str(atom) for atom in self.head])

    def get_rule_tail_string(self):
        return ', '.join([str(atom) for atom in self.tail])

    def __str__(self):
        if self.tail and self.head:
            return '%s :- %s.' % (self.get_rule_head_string(), self.get_rule_tail_string())
        elif self.tail:
            return ':- %s.' % self.get_rule_tail_string()
        return '%s.' % self.get_rule_head_string()
