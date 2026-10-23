import { groupingQuery } from "../api.js";
import { createSignal, createEffect } from "../reactive.js";

import { 
    selectedSources,
    selectedGroupings,
    setGroupingSpecs,
    setSourceSpecs,
} from "../app/settings.js";

export function GroupingContentHandler() {
    createEffect(() => {
        const selected = selectedSources();
        if (selected.length > 0) {
            const activeGroupings = selected.map((source) => document.getElementById(source).groupingName).join(", ");
            document.getElementById("active-sources").innerHTML = activeGroupings;
        }
        else {
            document.getElementById("active-sources").innerHTML = "(none)";
        }
    });

    createEffect(() => {
        const selected = selectedGroupings();
        if (selected.length > 0) {
            const activeGroupings = selected.map((grouping) => document.getElementById(grouping).groupingName).join(", ");
            document.getElementById("active-groupings").innerHTML = activeGroupings;
        }
        else {
            document.getElementById("active-groupings").innerHTML = "(none)";
        }
    });

    createEffect(() => {
        const selected = selectedSources();
        const sources = selected.map((source) => {
            const el = document.getElementById(source);
            return {
                type: el.groupingType,
                id: el.groupingId,
            }
        });
        
        if (sources.length > 0) {
            setSourceSpecs(sources);
        }
        else {
            setSourceSpecs([{ type: "local_beatmaps" }]);
        }
    });

    createEffect(() => {
        const selected = selectedGroupings();
        const groupings = selected.map((grouping) => {
            const el = document.getElementById(grouping);
            return {
                type: el.groupingType,
                id: el.groupingId,
            }
        });

        if (groupings.length > 0) {
            setGroupingSpecs(groupings);
        }
        else {
            setGroupingSpecs([{ type: "none" }]);
        }
    });

    function queryGroupings(request) {
        return groupingQuery(request);
    }

    return {
        queryGroupings,
    }
}