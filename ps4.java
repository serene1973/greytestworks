import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfReader;
import com.itextpdf.signatures.SignatureUtil;
import com.itextpdf.signatures.PdfPKCS7;

import java.util.List;

public class CheckSignature {
    public static void main(String[] args) throws Exception {
        PdfDocument pdf = new PdfDocument(new PdfReader("signed.pdf"));

        SignatureUtil util = new SignatureUtil(pdf);
        List<String> names = util.getSignatureNames();

        if (names.isEmpty()) {
            System.out.println("No digital signatures found");
            return;
        }

        System.out.println("Signatures count = " + names.size());

        for (String sigName : names) {
            System.out.println("Signature name: " + sigName);

            PdfPKCS7 pkcs7 = util.readSignatureData(sigName);
            boolean valid = pkcs7.verifySignatureIntegrityAndAuthenticity();

            System.out.println(valid ? "✔ VALID signature" : "❌ INVALID signature");
            System.out.println("Signed by: " + pkcs7.getSigningCertificate().getSubjectDN());
        }

        pdf.close();
    }
}
