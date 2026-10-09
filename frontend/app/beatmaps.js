import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapContentHandler } from "../components/BeatmapContentHandler.js";
import { BeatmapContainerHandler } from "../components/BeatmapContainerHandler.js";
import { 
    search, filter, sort, 
    selectedBeatmapId, selectedBeatmapSetId,
    selectedGroupingId, selectedSourceId,
    groupingType,
    sourceSpec, groupingSpec,
} from "./settings.js";

function buildRequest(searchSpec, filterSpec, sortSpec, sourceSpec, groupingSpec) {
    return {
        core_specs: {
            star_rating_spec: {},
            attached_score_spec: {},
            online_details_spec: {},
            source_spec: sourceSpec,
            filter_spec: filterSpec,
        },
        presentation_specs: {
            search_spec: searchSpec,
            grouping_spec: groupingSpec,
            sorting_spec: sortSpec,
        }
    }
}

const [request, setRequest] = createSignal();
const [beatmapQueryRows, setBeatmapQueryRows] = createSignal([]);

createEffect(() => {
    const searchSpec = { q: search() };
    const filterSpec = { filters: filter() };
    const sortSpec = { sortings: sort() };
    // const groupingSpec = { type: groupingType(), id: selectedGroupingId() };
    const source_spec = sourceSpec();
    const grouping_spec = groupingSpec();
    const req = buildRequest(searchSpec, filterSpec, sortSpec, source_spec, grouping_spec);
    console.log("beatmaps: request-building effect: req:", req);
    setRequest(req);
});

const beatmapContainerHandler = BeatmapContainerHandler();
const beatmapContainer = beatmapContainerHandler.init();

const beatmapContentHandler = BeatmapContentHandler();

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    beatmapContentHandler.queryBeatmaps(req)
        .then(response => { 
            if (id !== latestId) return;
            setBeatmapQueryRows(response.rows);
            virtualizedList?.scrollToIndex(0, "start");
        });
})

const displayRows = createMemo(() => {
    const beatmaps = beatmapQueryRows();
    const currentSelectBeatmapId = selectedBeatmapId();
    const currentSelectedBeatmapSetId = selectedBeatmapSetId();
    // const currentSelectedGroupingId = selectedGroupingId();
    // const currentSelectedSourceId = selectedSourceId();
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

export { request };