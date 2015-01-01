from unittest import TestCase
from mock import MagicMock

from program.atom import Atom, EpistemicModality
from optimisation import LogicProgram
from wviews import WorldViews


class OptimiseTest(TestCase):
    def setUp(self):
        self.program = LogicProgram(MagicMock())

    def test_get_atom_information(self):
        self.get_atom_information_assert(
            '-K-a', True, {'atom_id': 1, 'atom_negation': True, 'epistemic_id': 1, 'epistemic_negation': True,
                           'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            '-Ka', True, {'atom_id': 2, 'atom_negation': False, 'epistemic_id': 2, 'epistemic_negation': True,
                          'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'K-a', True, {'atom_id': 3, 'atom_negation': True, 'epistemic_id': 3, 'epistemic_negation': False,
                          'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'Ka', True, {'atom_id': 4, 'atom_negation': False, 'epistemic_id': 4, 'epistemic_negation': False,
                         'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'Ma', True, {'atom_id': 5, 'atom_negation': False, 'epistemic_id': 5, 'epistemic_negation': False,
                         'label': 'a', 'modality': 2, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'M-b', True, {'atom_id': 6, 'atom_negation': True, 'epistemic_id': 6, 'epistemic_negation': False,
                          'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            '-M-b', True, {'atom_id': 7, 'atom_negation': True, 'epistemic_id': 7, 'epistemic_negation': True,
                           'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            '-Mb', True, {'atom_id': 8, 'atom_negation': False, 'epistemic_id': 8, 'epistemic_negation': True,
                          'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'c', True, {'atom_id': 9, 'atom_negation': False, 'epistemic_id': None, 'epistemic_negation': False,
                        'label': 'c', 'modality': None, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            '-e', True, {'atom_id': 10, 'atom_negation': True, 'epistemic_id': None, 'epistemic_negation': False,
                         'label': 'e', 'modality': None, 'negation_as_failure': False, 'valuation': True}
        )
        self.get_atom_information_assert(
            'not d', True, {'atom_id': 11, 'atom_negation': False, 'epistemic_id': None, 'epistemic_negation': False,
                            'label': 'd', 'modality': None, 'negation_as_failure': True, 'valuation': True}
        )
        self.get_atom_information_assert(
            'not full_atom', True, {'atom_id': 12, 'atom_negation': False, 'epistemic_id': None,
                                    'epistemic_negation': False, 'label': 'full_atom', 'modality': None,
                                    'negation_as_failure': True, 'valuation': True}
        )

        self.assertRaises(ValueError, self.program.get_atom_information, 'not -d')
        self.assertRaises(ValueError, self.program.get_atom_information, 'not ~d')

    def get_atom_information_assert(self, atom_string, created_assertion, atom_compare_dict):
        test_created, test_atom = self.program.get_atom_information(atom_string)
        self.assertEqual(test_created, created_assertion)
        self.assertEqual(test_atom.__dict__, atom_compare_dict)

    def test_get_or_create_atom(self):
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=False, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=True, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=True, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), False)

    def test_check_atom_valuation(self):
        wviews = WorldViews(file_name=None)
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', atom_negation=False,
                         modality=EpistemicModality.KNOW, epistemic_negation=False, negation_as_failure=False,
                         valuation=True)
        self.assertTrue(wviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
        self.assertFalse(wviews.check_atom_valuation([{'a', 'c'}, set(), {'a', '-e'}], test_atom))
        test_atom.epistemic_negation = True
        self.assertTrue(wviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertFalse(wviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
        test_atom.modality = EpistemicModality.BELIEVE
        test_atom.epistemic_negation = False

        self.assertTrue(wviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertTrue(wviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
