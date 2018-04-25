
from itertools import product
from rule import Rule


class Token(object):
    def __init__(self, raw_label):
        self.raw_label = raw_label
        self.label = None
        self.variables = list()
        self.ground_values = list()
        self.args = self.parse_args(raw_label)

    def parse_args(self, raw_label):
        token = raw_label.replace(' ','')
        if '(' not in raw_label and ')' not in raw_label:
            self.label = raw_label
            return []
        elif '(' in raw_label and ')' not in raw_label or \
          '(' not in raw_label and ')' in raw_label:
          raise ValueError('Bad token syntax: %s' % raw_label)
        first_paren = token.index('(')
        self.label = token[:first_paren]
        raw_args = token[first_paren + 1:token.index(')')]
        args = raw_args.split(',')
        for arg in args:
            if arg.isupper() and arg not in self.variables:
                self.variables.append(arg)
            elif arg not in self.ground_values:
                self.ground_values.append(arg)
        self.variables.sort()
        self.ground_values.sort()
        return args

    def __str__(self):
        args = '(%s)' % ','.join(self.args) if self.args else ''
        return '%s%s' % (self.label, args)


class Grounder(object):
    def __init__(self, parsed_program):
        self.parsed_program = parsed_program
        self.variables = list()
        self.ground_values = list()
        self.get_variables_and_domain()

    def get_variables_and_domain(self):
        for rule in self.parsed_program:
            for raw_token in rule.head:
                token = Token(raw_label=raw_token)
                self.variables.extend(token.variables)
                self.variables =  list(set(self.variables))
                self.ground_values.extend(token.ground_values)
                self.ground_values = list(set(self.ground_values))
            for raw_token in rule.tail:
                token = Token(raw_label=raw_token)
                self.variables.extend(token.variables)
                self.variables =  list(set(self.variables))
                self.ground_values.extend(token.ground_values)
                self.ground_values = list(set(self.ground_values))
        self.ground_values.sort()
        self.variables.sort()

    def ground_program(self, parsed_program):
        for rule in parsed_program:
            for grounded_rule in self.ground_rule(rule):
                yield grounded_rule

    def ground_rule(self, rule):
        rule_variables = self.get_rule_variables(rule)
        val_product = product(self.ground_values, repeat=len(rule_variables))

        for vals in val_product:
            head = [str(token) for token in self.ground_tokens(rule.head, vals, rule_variables)]
            tail = [str(token) for token in self.ground_tokens(rule.tail, vals, rule_variables)]

            rule_string = ''
            if head and tail:
                rule_string = '%s :- %s' % (' v '.join(head), ', '.join(tail))
            elif tail:
                rule_string = ':- %s' % ', '.join(tail)
            else:
                rule_string = '%s' % (' v '.join(head))

            yield Rule(rule_string)

    def get_rule_variables(self, rule):
        rule_variables = []
        for raw_token in rule.head:
            rule_variables.extend(Token(raw_token).variables)
        for raw_token in rule.tail:
            rule_variables.extend(Token(raw_token).variables)
        rule_variables = list(set(rule_variables))
        rule_variables.sort()
        return rule_variables

    def ground_tokens(self, tokens, valuation, rule_variables):
        for token in tokens:
            yield self.ground_token(token, valuation, rule_variables)

    def ground_token(self, raw_token, valuation, rule_variables):
        token = Token(raw_token)
        grounded_token = Token(raw_token)
        grounded_token.args = []
        for argument in token.args:
            if not argument.isupper():
                grounded_token.args.append(argument)
                continue
            try:
                var_index = rule_variables.index(argument)
            except ValueError:
                print 'Parsing error with argument %s.' % argument
                exit(1)
            grounded_token.args.append(valuation[var_index])
        return grounded_token
