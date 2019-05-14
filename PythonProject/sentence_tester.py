from traduttore_interlingua import EnglishToItalianTranslator

sentences = ['you are imagining things',
             'there is a price on my head',
             'your big opportunity is flying out of here']

translator = EnglishToItalianTranslator()

for s in sentences:
    formula = translator.translate_sentence_to_formula(s)
    translation = translator.translate_sentence(s)
    print("\n\nFrase Input: {}\nFormula: {}\nTraduzione: {}".format(s, formula, translation))
