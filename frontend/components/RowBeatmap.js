import { createElementClassContent } from "../utils.js";
import { selectedBeatmapSetId, selectedBeatmapId } from "../app/settings.js";

function RowBeatmap(beatmap) {
    const li = createElementClassContent("li", "row beatmap");
    
    li.appendChild(createElementClassContent("div", "grade", beatmap.grade ?? ""));
    li.appendChild(createElementClassContent("div", "accuracy", beatmap.accuracy ?? ""));
    li.appendChild(createElementClassContent("div", "title", beatmap.title));
    li.appendChild(createElementClassContent("div", "artist", beatmap.artist));
    li.appendChild(createElementClassContent("div", "difficulty-name", `[${beatmap.difficulty_name}]`));
    li.appendChild(createElementClassContent("div", "star-rating", beatmap.star_rating ?? ""));
    li.appendChild(createElementClassContent("div", "bpm", `${beatmap.bpm} BPM`));
    li.appendChild(createElementClassContent("div", "combo", beatmap.combo ?? ""));
    li.appendChild(createElementClassContent("div", "max-combo", beatmap.max_combo ?? ""));
    li.appendChild(createElementClassContent("div", "beatmap-id", beatmap.beatmap_id));
    li.appendChild(createElementClassContent("div", "mapper-id", beatmap.mapper_id ?? ""));
    li.appendChild(createElementClassContent("div", "mapper", beatmap.mapper ?? ""));

    li.appendChild(createElementClassContent("div", "beatmap-set-id", beatmap.beatmap_set_id, true));

    if (beatmap.beatmap_set_id == selectedBeatmapSetId()) {
        li.classList.add("highlighted");        
    }

    if (beatmap.beatmap_id == selectedBeatmapId()) {
        li.classList.add("highlighted");
        li.classList.add("inner-outline-red");
    }
    
    return li;
}

export { RowBeatmap };