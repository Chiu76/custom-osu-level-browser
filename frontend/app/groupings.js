import { createSignal, createEffect, createMemo } from "../reactive.js";
import { GroupingContainerHandler } from "../components/GroupingContainerHandler.js";
import { GroupingContentHandler } from "../components/GroupingContentHandler.js";
import { RowGrouping } from "../components/RowGrouping.js";

import { 
    selectedSourceId, selectedGroupingId,
    groupingSearch, 
    groupingType, setGroupingType,
    groupingSpec, setGroupingSpec,
    sourceSpec, setSourceSpec,
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
    selectedSourceId();
    selectedGroupingId();
    const rows = groupingQueryRows();
    groupingContainer.replaceChildren();
    if (rows.length > 0) {
        for (let row of rows) {
            groupingContainer.appendChild(RowGrouping(row))
        }
    }
});

createEffect(() => {
    if (selectedSourceId() != undefined) {
        // todo: find a nicer way to do this, because having the grouping id (which is just an int) be the html element id seems very wrong
        const groupingName = document.getElementById(selectedSourceId()).name;
        document.getElementById("active-source").innerHTML = groupingName;
        setSourceSpec({ type: "collections", id: selectedSourceId() });
    }
    else {
        document.getElementById("active-source").innerHTML = "(none)";
        setSourceSpec({ type: "local_beatmaps" });
    }
});

createEffect(() => {
    if (selectedGroupingId() != undefined) {
        // todo: find a nicer way to do this, because having the grouping id (which is just an int) be the html element id seems very wrong
        const groupingName = document.getElementById(selectedGroupingId()).name;
        document.getElementById("active-grouping").innerHTML = groupingName;
        // setGroupingType("collections")
        setGroupingSpec({ type: "collections", id: selectedGroupingId() });
    }
    else {
        document.getElementById("active-grouping").innerHTML = "(none)";
        // setGroupingType("none")
        setGroupingSpec({ type: "none" });
    }
});

window.clearActiveSource = groupingContainerHandler.clearActiveSource;
window.clearActiveGrouping = groupingContainerHandler.clearActiveGrouping;