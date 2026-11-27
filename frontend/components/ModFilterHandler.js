import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";

export function ModFilterHandler() {
    const [modsExactFilter, setModsExactFilter] = createSignal([]);
    const [modsIncludeFilter, setModsIncludeFilter] = createSignal([]);
    const [modsExcludeFilter, setModsExcludeFilter] = createSignal([]);

    const filterParent = document.getElementById("attached-score-mod-filter");
    const filterInput = filterParent.getElementsByTagName("input")[0];

    const modValuesDefault = schemas["ScoreSqSpec"]["properties"]["mods_exact"]["items"]["anyOf"][0]["enum"];
    const modValuesAlts = schemas["ScoreSqSpec"]["properties"]["mods_exact"]["items"]["anyOf"][1]["enum"];
    const modValues = modValuesDefault.concat(modValuesAlts);

    function assertMod(mod) {
        return modValues.includes(mod);
    }

    function parseFilters(filters) {
        // assumes input is an array of filter strings, optionally with a +/- before them, such as:
        // ["hd", "dOuBlEtImE", "-Ht", "+ez"]
        const resultExact = [];
        const resultInclude = [];
        const resultExclude = [];

        for (let filter of filters) {
            let modifier;
            filter = filter.toLowerCase();

            if (filter.startsWith("+") || filter.startsWith("-")) {
                modifier = filter.substr(0, 1);
                filter = filter.slice(1);
                console.log(modifier, filter);
            }

            if (!assertMod(filter)) {
                return {
                    successful: false,
                    reason: `Invalid filter field: ${filter}`,
                    resultExact: [],
                    resultInclude: [],
                    resultExcude: [],
                }
            }

            if (modifier === undefined) {
                resultExact.push(filter)
            }
            else if (modifier === "+") {
                resultInclude.push(filter);
            }
            else if (modifier === "-") {
                resultExclude.push(filter);
            }
        }
        return {
            successful: true,
            reason: "",
            resultExact: resultExact,
            resultInclude: resultInclude,
            resultExclude: resultExclude,
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
        setModsExactFilter(filterParsedResult.resultExact);
        setModsIncludeFilter(filterParsedResult.resultInclude);
        setModsExcludeFilter(filterParsedResult.resultExclude);
    }

    function init() {
        let timeout;
        filterInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => onInput(event.target.value), 250);
        });

        return [modsExactFilter, modsIncludeFilter, modsExcludeFilter];
    }

    return {
        init,
    }
}