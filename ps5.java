import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.form.*;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotationWidget;
import java.io.File;
import java.util.List;

public class SignaturePageCheck {
    public static void main(String[] args) throws Exception {

        PDDocument doc = PDDocument.load(new File("signed.pdf"));

        PDAcroForm form = doc.getDocumentCatalog().getAcroForm();

        if (form == null) {
            System.out.println("No form fields");
            return;
        }

        int pageIndexToCheck = 1;  // 0 = first page, 1 = second, etc.

        for (PDField field : form.getFieldTree()) {
            if (field instanceof PDSignatureField) {
                PDSignatureField sigField = (PDSignatureField) field;

                List<PDAnnotationWidget> widgets = sigField.getWidgets();

                for (PDAnnotationWidget w : widgets) {
                    int pageIndex = doc.getPages().indexOf(w.getPage());

                    if (pageIndex == pageIndexToCheck) {
                        if (sigField.getSignature() != null) {
                            System.out.println("✔ Signed signature found on page " + (pageIndex + 1));
                        } else {
                            System.out.println("⚠ Signature field exists on page but NOT signed");
                        }
                    }
                }
            }
        }

        doc.close();
    }
}
