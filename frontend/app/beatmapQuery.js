import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapContentHandler } from "../components/BeatmapContentHandler.js";
import { BeatmapContainerHandler } from "../components/BeatmapContainerHandler.js";
import { search, filter, sort, selectedBeatmapId, selectedBeatmapSetId } from "./settings.js";

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
            grouping_spec: { type: "none" },
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
        .then(rows => { 
            if (id !== latestId) return;
            setBeatmapQueryRows(rows);
            virtualizedList?.scrollToIndex(0, "start");
        });
})

const displayRows = createMemo(() => {
    const beatmaps = beatmapQueryRows();
    const currentSelectBeatmapId = selectedBeatmapId();
    const currentSelectedBeatmapSetId = selectedBeatmapSetId();
    return beatmapContentHandler.beatmapsToDisplayRows(beatmaps, currentSelectedBeatmapSetId);
})

var VirtualizedList = window.VirtualizedList.default;
let virtualizedList = null;
createEffect(() => {
    const rows = displayRows();
    if (rows.length === 0) {
        virtualizedList?.destroy();
        virtualizedList = null;
        return;
    }
    if (!virtualizedList) {
        virtualizedList = new VirtualizedList(beatmapContainer, {
            height: 672, rowHeight: 96, rowCount: rows.length,
            renderRow: (index) => beatmapContentHandler.displayRowToElement(displayRows(), index),
        });
    }
    else {
        virtualizedList.setRowCount(rows.length);
    }
});