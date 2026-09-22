import { createSignal, createEffect, createMemo } from "./reactive.js";


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
    // todo: this eventlistener should be either active by default, or somehow triggered before the right click
    // first right click will still have a context menu, only subsequent ones are blocked
    // console.log(element)
    // console.log(typeof element)
    // document.getElementById(element.id).addEventListener('contextmenu', (event) => { event.preventDefault(); console.log("pulog"); });
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

export { getSelectedSourceId, getSelectedGroupingId };