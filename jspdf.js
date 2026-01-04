(function waitForPdfViewer(retries = 50) {
  const viewer = document.querySelector('pdf-viewer');

  if (viewer) {
    console.log('PDF viewer ready');
    return viewer;
  }

  if (retries <= 0) {
    console.error('PDF viewer not initialized');
    return null;
  }

  setTimeout(() => waitForPdfViewer(retries - 1), 200);
})();
