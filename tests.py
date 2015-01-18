from unittest import TestCase
from mock import MagicMock

from program.atom import EpistemicAtom, EpistemicModality
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

    def test_psychopath(self):
        world_view_generator = WorldViews('examples/psychopath.elp')
        worldview_generator = world_view_generator.generate_worldview()
        self.assertEqual(worldview_generator.next(), [{'-dangerous(sam)', '-psychopath(sam)', 'violent(sam)'}])
        self.assertEqual(worldview_generator.next(), [{'-dangerous(sam)', '-violent(sam)', 'psychopath(sam)'}])
        self.assertEqual(worldview_generator.next(), [{'psychopath(sam)'}, {'violent(sam)'}])

    def test_inconsistent(self):
        world_view_generator = WorldViews('examples/inconsistent.elp').generate_worldview()
        self.assertEqual(world_view_generator.next(), [{'a'}])
        self.assertRaises(StopIteration, world_view_generator.next)

    # def test_epistemic(self):
    #     world_view_generator = WorldViews('examples/epistemic.elp')
    #     test_worldview = world_view_generator.generate_worldview().next()
    #     self.assertSetEqual(test_worldview[0], {})

    def test_same(self):
        world_view_generator = WorldViews('examples/same.elp').generate_worldview()
        self.assertEqual(world_view_generator.next(), [{'d', 'c'}])
        self.assertRaises(StopIteration, world_view_generator.next)

    def test_trouble(self):
        world_view_generator = WorldViews('examples/trouble.elp').generate_worldview()
        self.assertEqual(world_view_generator.next(), [{'-b'}])
        self.assertRaises(StopIteration, world_view_generator.next)

    def test_negation_as_failure(self):
        world_view_generator = WorldViews('examples/naf.elp').generate_worldview()
        self.assertEqual(world_view_generator.next(), [{'-a(s)', '-g(s)', 'u(x)'}])
        self.assertRaises(StopIteration, world_view_generator.next)


class WorldViewsTest(TestCase):

    def test_check_atom_valuation(self):
        worldviews = WorldViews(file_name=None)
        test_atom = EpistemicAtom(label='a', atom_negation=False, modality=EpistemicModality.KNOW,
                                  epistemic_negation=False, valuation=True)
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))

        self.assertFalse(worldviews.check_atom_valuation([{'a', 'c'}, set(), {'a', '-e'}], test_atom))
        test_atom.epistemic_negation = True
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertFalse(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))
        test_atom.modality = EpistemicModality.BELIEVE
        test_atom.epistemic_negation = False
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'-e'}], test_atom))
        self.assertTrue(worldviews.check_atom_valuation([{'a', 'c'}, {'a'}, {'a', '-e'}], test_atom))