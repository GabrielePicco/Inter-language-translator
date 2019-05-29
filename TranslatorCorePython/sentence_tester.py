from traduttore_interlingua import EnglishToItalianTranslator

with open("test_sentences.txt") as f:
    sentences = f.readlines()

translator = EnglishToItalianTranslator()

for s in sentences:
    formula = translator.translate_sentence_to_formula(s)
    translation = translator.translate_sentence(s)
    print("\n\nFrase Input: {}\nFormula: {}\nTraduzione: {}".format(s, formula, translation))
