import { openapiSchemas } from "../api.js";

const schemas = await openapiSchemas();

function createElementClassContent(type, className="", content="", displayNone=false) {
    const element = document.createElement(type);
    element.className = className;
    element.textContent = content;
    if (displayNone) element.style = "display: none";
    return element;
}

export { createElementClassContent, schemas };