(function clickPdfDownload(retries = 50) {
  const viewer = document.querySelector('pdf-viewer');
  if (!viewer) {
    if (retries > 0) {
      return setTimeout(() => clickPdfDownload(retries - 1), 200);
    }
    console.error('pdf-viewer not found');
    return;
  }

  const toolbar = viewer.shadowRoot?.querySelector('#toolbar');
  if (!toolbar) return setTimeout(() => clickPdfDownload(retries - 1), 200);

  const toolbar2 = toolbar.shadowRoot?.querySelector('#toolbar');
  if (!toolbar2) return setTimeout(() => clickPdfDownload(retries - 1), 200);

  const downloads = toolbar2.querySelector('#downloads');
  if (!downloads) return setTimeout(() => clickPdfDownload(retries - 1), 200);

  const save = downloads.shadowRoot?.querySelector('#save');
  if (!save) return setTimeout(() => clickPdfDownload(retries - 1), 200);

  save.click();
  console.log('PDF download clicked');
})();
