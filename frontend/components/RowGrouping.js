import { createElementClassContent } from "../utils.js";
import { selectedGroupingId, selectedSourceId } from "../app/settings.js";

function RowGrouping(grouping) {
    const li = createElementClassContent("li", "row grouping");
    li.id = grouping.id;
    li.name = grouping.name;
    
    li.appendChild(createElementClassContent("div", "grouping-marker hidden", "Grouping"));
    li.appendChild(createElementClassContent("div", "source-marker hidden", "Source"));
    li.appendChild(createElementClassContent("div", "name", grouping.name));
    li.appendChild(createElementClassContent("div", "count", `${grouping.selected_count} (${grouping.total_count})`));

    if (grouping.id == selectedGroupingId()) {
        li.getElementsByClassName("grouping-marker")[0].classList.toggle("hidden");
    }

    if (grouping.id == selectedSourceId()) {
        li.getElementsByClassName("source-marker")[0].classList.toggle("hidden");
    }
    
    return li;
}

export { RowGrouping };