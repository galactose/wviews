from unittest import TestCase
from mock import patch, MagicMock

import wviews.program.parser as parser
from wviews.program.atom import Atom, EpistemicModality, \
    NegationAsFailureAtom, EpistemicAtom
from wviews.program.rule import Rule
from wviews.program.program import LogicProgram
from grounder import Token, Grounder
from wviews.program.parser import parse_program



class AtomTest(TestCase):
    def setUp(self):
        self.test_atom = EpistemicAtom(
            label='a', atom_negation=True,
            modality=EpistemicModality.KNOW, epistemic_negation=True
        )

    def test_base_atom(self):
        self.assertEqual(str(self.test_atom), '-K-a')

    def test_equal(self):
        self.assertEqual(
            self.test_atom,
            EpistemicAtom(atom_id=None, label_id=None, label='a',
                          atom_negation=True, modality=EpistemicModality.KNOW,
                          epistemic_negation=True))
        self.assertEqual(self.test_atom.__hash__(), hash('-K-a'))
        self.assertRaises(
            ValueError, EpistemicAtom, atom_id=None, label_id=None, label='a',
            atom_negation=True, modality=None, epistemic_negation=True
        )


class RuleTest(TestCase):
    def test_parse_rule_string(self):
        self.assertIn(str(Rule('a v c :- d, e')),
                      ('a v c :- d, e.', 'a v c :- e, d.'))
        self.assertIn(str(Rule('a :- b, c')), ('a :- b, c.', 'a :- c, b.'))
        self.assertIn(str(Rule('d v e')), ('d v e.', 'e v d.'))
        self.assertEqual(str(Rule('f')), 'f.')
        self.assertIn(str(Rule(':- g, h')), (':- g, h.', ':- h, g.'))
        self.assertEqual(str(Rule('a :- not s')), 'a :- not s.')


class ParserTest(TestCase):
    def test_get_sanitised_program_lines_no_file(self):
        line_generator = parser.get_sanitised_lines('')
        with self.assertRaises(StopIteration):
            line_generator.next()

    @patch('__builtin__.file', autospec=True)
    def test_get_sanitised_program_lines_file(self, file_mock):
        file_mock.return_value = [
            'a :- b, c. %test comment', 'd :- e.', 'e. %another comment',
            ':- g, h, i.'
        ]
        line_generator = parser.get_program_lines('fake_file.elp')
        self.assertEqual(line_generator.next(), 'a :- b, c')
        self.assertEqual(line_generator.next(), 'd :- e')
        self.assertEqual(line_generator.next(), 'e')
        self.assertEqual(line_generator.next(), ':- g, h, i')
        with self.assertRaises(StopIteration):
            line_generator.next()
        file_mock.assert_called_once_with('fake_file.elp', 'r')

    @patch('wviews.program.parser.sys', autospec=True)
    @patch('__builtin__.file', autospec=True)
    def test_get_sanitised_program_lines_file_error(self, file_mock, sys_mock):
        file_mock.side_effect = IOError
        line_generator = parser.get_program_lines('fake_file.elp')
        self.assertRaises(StopIteration, line_generator.next)
        sys_mock.stdout.write.assert_called_once_with(
            '\n<file does not exist.>\n'
        )

    @patch('wviews.program.parser.get_sanitised_lines', autospec=True)
    def test_get_sanitised_lines(self, get_sanitised_lines_mock):
        get_sanitised_lines_mock.return_value = ['a\n', 'b\n', 'c\n']
        answer_set = parser.import_answer_set(file_name='test_file_name')
        self.assertEqual(answer_set.next(), 'a')
        self.assertEqual(answer_set.next(), 'b')
        self.assertEqual(answer_set.next(), 'c')
        self.assertRaises(StopIteration, answer_set.next)
        get_sanitised_lines_mock.assert_called_once_with('test_file_name')


