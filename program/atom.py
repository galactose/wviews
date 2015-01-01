
class EpistemicModality(object):
    KNOW = 1
    BELIEVE = 2


class Atom(object):
    def __init__(self, atom_id, epistemic_id, label, atom_negation=False, epistemic_modality=None,
                 epistemic_negation=False, negation_as_failure=False, valuation=True):
        self.atom_id = atom_id
        self.epistemic_id = epistemic_id
        self.atom_negation = atom_negation
        self.label = label
        self.modality = epistemic_modality
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

    @property
    def valuation_string(self, apply_valuation=False):
        if apply_valuation and not self.valuation:
            return ''
        return '%s%s' % ('-' if self.atom_negation else '', self.label)

    def __str__(self):
        return '%s%s%s%s' % ('-' if self.epistemic_negation else '', self.modality_string,
                             '-' if self.atom_negation else '', self.label)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__str__())
