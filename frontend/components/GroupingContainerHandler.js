import { 
    selectedSources, setSelectedSources,
    selectedGroupings, setSelectedGroupings, 
} from "../app/settings.js";

export function GroupingContainerHandler() {
    function clearActiveSource() {
        const selectedElements = selectedSources().map((source) => document.getElementById(source));
        for (let element of selectedElements) {
            // element can be null when a different grouping type is selected, hence no element to remove hidden class
            if (element != null) {
                element.querySelector(".source-marker").classList.remove("hidden");
            }
        }
        setSelectedSources([]);
    }

    function clearActiveGrouping() {
        const selectedElements = selectedGroupings().map((source) => document.getElementById(source));
        console.log(selectedElements);
        for (let element of selectedElements) {
            // element can be null when a different grouping type is selected, hence no element to remove hidden class
            if (element != null) {
                element.querySelector(".grouping-marker").classList.remove("hidden");
            }
        }
        setSelectedGroupings([]);
    }

    window.clearActiveSource = clearActiveSource;
    window.clearActiveGrouping = clearActiveGrouping;

    function toggleActiveSource(event) {
        const row = event.target.closest(".row");
        const selected = selectedSources();
        if (selected.length == 0 || !selected.includes(row.id)) {
            selected.push(row.id);
            setSelectedSources(selected);
        }
        else {
            const idx = selected.indexOf(row.id);
            selected.splice(idx, 1);
            setSelectedSources(selected);
        }
    }

    function toggleActiveGrouping(event) {
        const row = event.target.closest(".row");
        const selected = selectedGroupings();
        if (selected.length == 0 || !selected.includes(row.id)) {
            selected.push(row.id);
            setSelectedGroupings(selected);
        }
        else {
            const idx = selected.indexOf(row.id);
            selected.splice(idx, 1);
            setSelectedGroupings(selected);
        }
    }

    function init() {
        const groupingListContainer = document.getElementById("grouping-list-container");
        groupingListContainer.addEventListener("click", (event) => toggleActiveGrouping(event));
        groupingListContainer.addEventListener("contextmenu", (event) => { event.preventDefault(); toggleActiveSource(event); });
        return groupingListContainer;
    }

    return {
        init,
    }
}