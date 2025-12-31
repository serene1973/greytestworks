PdfDocument pdf = new PdfDocument(new PdfReader("signed.pdf"));
SignatureUtil util = new SignatureUtil(pdf);

for (String sigName : util.getSignatureNames()) {

    PdfPKCS7 pkcs7 = util.readSignatureData(sigName);

    // signer name from certificate
    String signer = pkcs7.getSigningCertificate().getSubjectDN().getName();
    System.out.println("Signed By: " + signer);

    // signature timestamp
    java.util.Calendar cal = pkcs7.getSignDate();
    if (cal != null) {
        java.util.Date date = cal.getTime();
        System.out.println("Signed Date: " + date);
    }
}
pdf.close();
