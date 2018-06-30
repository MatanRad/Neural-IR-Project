import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonReader;
import com.sun.xml.internal.bind.api.impl.NameConverter;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.json.JSONObject;


import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class Main {

    public static void index(String path, IndexWriter writer) throws IOException{

        writer.deleteAll();

        Gson gson = new Gson();
        JsonReader reader = new JsonReader(new FileReader(path));
        ArrayList<Data> data = gson.fromJson(reader, new TypeToken<ArrayList<Data>>(){}.getType());

        int count = 0;
        for(Data doc: data){
            count++;
            System.out.println(count);
            for(String answer: doc.getNbestanswers()){
                Document temp = new Document();
                temp.add(new TextField("answer", answer, Field.Store.YES));
                temp.add(new StringField("id", doc.getId(), Field.Store.YES));
                //System.out.println(temp);
                writer.addDocument(temp);
                //System.out.println(writer.addDocument(temp));
            }
        }
        writer.commit();
        writer.close();
    }


    public static List<Answer> retrieve(Query query, IndexSearcher searcher, int n) throws IOException{
        TopDocs results = searcher.search(query, n);
        System.out.println("Found: " + results.totalHits);
        List<Answer> answers = new ArrayList<>();
        for( ScoreDoc scoreDoc : results.scoreDocs){
            Document doc = searcher.doc(scoreDoc.doc);
            Answer temp = Answer.fromDoc(doc);
            temp.setScore(Float.toString(scoreDoc.score));
            answers.add(temp);
        }

//        for(Answer answer : answers){
//            System.out.println(answer.getAnswer());
//        }
        return answers;
    }


    public static void write_answers(String path, List<Result> results) throws IOException
    {
        Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create();
        try(Writer writer = new FileWriter(path))
        {
            gson.toJson(results, new ArrayList<Result>().getClass(), writer);
        }
    }

    public static void writeQuestions(String pathToJson, String pathToOutput) throws IOException{
        Gson gson = new Gson();
        JsonReader reader = new JsonReader(new FileReader(pathToJson));
        ArrayList<Data> data = gson.fromJson(reader, new TypeToken<ArrayList<Data>>(){}.getType());
        BufferedWriter writer = new BufferedWriter(new FileWriter(pathToOutput));

        for (Data question : data){
            String id = question.getId();
            String q = question.getQuestion().replace("\n", "\\n");
            writer.write(id + '\t' + q);
            writer.newLine();
        }
        writer.close();
    }


    public static void main(String[] args){

        try{
            // writeQuestions("..\\data\\anfL6.json", "..\\exampleTestQuestions.txt");

            // ------------------ initialization ------------------ //
            Analyzer enAnalyzer = new EnglishAnalyzer();
            IndexWriterConfig conf = new IndexWriterConfig(enAnalyzer);
            Similarity sim = new ClassicSimilarity();
            conf.setSimilarity(sim);
            conf.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND);


            Directory dir = FSDirectory.open(Paths.get("..\\data\\out"));
            IndexWriter iw = new IndexWriter(dir, conf);
            System.out.println("init complete");

            // ------------------ index the database ------------------ //
            index("..\\data\\anfL6.json", iw);

            System.out.println("indexing complete");

            IndexReader ir = DirectoryReader.open(dir);
            IndexSearcher is = new IndexSearcher(ir);
            is.setSimilarity(sim);

            System.out.println("index searcher ready");


            BufferedReader reader = new BufferedReader(new FileReader("..\\all_questions.txt")); // read questions from file
            String line;
            List<Result> results = new ArrayList<>();
            int count = 0;
            while((line = reader.readLine()) != null){
                count++;
                System.out.println(count);
                String id = line.split("\\s+")[0];
                String[] query = line.split("\\s+"); // split questions into id and query
                query = Arrays.copyOfRange(query, 1, query.length);
                BooleanQuery.Builder qBuilder = new BooleanQuery.Builder();
                for(String term : query){
                    qBuilder.add(new TermQuery(new Term("answer", term)), BooleanClause.Occur.SHOULD);
                }
                Query q = qBuilder.build();

                List<Answer> res = retrieve(q, is, 5); // retrieve answers for questions
                Result temp = new Result(id, res);
                results.add(temp); //and store the results
                //writeJson(res, id);
            }
            write_answers("../data/res.json", results); // after getting all the results write them to file


        } catch(IOException e){
            System.out.println("IO Exception!");
        //} catch(ParseException e) {
        //    System.out.println("Parse Exception!");
        } catch(Exception e){
            System.out.println("Exception!");
        }


    }
}
