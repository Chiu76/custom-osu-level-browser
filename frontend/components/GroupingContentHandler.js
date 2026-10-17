import { groupingQuery } from "../api.js";
import { createSignal, createEffect } from "../reactive.js";

import { 
    selectedSourceId,
    selectedGroupingId,
    setGroupingSpec,
    setSourceSpec,
} from "../app/settings.js";

export function GroupingContentHandler() {
    const [selectedSourceType, setSelectedSourceType] = createSignal();
    const [selectedGroupingType, setSelectedGroupingType] = createSignal();

    createEffect(() => {
        if (selectedSourceId() != undefined) {
            const row = document.getElementById(selectedSourceId());
            document.getElementById("active-source").innerHTML = row.groupingName;
            setSelectedSourceType(row.groupingType);
            setSourceSpec({ type: row.groupingType, id: row.groupingId });
        }
        else {
            document.getElementById("active-source").innerHTML = "(none)";
            setSelectedSourceType("none");
            setSourceSpec({ type: "local_beatmaps" });
        }
    });

    createEffect(() => {
        if (selectedGroupingId() != undefined) {
            const row = document.getElementById(selectedGroupingId());
            document.getElementById("active-grouping").innerHTML = row.groupingName;
            setSelectedGroupingType(row.groupingType);
            setGroupingSpec({ type: selectedGroupingType(), id: row.groupingId });
        }
        else {
            document.getElementById("active-grouping").innerHTML = "(none)";
            setSelectedGroupingType("none");
            setGroupingSpec({ type: selectedGroupingType() });
        }
    });

    function queryGroupings(request) {
        return groupingQuery(request);
    }

    return {
        queryGroupings,
    }
}