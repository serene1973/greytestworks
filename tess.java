BufferedImage image = ImageIO.read(new File("sample.png"));

import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

public class ImageRotationCheck {

    public static void main(String[] args) throws Exception {

        ITesseract tesseract = new Tesseract();
        tesseract.setDatapath("C:/Program Files/Tesseract-OCR/tessdata");

        // Important: Enable OSD
        tesseract.setLanguage("osd");
        tesseract.setPageSegMode(0); // PSM_OSD_ONLY

        String osdResult = tesseract.doOCR(
                ImageIO.read(new File("sample.png"))
        );

        System.out.println(osdResult);
    }
}



public static int getRotationAngle(String osdText) {
    Pattern pattern = Pattern.compile("Orientation in degrees:\\s*(\\d+)");
    Matcher matcher = pattern.matcher(osdText);

    if (matcher.find()) {
        return Integer.parseInt(matcher.group(1));
    }
    return -1;
}

int angle = getRotationAngle(osdResult);

if (angle == 90) {
    System.out.println("Image is rotated by 90 degrees");
}





