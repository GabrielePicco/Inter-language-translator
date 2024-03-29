import re


class Reasoner:
    """
    Simple reasoner that infers some rule from a logical FOL formula
    """

    @staticmethod
    def make_inference(formula):
        formula = Reasoner.induce_away(formula)
        formula = Reasoner.induce_reward(formula)
        return formula

    @staticmethod
    def induce_away(formula):
        """
        If compl(x,out,of,here) => compl(x,away)
        :param formula: logical formula
        :return: logical formula
        """
        rule_1 = "compl\((.+?),out,of,here\)"
        s = re.search(rule_1, formula)
        if s:
            formula = formula.replace(s.group(0), "compl({},away)".format(s.group(1)))
        return formula

    @classmethod
    def induce_reward(cls, formula):
        """
        If propP(on,x,y) & objectRef(x,price) & objectRef(y,head) => objectRef(x,reward)
        :param formula: logical formula
        :return: logical formula
        """
        rule_on_a_b = "propP\(on,(.+?),(.+?)\)"
        rule_a_price = "objectRef\({},price,(.+?)\)"
        rule_b_head = "objectRef\({},head,(.+?)\)"
        r_on_a_b = re.search(rule_on_a_b, formula)
        if r_on_a_b and r_on_a_b.lastindex == 2:
            rule_b_head.format(r_on_a_b.group(2))
            r_a_price = re.search(rule_a_price.format(r_on_a_b.group(1)), formula)
            r_b_head = re.search(rule_b_head.format(r_on_a_b.group(2)), formula)
            if r_a_price and r_b_head:
                formula = formula.replace(r_a_price.group(0), "objectRef({},reward,{})".format(r_on_a_b.group(1),
                                                                                               r_a_price.group(1)))
        return formula

