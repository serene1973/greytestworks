js.executeAsyncScript("""
    const done = arguments[arguments.length - 1];

    fetch('https://vtxhoafqa.shqa.hgh.com/<<<YOUR_POST_ENDPOINT>>>', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'X-CSRF-Token': window.someTokenHere
        }
    }).then(r => done(r.status))
      .catch(e => done('ERROR:' + e));
""");
