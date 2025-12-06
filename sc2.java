import java.io.*;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

public class SauceConnectManager {

    private Process scProcess;

    // --- Stream handler for async log reading ---
    private static class StreamGobbler implements Runnable {
        private InputStream inputStream;
        private Consumer<String> consumer;

        public StreamGobbler(InputStream inputStream, Consumer<String> consumer) {
            this.inputStream = inputStream;
            this.consumer = consumer;
        }

        @Override
        public void run() {
            new BufferedReader(new InputStreamReader(inputStream)).lines()
                    .forEach(consumer);
        }
    }

    // --- Start Sauce Connect ---
    public void startTunnel(String username, String accessKey, String tunnelName) throws Exception {

        ProcessBuilder pb = new ProcessBuilder(
                "sc",
                "-u", username,
                "-k", accessKey,
                "--tunnel-name", tunnelName
        );

        pb.redirectErrorStream(true);
        scProcess = pb.start();

        // Read logs asynchronously
        StreamGobbler streamGobbler = new StreamGobbler(
                scProcess.getInputStream(),
                (line) -> System.out.println("[SC] " + line)
        );

        Executors.newSingleThreadExecutor().submit(streamGobbler);

        // Wait until SC is ready
        waitUntilReady();
    }

    // --- Wait until Sauce Connect is fully up ---
    private void waitUntilReady() throws Exception {
        System.out.println("[SC] Waiting for Sauce Connect to be ready...");

        BufferedReader reader = new BufferedReader(new InputStreamReader(scProcess.getInputStream()));
        String line;

        while ((line = reader.readLine()) != null) {
            if (line.contains("Sauce Connect is up")) {
                System.out.println("[SC] Tunnel is online and ready!");
                break;
            }

            if (line.contains("Goodbye.") || line.contains("failed")) {
                throw new RuntimeException("Sauce Connect failed to start: " + line);
            }
        }
    }

    // --- Stop Sauce Connect ---
    public void stopTunnel() {
        if (scProcess != null && scProcess.isAlive()) {
            System.out.println("[SC] Stopping Sauce Connect...");
            scProcess.destroy();
        }
    }
}
