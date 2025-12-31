import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature;
import org.apache.pdfbox.cos.COSName;

import java.io.File;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.security.Signature;
import java.util.Calendar;
import java.util.List;
import java.util.SimpleTimeZone;

public class PdfSignatureCheck {

    public static void main(String[] args) throws Exception {

        File file = new File("signed.pdf");
        try (PDDocument doc = PDDocument.load(file)) {

            List<PDSignature> signatures = doc.getSignatureDictionaries();

            if (signatures.isEmpty()) {
                System.out.println("No Signature Found");
                return;
            }

            System.out.println("Total Signatures = " + signatures.size());
