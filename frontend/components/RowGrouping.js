import { createElementClassContent } from "../utils.js";
import { selectedGroupings, selectedSources } from "../app/settings.js";

function RowGrouping(grouping) {
    const li = createElementClassContent("li", "row grouping");

    li.id = `grouping-${grouping.grouping_type}-${grouping.grouping_id}`;
    li.groupingType = grouping.grouping_type;
    li.groupingId = grouping.grouping_id;
    li.groupingName = grouping.grouping_name;
    
    li.appendChild(createElementClassContent("div", "grouping-marker hidden", "Grouping"));
    li.appendChild(createElementClassContent("div", "source-marker hidden", "Source"));
    li.appendChild(createElementClassContent("div", "name", grouping.grouping_name));
    li.appendChild(createElementClassContent("div", "count", `${grouping.selected_count} (${grouping.total_count})`));
    
    if (selectedGroupings().includes(li.id)) {
        li.getElementsByClassName("grouping-marker")[0].classList.toggle("hidden");
    }

    if (selectedSources().includes(li.id)) {
        li.getElementsByClassName("source-marker")[0].classList.toggle("hidden");
    }
    
    return li;
}

export { RowGrouping };