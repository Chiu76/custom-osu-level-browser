import { createSignal, createEffect, createMemo } from "../reactive.js";
import { GroupingContainerHandler } from "../components/GroupingContainerHandler.js";
import { GroupingContentHandler } from "../components/GroupingContentHandler.js";
import { RowGrouping } from "../components/RowGrouping.js";

import {
    selectedSources, selectedGroupings,
    groupingSearch, 
    groupingType,
    showSelectedCounts,
} from "../app/settings.js";

import * as beatmapQuery from "./beatmaps.js"

function buildRequest(beatmap_query_request, grouping_type, q, show_selected_counts) {
    return {
        beatmap_query_request: beatmap_query_request,
        grouping_type: grouping_type,
        q: q,
        show_selected_counts: show_selected_counts,
    }
}

const [request, setRequest] = createSignal();
let prevRequest = {};

createEffect(() => {
    const beatmap_query_request = structuredClone(beatmapQuery.request());
    beatmap_query_request.presentation_specs.grouping_specs = [{ type: "none" }];
    const grouping_type = groupingType();
    const q = groupingSearch();
    const show_selected_counts = showSelectedCounts();
    
    const newRequest = buildRequest(beatmap_query_request, grouping_type, q, show_selected_counts);
    
    if (JSON.stringify(prevRequest) !== JSON.stringify(newRequest)) {
        console.log("groupings: newRequest:", newRequest);
        prevRequest = structuredClone(newRequest);
        setRequest(newRequest);
    }
});

const groupingContentHandler = GroupingContentHandler();
const [groupingQueryRows, setGroupingQueryRows] = createSignal([]);

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    groupingContentHandler.queryGroupings(req)
        .then(response => { 
            if (id === latestId) setGroupingQueryRows(response.rows);
        });
});

const groupingContainerHandler = GroupingContainerHandler();
const groupingContainer = groupingContainerHandler.init();

createEffect(() => {
    selectedSources();
    selectedGroupings();
    const rows = groupingQueryRows();
    groupingContainer.replaceChildren();
    if (rows.length > 0) {
        for (let row of rows) {
            groupingContainer.appendChild(RowGrouping(row))
        }
    }
});
