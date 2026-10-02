import { createSignal, createEffect } from "../reactive.js";


const [selectedSourceId, setSelectedSourceId] = createSignal(undefined);

const setActiveSource = (element) => {
    const prevSelected = document.getElementById(selectedSourceId());
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
    const prevSelected = document.getElementById(selectedSourceId());
    if (prevSelected != undefined) {
        prevSelected.querySelector(".source-marker").classList.toggle("hidden");
    }
    setSelectedSourceId(undefined)
};

const [selectedGroupingId, setSelectedGroupingId] = createSignal(undefined);

const setActiveGrouping = (element) => {
    const prevSelected = document.getElementById(selectedGroupingId());
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
    const prevSelected = document.getElementById(selectedGroupingId());
    if (prevSelected != undefined) {
        prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
    }
    setSelectedGroupingId(undefined)
};

const getGroupingNameFromId = (id) => {
    return document.getElementById(id).querySelector(".name").innerHTML;
};

createEffect(() => {
    if (selectedSourceId() != undefined) {
        document.getElementById("active-source").innerHTML = getGroupingNameFromId(selectedSourceId());
    }
    else {
        document.getElementById("active-source").innerHTML = "(none)";
    }
});

createEffect(() => {
    if (selectedGroupingId() != undefined) {
        document.getElementById("active-grouping").innerHTML = getGroupingNameFromId(selectedGroupingId());
    }
    else {
        document.getElementById("active-grouping").innerHTML = "(none)";
    }
});

window.setActiveSource = setActiveSource;
window.clearActiveSource = clearActiveSource;
window.setActiveGrouping = setActiveGrouping;
window.clearActiveGrouping = clearActiveGrouping;