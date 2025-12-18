import java.awt.*;
import java.awt.image.BufferedImage;

public class ScreenCapture {

    public static BufferedImage captureFullScreen() throws Exception {
        Robot robot = new Robot();
        Rectangle screenRect =
                new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
        return robot.createScreenCapture(screenRect);
    }
}
public static BufferedImage captureRegion(int x, int y, int width, int height)
        throws Exception {

    Robot robot = new Robot();
    Rectangle rect = new Rectangle(x, y, width, height);
    return robot.createScreenCapture(rect);
}
ITesseract tesseract = new Tesseract();
tesseract.setDatapath("C:/Program Files/Tesseract-OCR/tessdata");
tesseract.setLanguage("osd");
tesseract.setPageSegMode(0); // OSD only

BufferedImage screenshot = ScreenCapture.captureRegion(200, 150, 900, 1100);

String osdResult = tesseract.doOCR(screenshot);
System.out.println(osdResult);
