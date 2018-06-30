import java.util.Arrays;

public class Data {
    private String main_category;
    private String question;
    private String[] nbestanswers;
    private String answer;
    private String id;

    public Data(String main_category, String question, String[] nbestanswers, String answer, String id) {
        this.main_category = main_category;
        this.question = question;
        this.nbestanswers = nbestanswers;
        this.answer = answer;
        this.id = id;
    }

    @Override
    public String toString() {
        return "Data{" + '\n' +
                " mainCategory='" + main_category + '\'' + '\n' +
                " question='" + question + '\'' + '\n' +
                " nbestanswers=" + Arrays.toString(nbestanswers) + '\n' +
                " answer='" + answer + '\'' + '\n' +
                " id='" + id + '\'' +
                '}';
    }

    public String getMainCategory() {
        return main_category;
    }

    public void setMainCategory(String mainCatagory) {
        this.main_category = mainCatagory;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String[] getNbestanswers() {
        return nbestanswers;
    }

    public void setNbestanswers(String[] nbestanswers) {
        this.nbestanswers = nbestanswers;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

}
