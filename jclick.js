JavascriptExecutor js = (JavascriptExecutor) driver;

js.executeScript(
    "var el = arguments[0];" +
    "el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));" +
    "el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));" +
    "el.dispatchEvent(new MouseEvent('click', {bubbles: true}));",
    element
);
