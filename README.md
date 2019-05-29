# Interlingua translator



## How to use

Start the simpleNLG Gateway server:

    java -jar JavaSimpleNLGGateway/SimpleNLG-GatewayServer.jar

Install the python requirements and run the test script:

    pip install TranslatorCorePython/requirements.txt
    python TranslatorCorePython/sentence_tester.py

## Examples

    Input sentence: You are imagining things.
    Formula: exists z6.(objectRef(z6,thing,pl) & clause(you,imagine,z6) & verbTense(imagine,progPres))
    Translation: Tu stai immaginando delle cose.

.

    Input sentence: There is a price on my head.
    Formula: exists x.(objectRef(x,price,sg) & exists y.(objectRef(y,head,sg) & pronPoss(my,y) & onlyOne(y) & propP(on,x,y)))
    Translation: C'è una taglia sopra la mia testa.

.

    Input sentence: Dogs are chasing Irene.
    Formula: exists x.(objectRef(x,dog,pl) & clause(x,chase,irene) & verbTense(chase,progPres))
    Translation: Dei cani stanno inseguendo irene.
