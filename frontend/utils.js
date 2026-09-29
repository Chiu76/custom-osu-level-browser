function createElementClassContent(type, className, content="") {
    const element = document.createElement(type);
    element.className = className;
    element.innerHTML = content;
    return element;
}

function buildRequest(q, filters, sortings) {
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
            sorting_spec: { sortings },
        }
    }
}

export { createElementClassContent, buildRequest };