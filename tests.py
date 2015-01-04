from unittest import TestCase
from mock import MagicMock

from program.atom import Atom, EpistemicModality
from program.program import LogicProgram
from wviews import WorldViews


class EndToEndTest(TestCase):
    def test_epistemic_program(self):
        world_view_generator = WorldViews('examples/interview_grounded.elp')
        test_worldview = world_view_generator.generate_worldview().next()
        self.assertSetEqual(test_worldview[0], {'highGPA(alice)', 'eligible(alice)', 'interview(alice)'})
        self.assertSetEqual(test_worldview[1], {'fairGPA(alice)', 'interview(alice)'})

    def test_conflict(self):
        world_view_generator = WorldViews('examples/conflict.elp')
        test_worldview = world_view_generator.generate_worldview().next()
        self.assertSetEqual(test_worldview[0], {'a', 'b', 'c'})


class OptimiseTest(TestCase):
    def setUp(self):
        self.program = LogicProgram(MagicMock())

    def test_get_atom_information(self):
        self.assertEqual(self.program.get_atom_information('-K-a').__dict__,
                         {'atom_id': 1, 'atom_negation': True, 'epistemic_negation': True,
                          'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-Ka').__dict__,
                         {'atom_id': 2, 'atom_negation': False, 'epistemic_negation': True,
                          'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('K-a').__dict__,
                         {'atom_id': 3, 'atom_negation': True, 'epistemic_negation': False,
                          'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('Ka').__dict__,
                         {'atom_id': 4, 'atom_negation': False, 'epistemic_negation': False,
                         'label': 'a', 'modality': 1, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('Ma').__dict__,
                         {'atom_id': 5, 'atom_negation': False, 'epistemic_negation': False,
                         'label': 'a', 'modality': 2, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('M-b').__dict__,
                         {'atom_id': 6, 'atom_negation': True, 'epistemic_negation': False,
                          'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-M-b').__dict__,
                         {'atom_id': 7, 'atom_negation': True, 'epistemic_negation': True,
                          'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-Mb').__dict__,
                         {'atom_id': 8, 'atom_negation': False, 'epistemic_negation': True,
                          'label': 'b', 'modality': 2, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('c').__dict__,
                         {'atom_id': 9, 'atom_negation': False, 'epistemic_negation': False,
                          'label': 'c', 'modality': None, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('-e').__dict__,
                         {'atom_id': 10, 'atom_negation': True, 'epistemic_negation': False,
                          'label': 'e', 'modality': None, 'negation_as_failure': False, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('not d').__dict__,
                         {'atom_id': 11, 'atom_negation': False, 'epistemic_negation': False,
                          'label': 'd', 'modality': None, 'negation_as_failure': True, 'valuation': None})

        self.assertEqual(self.program.get_atom_information('not full_atom').__dict__,
                         {'atom_id': 12, 'atom_negation': False, 'epistemic_negation': False, 'label': 'full_atom',
                          'modality': None, 'negation_as_failure': True, 'valuation': None})

        self.assertRaises(ValueError, self.program.get_atom_information, 'not -d')
        self.assertRaises(ValueError, self.program.get_atom_information, 'not ~d')

    def test_get_or_create_atom(self):
        test_atom = Atom(atom_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=False, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(atom_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=True, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), True)
        test_atom = Atom(atom_id=None, label='a', modality=EpistemicModality.KNOW,
                         epistemic_negation=False, atom_negation=True, negation_as_failure=False)
        self.assertEqual(self.program.get_or_create_atom(test_atom), False)

    def test_check_atom_valuation(self):
        worldviews = WorldViews(file_name=None)
        test_atom = Atom(atom_id=None, label='a', atom_negation=False, modality=EpistemicModality.KNOW,
                         epistemic_negation=False, negation_as_failure=False, valuation=True)
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))

        self.assertFalse(worldviews.check_atom_valuation([{'a', 'c'}, set(), {'a', '-e'}], test_atom))
        test_atom.epistemic_negation = True
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertFalse(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
        test_atom.modality = EpistemicModality.BELIEVE
        test_atom.epistemic_negation = False
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
