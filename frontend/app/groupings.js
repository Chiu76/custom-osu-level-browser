import { createSignal, createEffect } from "../reactive.js";
import { GroupingContainerHandler } from "../components/GroupingContainerHandler.js";
import { GroupingContentHandler } from "../components/GroupingContentHandler.js";

import { 
    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId, 
} from "../app/settings.js";

import * as beatmapQuery from "./beatmaps.js"

const groupingContainerHandler = GroupingContainerHandler();
const groupingContainer = groupingContainerHandler.init();

const groupingContentHandler = GroupingContentHandler();
// groupingContentHandler.queryGroupings();

console.log("Hi group groupings.js: beatmapQuery.request():", beatmapQuery.request());

createEffect(() => {
    if (selectedSourceId() != undefined) {
        document.getElementById("active-source").innerHTML = groupingContainerHandler.getGroupingNameFromId(selectedSourceId());
    }
    else {
        document.getElementById("active-source").innerHTML = "(none)";
    }
});

createEffect(() => {
    if (selectedGroupingId() != undefined) {
        document.getElementById("active-grouping").innerHTML = groupingContainerHandler.getGroupingNameFromId(selectedGroupingId());
    }
    else {
        document.getElementById("active-grouping").innerHTML = "(none)";
    }
});

window.setActiveSource = groupingContainerHandler.setActiveSource;
window.clearActiveSource = groupingContainerHandler.clearActiveSource;
window.setActiveGrouping = groupingContainerHandler.setActiveGrouping;
window.clearActiveGrouping = groupingContainerHandler.clearActiveGrouping;