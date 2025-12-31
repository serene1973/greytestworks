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

            for (PDSignature sig : signatures) {

                System.out.println("================================");
                System.out.println("Name      : " + sig.getName());
                System.out.println("Reason    : " + sig.getReason());
                System.out.println("Location  : " + sig.getLocation());

                Calendar cal = sig.getSignDate();
                if (cal != null)
                    System.out.println("Signed On : " + cal.getTime());
                else
                    System.out.println("Signed On : NULL");

                boolean valid = verifySignature(doc, sig);
                System.out.println("Signature Valid : " + valid);
            }
        }
    }

    private static boolean verifySignature(PDDocument document, PDSignature signature) {
        try {
            byte[] signedContent = signature.getSignedContent(document);
            byte[] signatureBytes = signature.getContents(document);

            Signature sig = Signature.getInstance(signature.getSubFilter());
            sig.initVerify(getCert(signature));
            sig.update(signedContent);

            return sig.verify(signatureBytes);
        } catch (Exception e) {
            return false;
        }
    }

    private static X509Certificate getCert(PDSignature sig) throws Exception {
        byte[] certBytes = sig.getCOSObject().getCOSArray(COSName.CONTENTS).getBytes();
        CertificateFactory factory = CertificateFactory.getInstance("X.509");
        return (X509Certificate) factory.generateCertificate(new java.io.ByteArrayInputStream(certBytes));
    }
}
