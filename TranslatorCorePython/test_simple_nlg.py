from py4j.java_gateway import JavaGateway
gateway = JavaGateway()


italianLexicon = gateway.jvm.simplenlg.lexicon.italian.ITXMLLexicon()
italianFactory = gateway.jvm.simplenlg.framework.NLGFactory(italianLexicon)
realiser = gateway.jvm.simplenlg.realiser.Realiser()

clauseIt = italianFactory.createClause("Paolo", "amare", "Francesca")
clauseIt.setFeature(gateway.jvm.simplenlg.features.Feature.TENSE, gateway.jvm.simplenlg.features.Tense.PAST)
paragraph = italianFactory.createParagraph()
paragraph.addComponent(clauseIt)
document = italianFactory.createDocument("Traduzione: \n")
document.addComponent(paragraph)

outString = realiser.realise(document).getRealisation()
print(outString)