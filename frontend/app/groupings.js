import { createSignal, createEffect, createMemo } from "../reactive.js";
import { GroupingContainerHandler } from "../components/GroupingContainerHandler.js";
import { GroupingContentHandler } from "../components/GroupingContentHandler.js";
import { RowGrouping } from "../components/RowGrouping.js";

import { 
    selectedSourceId, selectedGroupingId,
    groupingSearch, 
    groupingType, setGroupingType,
    groupingSpec, setGroupingSpec,
} from "../app/settings.js";

import * as beatmapQuery from "./beatmaps.js"

function buildRequest(beatmapQueryRequest, groupType, q) {
    return {
        beatmap_query_request: beatmapQueryRequest,
        grouping_type: groupType,
        q: q,
    }
}

const [request, setRequest] = createSignal();
const [groupingQueryRows, setGroupingQueryRows] = createSignal([]);

createEffect(() => {
    const beatmapQueryRequest = beatmapQuery.request();
    const groupType = groupingType();
    const q = groupingSearch();
    const req = buildRequest(beatmapQueryRequest, groupType, q);
    console.log("groupings: request-building effect: req:", req);
    setRequest(req);
});

const groupingContainerHandler = GroupingContainerHandler();
const groupingContainer = groupingContainerHandler.init();

const groupingContentHandler = GroupingContentHandler();

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    groupingContentHandler.queryGroupings(req)
        .then(response => { 
            if (id === latestId) setGroupingQueryRows(response.rows);
        });
});

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
    }
    else {
        document.getElementById("active-source").innerHTML = "(none)";
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

createEffect(() => {
    // if there is a selected grouping, set also the signal of grouping_spec!! otherwise unselect
});

window.clearActiveSource = groupingContainerHandler.clearActiveSource;
window.clearActiveGrouping = groupingContainerHandler.clearActiveGrouping;