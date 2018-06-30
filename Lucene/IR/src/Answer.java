import org.apache.lucene.document.Document;

public class Answer {
    String answer;
    String score;

    public Answer(String answer, String score) {
        this.answer = answer;
        this.score = score;
    }

    public static Answer fromDoc(Document doc){
        String answer = doc.getValues("answer")[0];
        String score = "0";
        return new Answer(answer, score);
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getScore() {
        return score;
    }

    public void setScore(String score) {
        this.score = score;
    }
}
