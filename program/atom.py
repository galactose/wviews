"""
    atom.py: atom structures for worldview solving

    Copyright (C) 2014  Michael Kelly

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class EpistemicModality(object):
    KNOW = 1
    BELIEVE = 2


class Atom(object):
    def __init__(self, label, atom_negation=False, atom_id=None,
                 label_id=None):
        self.atom_id = atom_id
        self.label_id = label_id
        self.atom_negation = atom_negation
        self.label = label

    def valuation_string(self, apply_valuation=False):
        return '%s%s' % ('-' if self.atom_negation else '', self.label)

    def __str__(self):
        return '%s%s' % ('-' if self.atom_negation else '', self.label)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__str__())


class EpistemicAtom(Atom):
    def __init__(self, label, modality, atom_id=None, label_id=None,
                 atom_negation=False, epistemic_negation=False,
                 valuation=None):
        super(EpistemicAtom, self).__init__(
            label, atom_negation, atom_id, label_id
        )
        self.modality = modality
        self.epistemic_negation = epistemic_negation
        self.valuation = valuation
        if self.modality is None:
            raise ValueError

    @property
    def modality_string(self):
        return 'K' if self.modality == EpistemicModality.KNOW else 'M'

    def __str__(self):
        return '%s%s%s%s' % (
            '-' if self.epistemic_negation else '', self.modality_string,
            '-' if self.atom_negation else '', self.label
        )

    def valuation_string(self, apply_valuation=False):
        if apply_valuation and self.valuation:
            return ''
        return '%s%s' % ('-' if self.atom_negation else '', self.label)


class NegationAsFailureAtom(Atom):
    def __init__(self, label, atom_negation, atom_id=None, label_id=None):
        super(NegationAsFailureAtom, self).__init__(
            label, atom_negation, atom_id, label_id
        )

    def valuation_string(self, apply_valuation=False):
        return 'not %s%s' % ('-' if self.atom_negation else '', self.label)

    def __str__(self):
        return 'not %s%s' % ('-' if self.atom_negation else '', self.label)
