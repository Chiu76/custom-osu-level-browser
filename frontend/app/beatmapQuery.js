import { createSignal, createEffect, createMemo } from "../reactive.js";

import { beatmapQuery } from "../api.js";
import { RowBeatmapSet } from "../components/RowBeatmapSet.js";
import { RowBeatmap } from "../components/RowBeatmap.js";

import { search, filter, sort } from "./settings.js";


function buildRequest(search, filters, sort) {
    // console.log("buildRequest: ", q, filters, sort);
    return {
        core_specs: {
            star_rating_spec: {},
            attached_score_spec: {},
            online_details_spec: {},
            source_spec: { type: "local_beatmaps" },
            filter_spec: { filters: filters },
        },
        presentation_specs: {
            search_spec: { q: search },
            grouping_spec: { type: "none"},
            sorting_spec: { sortings: sort },
        }
    }
}

const [request, setRequest] = createSignal(buildRequest(search(), filter(), sort()));

createEffect(() => {
    setRequest(buildRequest(search(), filter(), sort()));
    console.log("setRequest(buildRequest(search(), filter(), sort())): ", request());
});

var VirtualizedList = window.VirtualizedList.default;

createEffect(async () => {
    const beatmapQueryResult = await beatmapQuery(request());
    const beatmapListContainer = document.getElementById("beatmaps-list-container");
    
    // to empty previous content
    beatmapListContainer.replaceChildren();

    if (beatmapQueryResult.length > 0) {
        const virtualizedList = new VirtualizedList(beatmapListContainer, {
            height: 576,
            rowCount: beatmapQueryResult.length - 1,
            renderRow: (index) => RowBeatmap(beatmapQueryResult[index]),
            rowHeight: 96,
            overscanCount: 4,
        });
        virtualizedList.scrollToIndex(0, 'start');
    }
});