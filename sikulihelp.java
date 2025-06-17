import org.sikuli.script.*;

public class SikuliUtils {
    private static final Screen screen = new Screen();

    // Waits and clicks the image with retries
    public static boolean waitAndClick(String imagePath, int timeoutSeconds, int retryCount) {
        for (int i = 0; i < retryCount; i++) {
            try {
                System.out.println("Attempt " + (i + 1) + ": waiting for " + imagePath);
                Match match = screen.wait(imagePath, timeoutSeconds);
                if (match != null) {
                    System.out.println("Match found: clicking " + imagePath);
                    match.highlight(0.5); // optional debug flash
                    screen.click(match);
                    return true;
                }
            } catch (FindFailed e) {
                System.out.println("Image not found on attempt " + (i + 1));
            }

            sleep(500); // short wait before retry
        }

        System.err.println("Failed to click " + imagePath + " after " + retryCount + " retries.");
        return false;
    }

    // Clicks a field and types text
    public static boolean waitClickAndType(String imagePath, String text, int timeoutSeconds, int retryCount) {
        if (waitAndClick(imagePath, timeoutSeconds, retryCount)) {
            sleep(300); // wait for field to focus
            screen.type(text);
            return true;
        }
        return false;
    }

    // Focuses app and waits briefly
    public static void focusApp(String appTitle) {
        try {
            App app = App.focus(appTitle);
            if (app != null) {
                System.out.println("Focused on app: " + appTitle);
                sleep(1000); // wait to settle
            }
        } catch (Exception e) {
            System.err.println("Failed to focus app: " + appTitle);
        }
    }

    // Utility sleep
    private static void sleep(int millis) {
        try { Thread.sleep(millis); } catch (InterruptedException e) { }
    }
}


public class TestSikuliActions {
    public static void main(String[] args) {
        SikuliUtils.focusApp("Software Center");

        boolean clicked = SikuliUtils.waitAndClick("submit.png", 5, 3);
        if (!clicked) {
            System.out.println("Submit button not found.");
            return;
        }

        boolean typed = SikuliUtils.waitClickAndType("input_field.png", "Test Input", 5, 2);
        if (!typed) {
            System.out.println("Typing failed.");
        }
    }
}

