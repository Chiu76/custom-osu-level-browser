import { createElementClassContent } from "../utils.js";


function RowBeatmapSet(beatmapSet) {
    const li = createElementClassContent("li", "row-beatmap-set");
    li.appendChild(createElementClassContent("div", "set-marker", "Set"));
    li.appendChild(createElementClassContent("div", "title", beatmapSet.title));
    li.appendChild(createElementClassContent("div", "artist", beatmapSet.artist));
    li.appendChild(createElementClassContent("div", "bpm", beatmapSet.bpm));
    li.appendChild(createElementClassContent("div", "beatmap-set-id", beatmapSet.beatmap_set_id));
    li.appendChild(createElementClassContent("div", "owner-id", beatmapSet.owner_id ?? ""));
    li.appendChild(createElementClassContent("div", "owner", beatmapSet.owner));
    return li;
}

export { RowBeatmapSet };