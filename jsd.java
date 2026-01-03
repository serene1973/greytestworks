(function waitForPdfToolbar() {
  const viewer = document.querySelector('pdf-viewer');
  if (viewer && viewer.shadowRoot) {
    const toolbar = viewer.shadowRoot.querySelector('#toolbar');
    if (toolbar && toolbar.shadowRoot) {
      const btn = toolbar.shadowRoot
        .querySelector('cr-toolbar')?.shadowRoot
        ?.querySelector('#download')?.shadowRoot
        ?.querySelector('#save');

      if (btn) {
        btn.click();
        return;
      }
    }
  }
  setTimeout(waitForPdfToolbar, 200);
})();


JavascriptExecutor js = (JavascriptExecutor) driver;

js.executeAsyncScript("""
  const callback = arguments[arguments.length - 1];

  (function waitForPdf() {
    const viewer = document.querySelector('pdf-viewer');
    if (viewer && viewer.shadowRoot) {
      const toolbar = viewer.shadowRoot.querySelector('#toolbar');
      if (toolbar && toolbar.shadowRoot) {
        const btn = toolbar.shadowRoot
          .querySelector('cr-toolbar')?.shadowRoot
          ?.querySelector('#download')?.shadowRoot
          ?.querySelector('#save');

        if (btn) {
          btn.click();
          callback('clicked');
          return;
        }
      }
    }
    setTimeout(waitForPdf, 200);
  })();
""");
