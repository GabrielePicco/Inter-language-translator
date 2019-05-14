import re


class Reasoner:

    @staticmethod
    def make_inference(formula):
        formula = Reasoner.induce_verb_complement(formula)
        formula = Reasoner.induce_away(formula)
        return formula

    @staticmethod
    def induce_away(formula):
        rule_1 = "compl\((.+?),out,of,here\)"
        s = re.search(rule_1, formula)
        if s:
            formula = formula.replace(s.group(0), "compl({},away)".format(s.group(1)))
        return formula

    @staticmethod
    def induce_verb_complement(formula):
        rule_0_a = "compl\((.+?),(.+?)\)"
        rule_0_b = "clauseT\((.+?),(.+?)\)"
        r0_a = re.search(rule_0_a, formula)
        r0_b = re.search(rule_0_b, formula)
        if r0_a and r0_b and r0_b.lastindex >= 2 and r0_a.lastindex >= 1 and r0_b.group(1) == r0_a.group(1):
            formula = formula.replace(r0_b.group(0), "verbCompl({},{})".format(r0_b.group(2), r0_a.group(1)))
        return formula
