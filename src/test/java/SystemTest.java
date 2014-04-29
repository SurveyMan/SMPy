import input.csv.CSVLexer;
import input.csv.CSVParser;
import interstitial.ResponseWriter;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import qc.RandomRespondent;
import survey.Survey;
import survey.exceptions.SurveyException;
import system.SurveyResponse;
import system.generators.HTML;
import system.mturk.generators.MturkHTML;
import system.mturk.generators.MturkXML;

import java.io.StringReader;

@RunWith(JUnit4.class)
public class SystemTest extends TestLog {

    public SystemTest() {
        super.init(this.getClass());
    }

    @Test
    public void testMturkHTMLGenerator() throws Exception {
        try{
            for ( int i = 0 ; i < testsFiles.length ; i++ ) {
                CSVParser csvParser = new CSVParser(new CSVLexer(testsFiles[i], String.valueOf(separators[i])));
                HTML.getHTMLString(csvParser.parse(), new MturkHTML());
                LOGGER.info(testsFiles[i]+" generated IHTML successfully.");
            }
        } catch (SurveyException se) {
            LOGGER.warn(se);
        }
    }

    @Test
    public void testXMLGenerator() throws Exception {
        try{
            for (int i = 0 ; i < testsFiles.length ; i++) {
                CSVParser csvParser = new CSVParser(new CSVLexer(testsFiles[i], String.valueOf(separators[i])));
                MturkXML.getXMLString(csvParser.parse());
                LOGGER.info(testsFiles[i]+" generated IHTML successfully.");
            }
        } catch (SurveyException se) {
            LOGGER.warn(se);
        }
    }

    @Test
    public void testColumnPipeline() throws Exception {
        for (int i = 0 ; i < testsFiles.length ; i++) {
            System.out.println("File:"+testsFiles[i]);
            CSVParser csvParser = new CSVParser(new CSVLexer(testsFiles[i], String.valueOf(separators[i])));
            Survey survey = csvParser.parse();
            RandomRespondent rr = new RandomRespondent(survey, RandomRespondent.AdversaryType.UNIFORM);
            String headers = ResponseWriter.outputHeaders(survey);
            System.out.println(headers);
            String output = ResponseWriter.outputSurveyResponse(survey, rr.response);
            System.out.println(output);
            new SurveyResponse("").readSurveyResponses(survey, new StringReader(headers + output));
        }
    }

    @Test
    public void testCorrelatedPipeline() throws Exception {
        for (int i = 0 ; i < testsFiles.length ; i++) {
            System.out.println("File:"+testsFiles[i]);
            CSVParser csvParser = new CSVParser(new CSVLexer(testsFiles[i], String.valueOf(separators[i])));
            Survey survey = csvParser.parse();
            if (!survey.correlationMap.isEmpty()) {
                System.out.println("input specifies correlations "+survey.correlationMap.entrySet());
                RandomRespondent rr = new RandomRespondent(survey, RandomRespondent.AdversaryType.UNIFORM);
                String headerString = ResponseWriter.outputHeaders(survey);
                assert(headerString.contains(Survey.CORRELATION));
                String[] headers = headerString.split(",");
                // write a function to actually parse in the correlations and check against correlationMap
            }
        }
        System.out.println("Success");
    }

    public void testOptionRandomization() throws Exception {

    }
}