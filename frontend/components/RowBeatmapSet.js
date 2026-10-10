import { createElementClassContent } from "../utils.js";
import { selectedBeatmapSetId } from "../app/settings.js";

function RowBeatmapSet(beatmaps) {
    // first beatmap in set used to access set-related values
    const beatmapSet = beatmaps[0];
    
    const li = createElementClassContent("li", "row beatmap-set");
    
    li.appendChild(createElementClassContent("div", "set-marker", "Set"));
    li.appendChild(createElementClassContent("div", "title", beatmapSet.title));
    li.appendChild(createElementClassContent("div", "artist", beatmapSet.artist));
    li.appendChild(createElementClassContent("div", "bpm", `${beatmapSet.bpm} BPM`));
    li.appendChild(createElementClassContent("div", "beatmap-set-id", beatmapSet.beatmap_set_id));
    li.appendChild(createElementClassContent("div", "owner-id", beatmapSet.owner_id ?? ""));
    li.appendChild(createElementClassContent("div", "owner", beatmapSet.owner));
    
    if (beatmapSet.beatmap_set_id == selectedBeatmapSetId()) {
        li.classList.add("highlighted");
        li.classList.add("inner-outline-brown");
    }

    return li;
}

export { RowBeatmapSet };