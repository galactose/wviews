from unittest import TestCase

from program.atom import EpistemicAtom, EpistemicModality
from wviews import WorldViews


class EndToEndTest(TestCase):
    def test_conflict(self):
        generator = WorldViews('examples/conflict.elp')
        test_worldview = generator.generate_worldview().next()
        self.assertSetEqual(test_worldview[0], {'a', 'b', 'c'})

    def test_epistemic(self):
        generator = WorldViews('examples/epistemic.elp')
        test_worldview = generator.generate_worldview()
        # no consistent worldview, either valuation for this atom
        # will lead to a contradiction.
        self.assertRaises(StopIteration, test_worldview.next)

    def test_inconsistent(self):
        example_path = 'examples/inconsistent.elp'
        generator = WorldViews(example_path).generate_worldview()
        self.assertEqual(generator.next(), [{'a'}])
        self.assertRaises(StopIteration, generator.next)

    def test_interview_unground_end_to_end(self):
        generator = WorldViews('examples/interview.elp')
        test_worldview = generator.generate_worldview()
        wv = test_worldview.next()
        self.assertSetEqual(
            wv[0],
            {'highGPA(alice)', 'eligible(alice)', 'interview(alice)'}
        )
        self.assertSetEqual(
            wv[1],
            {'fairGPA(alice)', 'interview(alice)'}
        )
        self.assertRaises(StopIteration, test_worldview.next)

    def test_interview_variant_end_to_end(self):
        generator = WorldViews('examples/interview_variant.elp')
        test_worldview = generator.generate_worldview()
        wv = test_worldview.next()
        self.assertSetEqual(
            wv[0],
            {'minority(mary)', 'eligible(mary)', 'student(mary)', 'fairGPA(mary)'}
        )
        self.assertSetEqual(
            wv[1],
            {'minority(mary)', 'eligible(mary)', 'student(mary)', 'highGPA(mary)'}
        )
        self.assertRaises(StopIteration, test_worldview.next)

    def test_interview_variant_grounded_end_to_end(self):
        generator = WorldViews('examples/interview_variant_grounded.elp')
        test_worldview = generator.generate_worldview()
        wv = test_worldview.next()
        self.assertSetEqual(
            wv[0],
            {'minority(mary)', 'eligible(mary)', 'student(mary)', 'fairGPA(mary)'}
        )
        self.assertSetEqual(
            wv[1],
            {'minority(mary)', 'eligible(mary)', 'student(mary)', 'highGPA(mary)'}
        )
        self.assertRaises(StopIteration, test_worldview.next)

    def test_interview_ground_end_to_end(self):
        generator = WorldViews('examples/interview_grounded.elp')
        test_worldview = generator.generate_worldview()
        wv = test_worldview.next()
        self.assertSetEqual(
            wv[0],
            {'highGPA(alice)', 'eligible(alice)', 'interview(alice)'}
        )
        self.assertSetEqual(
            wv[1],
            {'fairGPA(alice)', 'interview(alice)'}
        )
        self.assertRaises(StopIteration, test_worldview.next)

    def test_negation_as_failure(self):
        generator = WorldViews('examples/negation_as_failure.elp').generate_worldview()
        self.assertEqual(generator.next(), [{'-a(s)', '-g(s)', 'u(x)'}])
        self.assertRaises(StopIteration, generator.next)

    def test_psychopath(self):
        generator = WorldViews('examples/psychopath.elp')
        worldview_generator = generator.generate_worldview()
        self.assertEqual(
            worldview_generator.next(),
            [{'-dangerous(sam)', '-psychopath(sam)', 'violent(sam)'}]
        )
        self.assertEqual(
            worldview_generator.next(),
            [{'-dangerous(sam)', '-violent(sam)', 'psychopath(sam)'}]
        )
        self.assertEqual(
            worldview_generator.next(),
            [{'psychopath(sam)'}, {'violent(sam)'}]
        )
        self.assertRaises(StopIteration, worldview_generator.next)

    def test_same(self):
        generator = WorldViews('examples/same.elp').generate_worldview()
        self.assertEqual(generator.next(), [{'d', 'c'}])
        self.assertRaises(StopIteration, generator.next)

    def test_trouble(self):
        generator = WorldViews('examples/trouble.elp').generate_worldview()
        self.assertEqual(generator.next(), [{'-b'}])
        self.assertRaises(StopIteration, generator.next)

    def test_world(self):
        generator = WorldViews('examples/set.elp')
        worldview_generator = generator.generate_worldview()
        self.assertEqual(
            worldview_generator.next(),
            [set(['p(a)', 'q(b)']), set(['p(a)', 'q(c)'])]
        )
        self.assertRaises(StopIteration, worldview_generator.next)


class WorldViewsTest(TestCase):

    def test_check_atom_valuation(self):
        wview = WorldViews(file_name=None)
        test_atom = EpistemicAtom(
            label='a', atom_negation=False, modality=EpistemicModality.KNOW,
            epistemic_negation=False, valuation=True
        )
        test_1 = [{'a', 'c'}, {'a'}, {'a', '-e'}]
        test_2 = [{'a', 'c'}, {'a'}, {'-e'}]
        test_3 = [{'a', 'c'}, set(), {'a', '-e'}]
        self.assertTrue(wview.check_atom_valuation(test_1, test_atom))
        self.assertFalse(wview.check_atom_valuation(test_3, test_atom))
        test_atom.epistemic_negation = True
        self.assertTrue(wview.check_atom_valuation(test_2, test_atom))
        self.assertFalse(wview.check_atom_valuation(test_1, test_atom))
        test_atom.modality = EpistemicModality.BELIEVE
        test_atom.epistemic_negation = False
        self.assertTrue(wview.check_atom_valuation(test_2, test_atom))
        self.assertTrue(wview.check_atom_valuation(test_1, test_atom))
