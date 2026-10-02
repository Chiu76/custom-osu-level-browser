import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapHandler } from "../components/BeatmapHandler.js";
import { search, filter, sort } from "./settings.js";

function buildRequest(search, filters, sort) {
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
    console.log(request());
});

const beatmapHandler = BeatmapHandler();

const beatmapListContainer = document.getElementById("beatmaps-list-container");
beatmapListContainer.addEventListener("click", (event) => beatmapHandler.onClickBeatmapRow(event));

var VirtualizedList = window.VirtualizedList.default;

createEffect(async () => {
    const displayRows = await beatmapHandler.getDisplayRows(request());
    beatmapListContainer.replaceChildren();
    if (displayRows.length > 0) {
        const virtualizedList = new VirtualizedList(beatmapListContainer, {
            height: 672,
            rowCount: displayRows.length - 1 || 1,
            renderRow: (index) => beatmapHandler.displayRowToElement(displayRows, index),
            rowHeight: 96,
            overScan: 0,
        });
        virtualizedList.scrollToIndex(0, 'start');
    }
});
 