class ProgramTest(TestCase):
    def setUp(self):
        self.program = LogicProgram(MagicMock())

    def test_get_or_create_atom(self):
        test_atom = Atom(label='a', atom_negation=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(label='a', atom_negation=True)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(label='a', atom_negation=True)
        self.assertEqual(self.program.get_or_create_atom(test_atom), False)

    def test_get_atom_information(self):
        self.assertEqual(
            self.program.get_atom_information('-K-a').__dict__,
            {'atom_id': 1, 'label_id': 1, 'atom_negation': True,
             'epistemic_negation': True, 'label': 'a', 'modality': 1,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('-Ka').__dict__,
            {'atom_id': 2, 'label_id': 1, 'atom_negation': False,
             'epistemic_negation': True, 'label': 'a', 'modality': 1,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('K-a').__dict__,
            {'atom_id': 3, 'label_id': 1, 'atom_negation': True,
             'epistemic_negation': False, 'label': 'a', 'modality': 1,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('Ka').__dict__,
            {
                'atom_id': 4, 'label_id': 1, 'atom_negation': False,
                'epistemic_negation': False, 'label': 'a', 'modality': 1,
                'valuation': None
            }
        )

        self.assertEqual(
            self.program.get_atom_information('Ma').__dict__,
            {
                'atom_id': 5, 'label_id': 1, 'atom_negation': False,
                'epistemic_negation': False, 'label': 'a', 'modality': 2,
                'valuation': None
            }
        )

        self.assertEqual(
            self.program.get_atom_information('M-b').__dict__,
            {'atom_id': 6, 'label_id': 2, 'atom_negation': True,
             'epistemic_negation': False, 'label': 'b', 'modality': 2,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('-M-b').__dict__,
            {'atom_id': 7, 'label_id': 2, 'atom_negation': True,
             'epistemic_negation': True, 'label': 'b', 'modality': 2,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('-Mb').__dict__,
            {'atom_id': 8, 'label_id': 2, 'atom_negation': False,
             'epistemic_negation': True, 'label': 'b', 'modality': 2,
             'valuation': None}
        )

        self.assertEqual(
            self.program.get_atom_information('c').__dict__,
            {'atom_id': 9, 'label_id': 3, 'atom_negation': False,
             'label': 'c'}
        )

        self.assertEqual(
            self.program.get_atom_information('-e').__dict__,
            {'atom_id': 10, 'label_id': 4, 'atom_negation': True, 'label': 'e'}
        )

        test_atom = self.program.get_atom_information('not d')
        self.assertIsInstance(test_atom, NegationAsFailureAtom)
        self.assertEqual(
            test_atom.__dict__,
            {'atom_id': 11, 'label_id': 5, 'label': 'd',
             'atom_negation': False}
        )

        test_atom = self.program.get_atom_information('not full_atom')
        self.assertIsInstance(test_atom, NegationAsFailureAtom)
        self.assertEqual(
            test_atom.__dict__,
            {'atom_id': 12, 'label_id': 6, 'atom_negation': False,
             'label': 'full_atom'}
        )

        self.assertRaises(
            ValueError, self.program.get_atom_information, 'not -d'
        )
        self.assertRaises(
            ValueError, self.program.get_atom_information, 'not ~d'
        )


class TokenTest(TestCase):

    def setUp(self):
        self.test_token = Token(raw_label='test(X, Y, a, b, c)')

    def test_base_token(self):
        self.assertEqual(str(self.test_token), 'test(X,Y,a,b,c)')
        self.assertListEqual(self.test_token.variables, ['X', 'Y'])
        self.assertListEqual(self.test_token.ground_values, ['a', 'b', 'c'])
        self.assertEqual(str(Token(raw_label='test')), 'test')

        token = Token('test(w, X, y, Z)')
        self.assertEqual(str(token), 'test(w,X,y,Z)')
        self.assertListEqual(token.variables, ['X', 'Z'])
        self.assertListEqual(token.ground_values, ['w', 'y'])

        self.assertRaises(ValueError, Token, 'test(X,')
        self.assertRaises(ValueError, Token, 'testX)')


class GrounderTest(TestCase):
    def setUp(self):
        self.test_program = parse_program('examples/interview.elp')
        self.grounder = Grounder(self.test_program)

    def test_get_variables(self):
        self.assertEqual(self.grounder.variables, ['X'])
        self.assertEqual(self.grounder.ground_values, ['alice'])

        self.grounder = Grounder(parse_program('examples/world.elp'))
        self.assertEqual(self.grounder.variables, ['X', 'Y', 'Z'])
        self.assertEqual(self.grounder.ground_values, ['a', 'b', 'c', 'd'])

    def test_ground_token(self):
        valuation =['foo', 'bar', 'baz']
        variables = ['X', 'Y']
        gdr = self.grounder
        self.assertEqual(
            str(gdr.ground_token('test(foo,X)', ['bar', 'baz'], variables)), 'test(foo,bar)'
        )
        self.assertEqual(
            str(gdr.ground_token('test(X,foo,Y)', ['blah', 'blah'], variables)), 'test(blah,foo,blah)'
        )
        self.assertEqual(
            str(gdr.ground_token('test(Y)', valuation, variables)), 'test(bar)'
        )

        variables = ['X', 'Y', 'Z']
        self.assertEqual(
            str(gdr.ground_token('test(Z,X,Y)', valuation, variables)), 'test(baz,foo,bar)'
        )
        self.assertEqual(
            str(gdr.ground_token('test(X,Y,Z)', valuation, variables)), 'test(foo,bar,baz)'
        )
        self.assertEqual(
            str(gdr.ground_token('test(Y,Z,X)', valuation, variables)), 'test(bar,baz,foo)'
        )
        self.assertEqual(
            str(gdr.ground_token('test(fizz,bang,X)', valuation, variables)), 'test(fizz,bang,foo)'
        )
        self.assertEqual(
            str(gdr.ground_token('test( )', valuation, variables)), 'test()'
        )
        gdr.variables = []
        self.assertEqual(
            str(gdr.ground_token('test(foo)', valuation, variables)), 'test(foo)'
        )

    def test_ground_tokens(self):
        variables = ['X', 'Y', 'Z']
        ground_it = self.grounder.ground_tokens(['test(Z,X,Y)', 'test(X,Y,Z)'], ['foo', 'bar', 'baz'], variables)

        self.assertEqual(
            str(ground_it.next()), 'test(baz,foo,bar)'
        )
        self.assertEqual(
            str(ground_it.next()), 'test(foo,bar,baz)'
        )
        self.assertRaises(
            StopIteration, ground_it.next
        )

    def test_ground_rule(self):
        self.grounder.variables = ['X', 'Y', 'Z']
        self.grounder.ground_values = ['foo', 'bar']
        rule = Rule('a(X) :- b(X)')

        ground_it = self.grounder.ground_rule(rule)
        self.assertEqual(str(ground_it.next()), 'a(foo) :- b(foo).')
        self.assertEqual(str(ground_it.next()), 'a(bar) :- b(bar).')
        self.assertRaises(
            StopIteration, ground_it.next
        )

        self.grounder.variables = ['X', 'Y', 'Z']
        self.grounder.ground_values = ['foo', 'bar']
        rule = Rule('a(X) v b v c(Z) :- b(X), d(Y)')

        ground_it = self.grounder.ground_rule(rule)
        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(foo)', 'b', 'c(foo)'})
        self.assertSetEqual(rule.tail, {'b(foo)', 'd(foo)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(foo)', 'b', 'c(bar)'})
        self.assertSetEqual(rule.tail, {'b(foo)', 'd(foo)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(foo)', 'b', 'c(foo)'})
        self.assertSetEqual(rule.tail, {'b(foo)', 'd(bar)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(foo)', 'b', 'c(bar)'})
        self.assertSetEqual(rule.tail, {'b(foo)', 'd(bar)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(bar)', 'b', 'c(foo)'})
        self.assertSetEqual(rule.tail, {'b(bar)', 'd(foo)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(bar)', 'b', 'c(bar)'})
        self.assertSetEqual(rule.tail, {'b(bar)', 'd(foo)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(bar)', 'b', 'c(foo)'})
        self.assertSetEqual(rule.tail, {'b(bar)', 'd(bar)'})

        rule = ground_it.next()
        self.assertSetEqual(rule.head, {'a(bar)', 'b', 'c(bar)'})
        self.assertSetEqual(rule.tail, {'b(bar)', 'd(bar)'})

        self.assertRaises(StopIteration, ground_it.next)

    def test_ground_program_no_vars(self):
        test_program = parse_program('examples/conflict.elp')
        grounder = Grounder(test_program)
        it = grounder.ground_program(parse_program('examples/conflict.elp'))
        rule = it.next()
        self.assertSetEqual(rule.head, {'a'})
        self.assertSetEqual(rule.tail, {'b', 'c'})
        self.assertEqual(str(it.next()), 'b.')
        self.assertEqual(str(it.next()), 'c.')
        self.assertRaises(StopIteration, it.next)

    def test_ground_program(self):
        test_program = parse_program('examples/world.elp')
        grounder = Grounder(test_program)
        it = grounder.ground_program(parse_program('examples/world.elp'))

        self.assertEqual(str(it.next()), 'P(b) v P(a).')
        self.assertEqual(str(it.next()), 'P(c).')
        self.assertEqual(str(it.next()), 'Q(d).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MP(a,a).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MP(a,b).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MP(a,c).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MP(a,d).')

        self.assertEqual(str(it.next()), '~P(b) :- ~MP(b,a).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MP(b,b).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MP(b,c).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MP(b,d).')

        self.assertEqual(str(it.next()), '~P(c) :- ~MP(c,a).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MP(c,b).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MP(c,c).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MP(c,d).')

        self.assertEqual(str(it.next()), '~P(d) :- ~MP(d,a).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MP(d,b).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MP(d,c).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MP(d,d).')

        self.assertEqual(str(it.next()), '~P(a) :- ~MQ(a).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MQ(b).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MQ(c).')
        self.assertEqual(str(it.next()), '~P(a) :- ~MQ(d).')

        self.assertEqual(str(it.next()), '~P(b) :- ~MQ(a).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MQ(b).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MQ(c).')
        self.assertEqual(str(it.next()), '~P(b) :- ~MQ(d).')

        self.assertEqual(str(it.next()), '~P(c) :- ~MQ(a).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MQ(b).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MQ(c).')
        self.assertEqual(str(it.next()), '~P(c) :- ~MQ(d).')

        self.assertEqual(str(it.next()), '~P(d) :- ~MQ(a).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MQ(b).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MQ(c).')
        self.assertEqual(str(it.next()), '~P(d) :- ~MQ(d).')

        self.assertRaises(StopIteration, it.next)
