import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.Signature;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Calendar;
import java.util.List;

public class PdfSignatureCheck {

    public static void main(String[] args) throws Exception {

        File file = new File("signed.pdf");

        try (PDDocument document = PDDocument.load(file);
             InputStream fis = new FileInputStream(file)) {

            List<PDSignature> sigList = document.getSignatureDictionaries();

            if (sigList.isEmpty()) {
                System.out.println("No signatures found");
                return;
            }

            System.out.println("Total signatures = " + sigList.size());

            for (PDSignature sig : sigList) {

                System.out.println("================================");
                System.out.println("Name      : " + sig.getName());
                System.out.println("Reason    : " + sig.getReason());
                System.out.println("Location  : " + sig.getLocation());

                Calendar cal = sig.getSignDate();
                System.out.println("Signed On : " + (cal != null ? cal.getTime() : "NULL"));

                boolean valid = verify(sig, fis);
                System.out.println("Signature Valid : " + valid);
            }
        }
    }

    private static boolean verify(PDSignature signature, InputStream pdfStream) {
        try {
            byte[] signedContent = signature.getSignedContent(pdfStream);
            byte[] signatureBytes = signature.getContents();

            // Get cert
            CertificateFactory cf = CertificateFactory.getInstance("X.509");
            X509Certificate cert =
                    (X509Certificate) cf.generateCertificate(signature.getCertificates().get(0).getInputStream());

            Signature sig = Signature.getInstance("SHA256withRSA");
            sig.initVerify(cert);
            sig.update(signedContent);

            return sig.verify(signatureBytes);

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
