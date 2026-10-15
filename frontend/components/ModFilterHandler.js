import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";

export function ModFilterHandler(parentId) {
    const [modFilter, setModFilter] = createSignal([]);

    const filterParent = document.getElementById(parentId);
    const filterInput = filterParent.getElementsByTagName("input")[0];

    const fieldValuesDefault = schemas["ScoreSqSpec"]["properties"]["mods_exact"]["items"]["anyOf"][0]["enum"];
    const fieldValuesAlts = schemas["ScoreSqSpec"]["properties"]["mods_exact"]["items"]["anyOf"][1]["enum"];
    const fieldValues = fieldValuesDefault.concat(fieldValuesAlts);

    function assertField(mod) {
        return fieldValues.includes(mod);
    }

    function parseFilters(filters) {
        // assumes input is an array of filter strings, such as:
        // ["hd", "doubletime"]
        const result = [];
        for (let filter of filters) {
            filter = filter.toLowerCase();
            if (!assertField(filter)) {
                return {
                    successful: false,
                    reason: `Invalid filter field: ${filter}`,
                    result: [],
                }
            }
            result.push(filter);
        }
        return {
            successful: true,
            reason: "",
            result: result,
        }
    }

    function parseUserInput(filters) {
        if (filters === "") return { successful: true, reason: "", result: [] };
        if (filters === filters.split(" ")) return parseFilters([filters]);
        return parseFilters(filters.split(" "));
    }

    function onInput(value) {
        const filterParsedResult = parseUserInput(value);
        if (!filterParsedResult.successful) {
            // todo: create and set some signals to show the error in the interface
            console.log("filterParsedResult: ", filterParsedResult.reason, filterParsedResult);
            return;
        }
        setModFilter(filterParsedResult.result);
    }

    function init() {
        let timeout;
        filterInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => onInput(event.target.value), 250);
        });

        return [modFilter, setModFilter];
    }

    return {
        init,
    }
}