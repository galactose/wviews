from unittest import TestCase
from mock import patch, MagicMock

import wviews.program.parser as parser
from wviews.program.atom import Atom, EpistemicModality, NegationAsFailureAtom, EpistemicAtom
from wviews.program.rule import Rule
from wviews.program.program import LogicProgram


class AtomTest(TestCase):
    def setUp(self):
        self.test_atom = EpistemicAtom(
            label='a', atom_negation=True,
            modality=EpistemicModality.KNOW, epistemic_negation=True
        )

    def test_base_atom(self):
        self.assertEqual(str(self.test_atom), '-K-a')

    def test_equal(self):
        self.assertEqual(self.test_atom,
                         EpistemicAtom(atom_id=None, label_id=None, label='a', atom_negation=True,
                                       modality=EpistemicModality.KNOW, epistemic_negation=True))
        self.assertEqual(self.test_atom.__hash__(), hash('-K-a'))
        self.assertRaises(ValueError, EpistemicAtom, atom_id=None, label_id=None, label='a', atom_negation=True,
                          modality=None, epistemic_negation=True)


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
        #bla = self.program.get_atom_information('-K-a')
        #print bla.__dict__
        self.assertEqual(self.program.get_atom_information('-K-a').__dict__,
                         {'atom_id': 1, 'label_id': 1, 'atom_negation': True, 'epistemic_negation': True,
                          'label': 'a', 'modality': 1, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-Ka').__dict__,
                         {'atom_id': 2, 'label_id': 1, 'atom_negation': False, 'epistemic_negation': True,
                          'label': 'a', 'modality': 1, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('K-a').__dict__,
                         {'atom_id': 3, 'label_id': 1, 'atom_negation': True, 'epistemic_negation': False,
                          'label': 'a', 'modality': 1, 'valuation': None})

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

        self.assertEqual(self.program.get_atom_information('M-b').__dict__,
                         {'atom_id': 6, 'label_id': 2, 'atom_negation': True, 'epistemic_negation': False,
                          'label': 'b', 'modality': 2, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-M-b').__dict__,
                         {'atom_id': 7, 'label_id': 2, 'atom_negation': True, 'epistemic_negation': True,
                          'label': 'b', 'modality': 2, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-Mb').__dict__,
                         {'atom_id': 8, 'label_id': 2, 'atom_negation': False, 'epistemic_negation': True,
                          'label': 'b', 'modality': 2, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('c').__dict__,
                         {'atom_id': 9, 'label_id': 3, 'atom_negation': False, 'label': 'c'})

        self.assertEqual(self.program.get_atom_information('-e').__dict__,
                         {'atom_id': 10, 'label_id': 4, 'atom_negation': True, 'label': 'e'})

        test_atom = self.program.get_atom_information('not d')
        self.assertIsInstance(test_atom, NegationAsFailureAtom)
        self.assertEqual(test_atom.__dict__, {'atom_id': 11, 'label_id': 5, 'label': 'd', 'atom_negation': False})

        test_atom = self.program.get_atom_information('not full_atom')
        self.assertIsInstance(test_atom, NegationAsFailureAtom)
        self.assertEqual(test_atom.__dict__,
                         {'atom_id': 12, 'label_id': 6, 'atom_negation': False, 'label': 'full_atom'})

        self.assertRaises(ValueError, self.program.get_atom_information, 'not -d')
        self.assertRaises(ValueError, self.program.get_atom_information, 'not ~d')
