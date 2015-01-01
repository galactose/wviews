from mock import patch, MagicMock
from unittest import TestCase

import parser
from atom import Atom, EpistemicModality
from rule import Rule


class AtomTest(TestCase):
    def test_atom(self):
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', atom_negation=True,
                         modality=EpistemicModality.KNOW, epistemic_negation=True, negation_as_failure=False)
        self.assertEqual(str(test_atom), '-K-a')


class RuleTest(TestCase):
    def test_parse_rule_string(self):
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('a v c :- d, e')),
                      ('a v c :- d, e.', 'a v c :- e, d.'))
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('a :- b, c')), ('a :- b, c.', 'a :- c, b.'))
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('d v e')), ('d v e.', 'e v d.'))
        self.assertEqual(str(Rule(head=None, tail=None).parse_rule_string('f')), 'f.')
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string(':- g, h')), (':- g, h.', ':- h, g.'))
        self.assertEqual(str(Rule(head=None, tail=None).parse_rule_string('a :- not s')), 'a :- not s.')


class ParserTest(TestCase):
    def test_get_sanitised_program_lines_no_file(self):
        line_generator = parser.get_sanitised_lines('')
        with self.assertRaises(StopIteration):
            line_generator.next()

    @patch('__builtin__.file', autospec=True)
    def test_get_sanitised_program_lines_file(self, file_mock):
        file_mock.return_value = ['a :- b, c. %test comment', 'd :- e.', 'e. %another comment', ':- g, h, i.']
        line_generator = parser.get_program_lines('fake_file.elp')
        self.assertEqual(line_generator.next(), 'a :- b, c')
        self.assertEqual(line_generator.next(), 'd :- e')
        self.assertEqual(line_generator.next(), 'e')
        self.assertEqual(line_generator.next(), ':- g, h, i')
        with self.assertRaises(StopIteration):
            line_generator.next()
        file_mock.assert_called_once_with('fake_file.elp', 'r')
