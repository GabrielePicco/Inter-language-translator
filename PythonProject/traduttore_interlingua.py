from nltk import load_parser
from py4j.java_gateway import JavaGateway
import re

from reasoner import Reasoner
from traduttore import WordTanslator, Languages

parser = load_parser('simple-sem.fcfg', trace=0)
from nltk.sem.logic import *

#sentence = 'you are imagining things'


# sentence = 'there is a price on my head'
sentence = 'your big opportunity is flying out of here'


class EnglishToItalianTranslator:

    def __init__(self):
        self.gateway = JavaGateway()
        self.italian_lexicon = self.gateway.jvm.simplenlg.lexicon.italian.ITXMLLexicon()
        self.italian_factory = self.gateway.jvm.simplenlg.framework.NLGFactory(self.italian_lexicon)
        self.realiser = self.gateway.jvm.simplenlg.realiser.Realiser()
        self.word_translator = WordTanslator(language_from=Languages.ENGLISH, language_to=Languages.ITALIAN)
        self.features = self.gateway.jvm.simplenlg.features
        self.Feature = self.gateway.jvm.simplenlg.features.Feature
        self.Tense = self.gateway.jvm.simplenlg.features.Tense
        self.Gender = self.gateway.jvm.simplenlg.features.Gender
        self.reasoner = Reasoner()

    def translate_sentence(self, sentence):
        formula = self.translate_sentence_to_formula(sentence)
        plan = self.formula_to_sentece_plan(formula)
        return self.realiser.realiseSentence(plan)

    @staticmethod
    def translate_sentence_to_formula(sentence):
        read_expr = Expression.fromstring
        tree = list(parser.parse(sentence.split()))[0]
        # print(tree)
        formula = read_expr(str(tree.label()['SEM'])).simplify()
        print(formula)
        return str(formula)

    def formula_to_sentece_plan(self, formula):
        formula = self.reasoner.make_inference(formula)
        clause_t = "clauseT\((.+?)\)"
        s = re.search(clause_t, formula)

        if s:
            clause_t = s.group(1).split(',')
            if len(clause_t) == 3:
                sbj = self.word_translator.translate_word(clause_t[0])
                subject = self.get_object_reference(sbj, formula)
                verb = self.get_verbe(clause_t[1], formula)
                obj = self.get_object_reference(clause_t[2], formula)
                clause = self.italian_factory.createClause(subject, verb, obj)
                return clause
            if len(clause_t) == 2:
                sbj = self.word_translator.translate_word(clause_t[0])
                subject = self.get_object_reference(sbj, formula)
                verb = self.get_verbe(clause_t[1], formula)
                clause = self.italian_factory.createClause(subject, verb)
                return clause

    def get_verbe(self, v, formula):
        v_t = self.word_translator.translate_word(v)
        verb = self.italian_factory.createVerbPhrase(v_t)
        verb = self.set_verb_tense(verb, v, formula)
        verb = self.set_verb_complement(verb, v, formula)
        return verb

    def get_object_reference(self, variable, formula):
        object_ref = "objectRef\({},(.+?)\)".format(variable)
        s = re.search(object_ref, formula)
        if s:
            object_props = s.group(1).split(',')
            o = self.word_translator.translate_word(object_props[0])
            obj = self.italian_factory.createNounPhrase(o)
            obj = self.set_object_specifier(obj, variable, formula)
            obj = self.manage_lexical_exception(obj)
            obj = self.set_possessive_pron(obj, variable, formula)
            obj = self.set_object_adj(obj, variable, formula)
            if object_props[1] == "pl":
                obj.setPlural(True)
            return obj
        else:
            return self.italian_factory.createNounPhrase(self.word_translator.translate_word(variable))

    def set_verb_tense(self, verb, v, formula):
        verbe_tense = "verbTense\({},(.+?)\)".format(v)
        s = re.search(verbe_tense, formula)
        if s:
            tense = s.group(1)
            if tense == "progPres":
                verb.setFeature(self.Feature.PROGRESSIVE, True)
                verb.setFeature(self.Feature.PERFECT, False)
                verb.setFeature(self.Feature.TENSE, self.Tense.PRESENT)
        return verb

    @staticmethod
    def set_object_specifier(obj, variable, formula):
        only_one = "onlyOne\({}\)".format(variable)
        if re.search(only_one, formula):
            obj.setSpecifier("il")
        else:
            obj.setSpecifier("un")
        return obj

    def set_object_adj(self, obj, variable, formula):
        adj_match = "adj\((.+?),{}\)".format(variable)
        s = re.search(adj_match, formula)
        if s:
            adj = self.italian_factory.createAdjectivePhrase(self.word_translator.translate_word(s.group(1)))
            obj.addPreModifier(adj)
        return obj

    def set_possessive_pron(self, obj, variable, formula):
        pron_match = "pronPoss\((.+?),{}\)".format(variable)
        s = re.search(pron_match, formula)
        if s:
            pron = self.italian_factory.createAdjectivePhrase(self.word_translator.translate_word(s.group(1)))
            obj.addModifier(pron)
        return obj

    def set_verb_complement(self, verb, v, formula):
        compl_match = "verbCompl\({},(.+?)\)".format(v)
        s = re.search(compl_match, formula)
        if s:
            compl_variable = s.group(1)
            compl_int_match = "compl\({},(.+?)\)".format(compl_variable)
            s_int = re.search(compl_int_match, formula)
            if s_int:
                compl = s_int.group(1).split(",")
                if len(compl) == 1:
                    verb.addComplement(self.word_translator.translate_word(compl[0]))
        return verb

    def manage_lexical_exception(self, obj):
        if "opportunità" in obj.getNoun().toString():
            obj.setFeature(self.features.LexicalFeature.GENDER, self.Gender.FEMININE)
        return obj


translator = EnglishToItalianTranslator()
print(translator.translate_sentence(sentence))
