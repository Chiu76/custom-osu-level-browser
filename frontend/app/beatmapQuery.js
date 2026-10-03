import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapContentHandler } from "../components/BeatmapContentHandler.js";
import { BeatmapContainerHandler } from "../components/BeatmapContainerHandler.js";
import { search, filter, sort, selectedBeatmapSetId } from "./settings.js";

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
const [beatmapQueryRows, setBeatmapQueryRows] = createSignal([]);

createEffect(() => {
    setRequest(buildRequest(search(), filter(), sort()));
    console.log(request());
});

const beatmapContainerHandler = BeatmapContainerHandler();
const beatmapContainer = beatmapContainerHandler.init();

const beatmapContentHandler = BeatmapContentHandler();

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    beatmapContentHandler.queryBeatmaps(req)
        .then(rows => { if (id == latestId) setBeatmapQueryRows(rows)});
})

const displayRows = createMemo(() => {
    const beatmaps = beatmapQueryRows();
    const selectedSetId = selectedBeatmapSetId();
    return beatmapContentHandler.beatmapsToDisplayRows(beatmaps, selectedSetId);
})

var VirtualizedList = window.VirtualizedList.default;
let virtualizedList;
createEffect(() => {
    const rows = displayRows();
    if (rows.length == 0) return;
    
    // beatmapContainer.replaceChildren();
    if (virtualizedList) virtualizedList.destroy();

    virtualizedList = new VirtualizedList(beatmapContainer, {
        height: 672,
        rowCount: rows.length - 1 || 1,
        renderRow: (index) => beatmapContentHandler.displayRowToElement(rows, index),
        rowHeight: 96,
        overScan: 0,
    });
    virtualizedList.scrollToIndex(0, 'start');
});