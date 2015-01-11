from mock import patch, MagicMock
from unittest import TestCase

import parser
from atom import Atom, EpistemicModality
from rule import Rule


class AtomTest(TestCase):

    def setUp(self):
        self.test_atom = Atom(atom_id=None, label='a', atom_negation=True, modality=EpistemicModality.KNOW,
                              epistemic_negation=True, negation_as_failure=False)

    def test_atom(self):
        self.assertEqual(str(self.test_atom), '-K-a')

    def test_equal(self):
        self.assertEqual(self.test_atom,
                         Atom(atom_id=None, label='a', atom_negation=True, modality=EpistemicModality.KNOW,
                              epistemic_negation=True, negation_as_failure=False))
        self.assertEqual(self.test_atom.__hash__(), hash('-K-a'))
        self.assertRaises(ValueError, Atom, atom_id=None, label='a', atom_negation=True, modality=None,
                          epistemic_negation=True, negation_as_failure=False)


class RuleTest(TestCase):
    def test_parse_rule_string(self):
        self.assertIn(str(Rule('a v c :- d, e')), ('a v c :- d, e.', 'a v c :- e, d.'))
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
        file_mock.return_value = ['a :- b, c. %test comment', 'd :- e.', 'e. %another comment', ':- g, h, i.']
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
        sys_mock.stdout.write.assert_called_once_with('\n<file does not exist.>\n')

    @patch('wviews.program.parser.get_sanitised_lines', autospec=True)
    def test_get_sanitised_lines(self, get_sanitised_lines_mock):
        get_sanitised_lines_mock.return_value = ['a\n', 'b\n', 'c\n']
        answer_set_importer = parser.import_answer_set(file_name='test_file_name')
        self.assertEqual(answer_set_importer.next(), 'a')
        self.assertEqual(answer_set_importer.next(), 'b')
        self.assertEqual(answer_set_importer.next(), 'c')
        self.assertRaises(StopIteration, answer_set_importer.next)
        get_sanitised_lines_mock.assert_called_once_with('test_file_name')
