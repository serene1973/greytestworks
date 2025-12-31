import org.apache.pdfbox.cos.COSBase;
import org.apache.pdfbox.cos.COSDictionary;
import org.apache.pdfbox.cos.COSName;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.annotation.*;
import org.apache.pdfbox.pdmodel.interactive.form.*;

import java.io.File;
import java.util.List;

public class SignaturePageFinder_2032 {
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

                if (ann instanceof PDAnnotationWidget) {

                    PDAnnotationWidget widget = (PDAnnotationWidget) ann;

                    COSBase parent = widget.getCOSObject().getDictionaryObject(COSName.PARENT);

                    if (parent instanceof COSDictionary) {

                        PDField field = PDField.fromDictionary(form, (COSDictionary) parent);

                        if (field instanceof PDSignatureField) {

                            PDSignatureField sigField = (PDSignatureField) field;

                            if (sigField.getSignature() != null)
                                System.out.println("✔ Signed signature on page " + (i + 1));
                            else
                                System.out.println("⚠ Signature field exists but NOT signed on page " + (i + 1));
                        }
                    }
                }
            }
        }

        doc.close();
    }
}
