import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.annotation.*;
import org.apache.pdfbox.pdmodel.interactive.form.*;
import java.io.File;
import java.util.List;

public class SignaturePageFinder {

    public static void main(String[] args) throws Exception {

        PDDocument doc = PDDocument.load(new File("signed.pdf"));
        PDAcroForm form = doc.getDocumentCatalog().getAcroForm();

        if (form == null) {
            System.out.println("No AcroForm");
            return;
        }

        for (int i = 0; i < doc.getNumberOfPages(); i++) {

            List<PDAnnotation> annotations = doc.getPage(i).getAnnotations();

            for (PDAnnotation ann : annotations) {

                if (ann instanceof PDAnnotationWidget widget) {

                    PDField field = widget.getField();

                    if (field instanceof PDSignatureField sigField) {

                        if (sigField.getSignature() != null) {
                            System.out.println("✔ Signed signature on page " + (i + 1));
                        } else {
                            System.out.println("⚠ Signature field exists but NOT signed on page " + (i + 1));
                        }
                    }
                }
            }
        }

        doc.close();
    }
}
