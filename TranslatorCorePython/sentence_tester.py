from traduttore_interlingua import EnglishToItalianTranslator

sentences = ['Angus imagines a thing',
             'Irene is chasing a dog',
             'you imagine things',
             'you are imagining things',
             'you are imagining a thing',
             'there is a price on my head',
             'there is a price on my apple',
             'there is a price on your head',
             'your big opportunity is flying out of here',
             'your big opportunity fly out of here',
             'my dog is flying out of here']

sentences = ['you imagine things']

translator = EnglishToItalianTranslator()

for s in sentences:
    formula = translator.translate_sentence_to_formula(s)
    translation = translator.translate_sentence(s)
    print("\n\nFrase Input: {}\nFormula: {}\nTraduzione: {}".format(s, formula, translation))
