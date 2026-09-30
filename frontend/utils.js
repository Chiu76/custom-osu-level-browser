import { openapiSchemas } from "./api.js";


function createElementClassContent(type, className, content="") {
    const element = document.createElement(type);
    element.className = className;
    element.innerHTML = content;
    return element;
}

const schemas = await openapiSchemas();

const filterFieldValues = schemas["Filter"]["properties"]["field"]["enum"];
const filterFieldValuesRegex = new RegExp(filterFieldValues.join("|"), "g")

const filterOpValues = schemas["Filter"]["properties"]["op"]["enum"];
const filterOpValuesRegex = new RegExp(filterOpValues.join("|"), "g")


function assertOp(filter) {
    return (filter.match(filterOpValuesRegex) ?? []).length === 1;
}

function assertField(filter) {
    let field = filter.split(filterOpValuesRegex)[0];
    return filterFieldValues.includes(field);
}

function parseSplitFilters(filters) {
    const result = [];
    for (let filter of filters) {
        if (!assertField(filter)) {
            return {
                successful: false,
                reason: `Invalid filter field: ${filter.split(filterOpValuesRegex)[0]}`,
                result: [],
            }
        }
        if (!assertOp(filter)) {
            return {
                successful: false,
                reason: "Invalid filter operator, or there is not exactly one operator in the filter.",
                result: [],
            }
        }
        const op = filter.match(filterOpValuesRegex)[0];
        const tokens = filter.split(op);
        result.push({
            field: tokens[0],
            op: op,
            value: tokens[1],
        })
    }
    return {
        successful: true,
        reason: "",
        result: result,
    }
}

function parseFilterUserInput(filters) {
    if (filters === "") return [];
    if (filters === filters.split(" ")) return parseSplitFilters([filters]);
    return parseSplitFilters(filters.split(" "));
}

function buildRequest(q, filters, sortings) {
    // console.log("buildRequest: ", q, filters, sortings);
    return {
        core_specs: {
            star_rating_spec: {},
            attached_score_spec: {},
            online_details_spec: {},
            source_spec: { type: "local_beatmaps" },
            filter_spec: { filters },
        },
        presentation_specs: {
            search_spec: { q },
            grouping_spec: { type: "none"},
            sorting_spec: { },
        }
    }
}

export { createElementClassContent, buildRequest, parseFilterUserInput };