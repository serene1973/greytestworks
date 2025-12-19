Image original = new Region(x,y,w,h).getImage();
Image rotated90 = new Region(x,y,w,h).getImage();
Image rotated180 = new Region(x,y,w,h).getImage();
Image rotated270 = new Region(x,y,w,h).getImage();

double score0 = getScore(original, original);
double score90 = getScore(original, rotated90);
double score180 = getScore(original, rotated180);
double score270 = getScore(original, rotated270);

System.out.println("0   : " + score0);
System.out.println("90  : " + score90);
System.out.println("180 : " + score180);
System.out.println("270 : " + score270);


public static double getScore(Image base, Image candidate) {
    Finder finder = new Finder(candidate);
    finder.find(base);

    if (finder.hasNext()) {
        Match m = finder.next();
        return m.getScore();  // 0.0 - 1.0
    }
    return 0.0;
}
