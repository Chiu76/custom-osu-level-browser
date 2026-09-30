import { openapiSchemas } from "../api.js";

const schemas = await openapiSchemas();

function createElementClassContent(type, className, content="") {
    const element = document.createElement(type);
    element.className = className;
    element.innerHTML = content;
    return element;
}

export { createElementClassContent, schemas };