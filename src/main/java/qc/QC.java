package qc;

import interstitial.ISurveyResponse;
import survey.Survey;
import survey.exceptions.SurveyException;

import java.util.*;

public class QC {


    public enum QCActions {
        REJECT, BLOCK, APPROVE, DEQUALIFY
    }

    public static final Random rng = new Random(System.currentTimeMillis());

    public final static List<String> repeaters = new ArrayList<String>();
    public final static Map<String, List<String>> participantIDMap = new HashMap<String, List<String>>();
    
    public Survey survey;
    public List<ISurveyResponse> validResponses = new ArrayList<ISurveyResponse>();
    public List<ISurveyResponse> botResponses = new ArrayList<ISurveyResponse>();
    public double alpha = 0.05;

    public QC(Survey survey) throws SurveyException {
        this.survey = survey;
        participantIDMap.put(survey.sid, new ArrayList<String>());
    }

    public boolean complete(List<ISurveyResponse> responses, Properties props) {
        // this needs to be improved
        String numSamples = props.getProperty("numparticipants");
        if (numSamples!=null)
            return validResponses.size() >= Integer.parseInt(numSamples);
        else return true;
    }

    public QCActions[] assess(ISurveyResponse sr) {
        // add this survey response to the list of valid responses
        validResponses.add(sr);
        // update the frequency map to reflect this new response
        //updateFrequencyMap();
        //updateAverageLikelihoods();
        // classify this answer as a bot or not
        boolean bot = false; //isBot(sr);
        // classify any old responses as bot or not
        //updateValidResponses();
        // recompute likelihoods
        //updateAverageLikelihoods();
        List<String> participants = participantIDMap.get(survey.sid);
        /*
        if (participants.contains(sr.workerId)) {
            sr.msg = QC.QUAL;
            return new QCActions[]{ QCActions.REJECT, QCActions.DEQUALIFY };
        } else if (bot) {
            participants.add(sr.workerId);
            sr.msg = QC.BOT;
            return new QCActions[]{ QCActions.BLOCK, QCActions.DEQUALIFY };
        } else {
            //service.assignQualification("survey", a.getWorkerId(), 1, false);
            participants.add(sr.workerId);
            return new QCActions[]{ QCActions.APPROVE, QCActions.DEQUALIFY };
        }
        * */
        return new QCActions[] {QCActions.APPROVE, QCActions.DEQUALIFY};
    }


}