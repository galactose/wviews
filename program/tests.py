from unittest import TestCase
from atom import Atom, EpistemicModality
from rule import Rule


class AtomTest(TestCase):
    def test_atom(self):
        test_atom = Atom(atom_id=None, epistemic_id=None, label='a', atom_negation=True,
                         epistemic_modality=EpistemicModality.KNOW, epistemic_negation=True,
                         negation_as_failure=False)
        self.assertEqual(str(test_atom), '-K-a')


class RuleTest(TestCase):
    def test_parse_rule_string(self):
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('a v c :- d, e')),
                      ('a v c :- d, e.', 'a v c :- e, d.'))
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('a :- b, c')), ('a :- b, c.', 'a :- c, b.'))
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string('d v e')), ('d v e.', 'e v d.'))
        self.assertEqual(str(Rule(head=None, tail=None).parse_rule_string('f')), 'f.')
        self.assertIn(str(Rule(head=None, tail=None).parse_rule_string(':- g, h')), (':- g, h.', ':- h, g.'))
