import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature;
import org.bouncycastle.cms.CMSSignedData;
import org.bouncycastle.cms.SignerInformation;
import org.bouncycastle.cms.SignerInformationStore;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cms.jcajce.JcaSimpleSignerInfoVerifierBuilder;

import java.io.File;
import java.security.cert.X509Certificate;
import java.util.Collection;
import java.util.List;

public class PdfSignatureValidator {

    public static void main(String[] args) throws Exception {
        PDDocument document = PDDocument.load(new File("signed.pdf"));

        List<PDSignature> signatures = document.getSignatureDictionaries();

        if (signatures.isEmpty()) {
            System.out.println("No signatures found");
            return;
        }

        for (PDSignature sig : signatures) {

            byte[] signedContent = sig.getSignedContent(document);
            byte[] signatureBytes = sig.getContents(document);

            CMSSignedData cms = new CMSSignedData(signedContent, signatureBytes);
            SignerInformationStore signers = cms.getSignerInfos();
            Collection<SignerInformation> c = signers.getSigners();

            for (SignerInformation signer : c) {

                Collection<X509CertificateHolder> certs =
                        (Collection<X509CertificateHolder>) cms.getCertificates().getMatches(signer.getSID());

                X509CertificateHolder holder = certs.iterator().next();
                X509Certificate cert = new JcaX509CertificateConverter()
                        .setProvider("BC").getCertificate(holder);

                boolean verified = signer.verify(
                        new JcaSimpleSignerInfoVerifierBuilder()
                                .setProvider("BC")
                                .build(cert)
                );

                if (verified) {
                    System.out.println("✔ Signature is VALID");
                    System.out.println("Signed By: " + cert.getSubjectDN());
                    System.out.println("Issuer: " + cert.getIssuerDN());
                } else {
                    System.out.println("❌ Signature INVALID");
                }
            }
        }

        document.close();
    }
}
