function clickPdfSaveButton(timeout = 5000) {
  const start = Date.now();

  (function waitForButton() {
    try {
      document
        .querySelector('pdf-viewer')
        ?.shadowRoot
        ?.querySelector('#toolbar')
        ?.shadowRoot
        ?.querySelector('#toolbar')
        ?.querySelector('#downloads')
        ?.shadowRoot
        ?.querySelector('#save')
        ?.click();
    } catch (e) {
      // ignore
    }

    if (Date.now() - start < timeout) {
      setTimeout(waitForButton, 200);
    } else {
      console.error('PDF save button not found within timeout');
    }
  })();
}


public static void clickPdfSaveButton(WebDriver driver) {
    JavascriptExecutor js = (JavascriptExecutor) driver;

    js.executeAsyncScript("""
        const callback = arguments[arguments.length - 1];
        const start = Date.now();

        (function waitForButton() {
          try {
            document
              .querySelector('pdf-viewer')
              ?.shadowRoot
              ?.querySelector('#toolbar')
              ?.shadowRoot
              ?.querySelector('#toolbar')
              ?.querySelector('#downloads')
              ?.shadowRoot
              ?.querySelector('#save')
              ?.click();

            callback('clicked');
            return;
          } catch (e) {
            // ignore
          }

          if (Date.now() - start < 5000) {
            setTimeout(waitForButton, 200);
          } else {
            callback('not found');
          }
        })();
    """);
}
