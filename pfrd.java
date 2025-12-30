import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.text.PDFTextStripperByArea;

import java.awt.Rectangle;
import java.io.File;

public class ReadOrderSummary {
    public static void main(String[] args) throws Exception {

        PDDocument doc = PDDocument.load(new File("OrderSummary.pdf"));
        PDPage page = doc.getPage(0);

        PDFTextStripperByArea area = new PDFTextStripperByArea();

        // rectangle = x , y , width , height   (points)
        Rectangle orderNumberRect = new Rectangle(80, 100, 200, 25);
        area.addRegion("orderNo", orderNumberRect);

        area.extractRegions(page);

        String orderNo = area.getTextForRegion("orderNo").trim();
        System.out.println("Order No: " + orderNo);

        doc.close();
    }
}


PDFTextStripper stripper = new PDFTextStripper();
String text = stripper.getText(doc);

Pattern p = Pattern.compile("Order Number\\s*:?\\s*(\\S+)");
Matcher m = p.matcher(text);

if(m.find()) {
    System.out.println("Order Number: " + m.group(1));
}
