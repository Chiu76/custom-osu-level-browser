import { openapiSchemas } from "../api.js";

const schemas = await openapiSchemas();

function posixTimestampFormatter(timestamp) {
    const date = new Date(timestamp * 1000);
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${1900 + date.getYear()}.${month}.${day}`
}

function createElementClassContent(type, className="", content="", displayNone=false) {
    const element = document.createElement(type);
    element.className = className;
    element.textContent = content;
    if (displayNone) element.style = "display: none";
    return element;
}

function getModsBitwiseEnum() {
    const modsEnum = schemas["ScoreSqSpec"]["properties"]["mods_exact"]["items"]["anyOf"][1]["enum"];
    // const modsBitwise = { 0: 'nm' };
    const modsBitwise = {};
    for (let i = 1; i < modsEnum.length; i++) {
        modsBitwise[Math.pow(2, i - 1)] = modsEnum[i];
    }
    return modsBitwise;
}

function getModsString(modsBitwise) {
    let result = "";
    const modsBitwiseEnum = getModsBitwiseEnum();
    for (let mod in modsBitwiseEnum) {
        const modInt = parseInt(mod);
        if ((modsBitwise & modInt) === modInt) {
            result = result.concat(modsBitwiseEnum[mod]).toUpperCase();
        }
    }
    return result;
}

function getModsElement(modsBitwise) {
    return createElementClassContent("div", "mods", getModsString(modsBitwise) ?? "");
}

function getGradeElement(grade) {
    const element = createElementClassContent("div", "grade", grade ?? "");
    if (grade === "SS") {
        element.style.left = "2.5px";
    }
    return element;
}

export { schemas, posixTimestampFormatter, createElementClassContent, getModsElement, getGradeElement };