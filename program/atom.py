
class EpistemicModality(object):
    KNOW = 1
    BELIEVE = 2


class Atom(object):
    def __init__(self, atom_id, label, atom_negation=False, modality=None, epistemic_negation=False,
                 negation_as_failure=False, valuation=None):
        self.atom_id = atom_id
        self.atom_negation = atom_negation
        self.label = label
        self.modality = modality
        self.epistemic_negation = epistemic_negation
        self.negation_as_failure = negation_as_failure
        self.valuation = valuation
        if self.modality is None and self.epistemic_negation:
            raise ValueError

    @property
    def modality_string(self):
        if self.modality is not None:
            return 'K' if self.modality == EpistemicModality.KNOW else 'M'
        return ''

    def valuation_string(self, apply_valuation=False):
        if apply_valuation and self.modality and self.valuation:
            return ''
        return '%s%s' % ('-' if self.atom_negation else '', self.label)

    def __str__(self):
        return '%s%s%s%s' % ('-' if self.epistemic_negation else '', self.modality_string,
                             '-' if self.atom_negation else '', self.label)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__str__())
