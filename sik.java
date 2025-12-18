Java (SikuliX API)

import org.sikuli.script.*;

public class ImageCompare {

    public static void main(String[] args) throws Exception {

        Screen screen = new Screen();

        Pattern reference = new Pattern("expected.png").similar(0.90);
        Match match = screen.find(reference);

        if (match != null) {
            System.out.println("Images are similar");
            System.out.println("Similarity score: " + match.getScore());
        }
    }
}

🔹 getScore() returns a value between 0.0 – 1.0

Finder finder = new Finder("actual.png");
Pattern pattern = new Pattern("expected.png").similar(0.85);

finder.find(pattern);

if (finder.hasNext()) {
    Match match = finder.next();
    System.out.println("Matched with score: " + match.getScore());
} else {
    System.out.println("Images are different");
}


Map<Integer, Double> scoreMap = new HashMap<>();

for (int angle : List.of(0, 90, 180, 270)) {
    BufferedImage rotated = rotateImage(refImage, angle);
    save(rotated, "temp.png");

    Finder f = new Finder("actual.png");
    f.find(new Pattern("temp.png"));

    if (f.hasNext()) {
        scoreMap.put(angle, f.next().getScore());
    }
}

int detectedAngle = scoreMap.entrySet()
        .stream()
        .max(Map.Entry.comparingByValue())
        .get()
        .getKey();



