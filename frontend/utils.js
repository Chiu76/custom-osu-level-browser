function createElementClassContent(tagName, className, content="") {
    const element = document.createElement(tagName);
    element.className = className;
    element.innerHTML = content;
    return element;
}

export { createElementClassContent };