import { createSignal, createEffect, createMemo } from "../reactive.js";

import { beatmapsQuery } from "../api.js";
import { RowBeatmapSet } from "./RowBeatmapSet.js";
import { RowBeatmap } from "./RowBeatmap.js";

import { q, filters, sortings } from "./Settings.js";


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

const [request, setRequest] = createSignal(buildRequest(q(), filters(), sortings()));

createEffect(() => {
    setRequest(buildRequest(q(), filters(), sortings()));
    console.log("setRequest(buildRequest(q(), filters(), sortings())): ", request());
});

var VirtualizedList = window.VirtualizedList.default;

createEffect(async () => {
    const beatmapsQueryResult = await beatmapsQuery(request());
    const beatmapsListContainer = document.getElementById("beatmaps-list-container");
    
    // to empty previous content
    beatmapsListContainer.replaceChildren();

    if (beatmapsQueryResult.length > 0) {
        const virtualizedList = new VirtualizedList(beatmapsListContainer, {
            height: 800,
            rowCount: beatmapsQueryResult.length - 1,
            renderRow: (index) => RowBeatmap(beatmapsQueryResult[index]),
            rowHeight: 100,
            overscanCount: 4,
        });
        virtualizedList.scrollToIndex(0, 'start');
    }
});