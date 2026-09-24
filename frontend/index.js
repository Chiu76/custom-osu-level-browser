import { createSignal, createEffect, createMemo } from "./reactive.js";

import { beatmapsQuery } from "./api.js";
import { RowBeatmapSet } from "./components/RowBeatmapSet.js";
import { RowBeatmap } from "./components/RowBeatmap.js";


let selectedScoreId = undefined;

const scoreOnClick = (element) => {
    const prevSelected = document.getElementById(selectedScoreId);
    if (prevSelected == undefined) {
        element.classList.toggle("highlighted");
        selectedScoreId = element.id;
    }
    else {
        if (prevSelected.id != element.id) {
            prevSelected.classList.toggle("highlighted")
            selectedScoreId = element.id;
        }
        else {
            selectedScoreId = undefined;
        }
        element.classList.toggle("highlighted");
    }
};


const [getSelectedSourceId, setSelectedSourceId] = createSignal(undefined);

const setActiveSource = (element) => {
    const prevSelected = document.getElementById(getSelectedSourceId());
    if (prevSelected == undefined) {
        element.querySelector(".source-marker").classList.toggle("hidden");
        setSelectedSourceId(element.id);
    }
    else {
        if (prevSelected.id != element.id) {
            prevSelected.querySelector(".source-marker").classList.toggle("hidden");
            setSelectedSourceId(element.id);
        }
        else {
            setSelectedSourceId(undefined);
        }
        element.querySelector(".source-marker").classList.toggle("hidden");
    }
};

const clearActiveSource = () => {
    const prevSelected = document.getElementById(getSelectedSourceId());
    if (prevSelected != undefined) {
        prevSelected.querySelector(".source-marker").classList.toggle("hidden");
    }
    setSelectedSourceId(undefined)
};


const [getSelectedGroupingId, setSelectedGroupingId] = createSignal(undefined);

const setActiveGrouping = (element) => {
    const prevSelected = document.getElementById(getSelectedGroupingId());
    if (prevSelected == undefined) {
        element.querySelector(".grouping-marker").classList.toggle("hidden");
        setSelectedGroupingId(element.id);
    }
    else {
        if (prevSelected.id != element.id) {
            prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
            setSelectedGroupingId(element.id);
        }
        else {
            setSelectedGroupingId(undefined);
        }
        element.querySelector(".grouping-marker").classList.toggle("hidden");
    }
};

const clearActiveGrouping = () => {
    const prevSelected = document.getElementById(getSelectedGroupingId());
    if (prevSelected != undefined) {
        prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
    }
    setSelectedGroupingId(undefined)
};

window.scoreOnClick = scoreOnClick;
window.setActiveSource = setActiveSource;
window.clearActiveSource = clearActiveSource;
window.setActiveGrouping = setActiveGrouping;
window.clearActiveGrouping = clearActiveGrouping;


const getGroupingNameFromId = (id) => {
    return document.getElementById(id).querySelector(".name").innerHTML;
};

createEffect(() => {
    if (getSelectedSourceId() != undefined) {
        document.getElementById("active-source").innerHTML = getGroupingNameFromId(getSelectedSourceId());
    }
    else {
        document.getElementById("active-source").innerHTML = "(none)";
    }
});

createEffect(() => {
    if (getSelectedGroupingId() != undefined) {
        document.getElementById("active-grouping").innerHTML = getGroupingNameFromId(getSelectedGroupingId());
    }
    else {
        document.getElementById("active-grouping").innerHTML = "(none)";
    }
});


async function updateRequest() {
    setRequest(request() + 1);
}
window.updateRequest = updateRequest;

const [request, setRequest] = createSignal(0);

var VirtualizedList = window.VirtualizedList.default;

createEffect(async () => {
    const beatmapsQueryResult = await beatmapsQuery(request());
    const beatmapsListContainer = document.getElementById("beatmaps-list-container");
    
    // to empty previous content
    beatmapsListContainer.replaceChildren();

    const virtualizedList = new VirtualizedList(beatmapsListContainer, {
        height: 800,
        rowCount: beatmapsQueryResult.length,
        renderRow: (index) => RowBeatmap(beatmapsQueryResult[index]),
        rowHeight: 100,
        overscanCount: 4,
    });

    virtualizedList.scrollToIndex(0, 'start');
});


export { getSelectedSourceId, getSelectedGroupingId };