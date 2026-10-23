import { createSignal, createEffect } from "../reactive.js";
import { GroupingContainerHandler } from "../components/GroupingContainerHandler.js";
import { GroupingContentHandler } from "../components/GroupingContentHandler.js";
import { RowGrouping } from "../components/RowGrouping.js";

import {
    selectedSources, selectedGroupings,
    groupingSearch, 
    groupingType,
} from "../app/settings.js";

import * as beatmapQuery from "./beatmaps.js"

function buildRequest(beatmap_query_request, grouping_type, q) {
    return {
        beatmap_query_request: beatmap_query_request,
        grouping_type: grouping_type,
        q: q,
    }
}

const [request, setRequest] = createSignal();

createEffect(() => {
    const beatmap_query_request = beatmapQuery.request();
    beatmap_query_request.presentation_specs.grouping_specs = [{ type: "none" }];
    
    const grouping_type = groupingType();
    const q = groupingSearch();
    const newRequest = buildRequest(beatmap_query_request, grouping_type, q);
    console.log("groupings: newRequest:", newRequest);
    setRequest(newRequest);
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
