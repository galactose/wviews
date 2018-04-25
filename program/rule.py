
class BrokenConstraint(Exception):
    pass


class Rule(object):
    def __init__(self, rule_string):
        """
        An object loosely representing a rule in a logic program,

        Arguments:
         * rule_string (str) - a rule that follows the syntax of an epistemic
                               logic program rule.
        """
        self.head = set()
        self.tail = set()
        self.parse_rule_string(rule_string)

    def parse_rule_string(self, rule_string):
        """
        Given a string following the syntax of an epistemic logic program break
        it down into sections usable in evaluating it's valid worldviews.

        Arguments:
         * rule_string (str) - a rule that follows the syntax of an epistemic
                               logic program rule.
        """
        body = rule_string.split(':-')
        if len(body) == 1:  # atom or disjunctive atom
            self.head = {token.strip() for token in body[0].split(' v ')}
        elif len(body) == 2:  # rule or constraint
            for token in body[0].split(' v '):
                self.head.add(token.replace(' ', ''))
            if len(self.head) == 1 and '' in self.head:
                self.head = set()

            if '(' in body[1] and ')' in body[1]:
                while '(' in body[1] and ')' in body[1]:
                    first = body[1].index('(')
                    last = body[1].index(')')
                    token = body[1][:last + 1].strip()
                    if not token.startswith('not '):
                        token = token.replace(' ', '')
                    self.tail.add(token)
                    body[1] = body[1][last + 1:].strip()
                    if body[1].startswith(','):
                        body[1] = body[1][1:].strip()
            else:
                for token in body[1].split(','):
                    token = token.strip()
                    if not token.startswith('not '):
                        token = token.replace(' ', '')
                    self.tail.add(token)

        return [self.head, self.tail]

    def __str__(self):
        if self.head and self.tail:
            return '%s :- %s.' % (' v '.join(self.head), ', '.join(self.tail))
        if self.tail:
            return ':- %s.' % ', '.join(self.tail)
        return '%s.' % (' v '.join(self.head))


class IndexedRule(object):
    def __init__(self, head, tail, atom_dict=None):
        self.head = head
        self.tail = tail
        self.atom_dict = atom_dict

    def get_rule_head_string(self):
        return ' v '.join([str(self.atom_dict[atom]) for atom in self.head])

    def get_rule_tail_string(self, apply_valuation=False):
        """
        For the rule, run through the indexed atoms and return the
        representative string to be sent to dlv.
        If apply_valuation is true apply the semantics of an evaluated rule.

        Arguments:
         * apply_valuation (bool) - apply epistemic atom semantics to the rule
                                    based on the valuations.
        """
        if apply_valuation:
            rule_tail = []
            for atom_id in self.tail:
                atom = self.atom_dict[atom_id]
                evaluated_atom = atom.valuation_string(apply_valuation)
                if evaluated_atom:
                    rule_tail.append(evaluated_atom)
            return ', '.join(rule_tail)
        return ', '.join([str(self.atom_dict[atom]) for atom in self.tail])

    def get_rule_string(self, apply_valuation=False):
        if self.head and self.tail:
            tail = self.get_rule_tail_string(apply_valuation)
            if not tail:
                return '%s.' % self.get_rule_head_string()
            return '%s :- %s.' % (self.get_rule_head_string(), tail)
        elif self.tail:
            tail = self.get_rule_tail_string(apply_valuation)
            if not tail:
                raise BrokenConstraint
            return ':- %s.' % self.get_rule_tail_string(apply_valuation)
        return '%s.' % self.get_rule_head_string()

    def __str__(self):
        return self.get_rule_string()
