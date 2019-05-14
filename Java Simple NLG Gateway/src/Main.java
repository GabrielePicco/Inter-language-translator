import simplenlg.features.Feature;
import simplenlg.features.Gender;
import simplenlg.features.LexicalFeature;
import simplenlg.features.Tense;
import simplenlg.framework.*;
import simplenlg.lexicon.Lexicon;
import simplenlg.lexicon.italian.ITXMLLexicon;
import simplenlg.phrasespec.*;
import simplenlg.realiser.Realiser;
import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        Main app = new Main();
        GatewayServer server = new GatewayServer(app);
        server.start();

        Lexicon italianLexicon = new ITXMLLexicon();
        NLGFactory italianFactory = new NLGFactory(italianLexicon);

        Realiser realiser = new Realiser();
        //realiser.setDebugMode(true);

        SPhraseSpec clauseIt = italianFactory.createClause("prezzo", "essere");
        
        clauseIt.setFeature(Feature.TENSE, Tense.PRESENT);

        DocumentElement paragraph = italianFactory.createParagraph();
        paragraph.addComponent(clauseIt);
        DocumentElement document = italianFactory.createDocument("Traduzione: \n");
        document.addComponent(paragraph);

        String outString = realiser.realise(document).getRealisation();
        System.out.print(outString);


        NPPhraseSpec directObject = italianFactory.createNounPhrase("cosa");
        directObject = italianFactory.createNounPhrase("un", directObject.getNoun());
        NPPhraseSpec subject = italianFactory.createNounPhrase("tu");
        VPPhraseSpec verb = italianFactory.createVerbPhrase("immaginare");
        directObject.setPlural(true);
        SPhraseSpec clause = italianFactory.createClause(subject, verb, directObject);
        verb.setFeature(Feature.PROGRESSIVE, true);
        verb.setFeature(Feature.PERFECT, false);
        verb.setFeature(Feature.TENSE, Tense.PRESENT);
        String output = realiser.realiseSentence(clause);
        System.out.println("PROGRESSIVO PRESENTE");
        System.out.println("Tu stai immaginando cose -->" + output);

        subject = italianFactory.createNounPhrase("opportunita");
        subject.setSpecifier("il");
        subject.setFeature(LexicalFeature.GENDER, Gender.FEMININE);
        subject.addModifier("tua");
        AdjPhraseSpec grande = italianFactory.createAdjectivePhrase("grande");
        subject.addPreModifier(grande);
        verb = italianFactory.createVerbPhrase("volare");
        verb.addComplement("via");
        clause = italianFactory.createClause(subject, verb);
        verb.setFeature(Feature.PROGRESSIVE, true);
        verb.setFeature(Feature.PERFECT, false);
        verb.setFeature(Feature.TENSE, Tense.PRESENT);
        output = realiser.realiseSentence(clause);
        System.out.println("PROGRESSIVO PRESENTE");
        System.out.println("La tua grande opportunità sta volando via -->" + output);


        WordElement ci = italianFactory.getLexicon().getWord("ci", LexicalCategory.ADVERB);
        VPPhraseSpec vPhrase = italianFactory.createVerbPhrase("è");
        //vPhrase.setFeature(Feature.PARTICLE,"ci");
        //vPhrase.addFrontModifier(ci);

        NPPhraseSpec price = italianFactory.createNounPhrase("taglia");
        price.setSpecifier("un");
        //price.setFeature(LexicalFeature.GENDER, Gender.MASCULINE);
        NPPhraseSpec testa = italianFactory.createNounPhrase("testa");
        testa.setSpecifier("il");
        PPPhraseSpec suTesta = italianFactory.createPrepositionPhrase("su", testa);
        testa.addModifier("mia");
        price.addComplement(suTesta);
        vPhrase.setObject(price);
        output = realiser.realiseSentence(vPhrase);
        System.out.println(output);

        Lexicon englishLexicon = new simplenlg.lexicon.english.XMLLexicon();
        NLGFactory englishFactory = new NLGFactory(englishLexicon);
        System.out.println(realiser.realiseSentence(italianFactory.createClause("ci","essere", "un cane")));
        NPPhraseSpec dog = italianFactory.createNounPhrase("dog");
        dog.setSpecifier("a");
        dog.setPlural(true);
        System.out.println(realiser.realiseSentence(englishFactory.createClause("there","be", dog)));

        SPhraseSpec proposition = italianFactory.createClause(null, "essere");
        proposition.setObject("ci");
        output = realiser.realiseSentence(proposition);
        System.out.println(output);
    }
}
