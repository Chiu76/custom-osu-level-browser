import { createElementClassContent, getGradeElement } from "../utils.js";
import { selectedBeatmapSetId, selectedBeatmapId, disableBeatmapSets } from "../app/settings.js";


function accuracy(beatmap) {
    if (beatmap.accuracy) return `${beatmap.accuracy}%`;
    else return "";
}

function starRating(beatmap) {
    if (beatmap.star_rating) return `${beatmap.star_rating}*`;
    else return "";
}

function RowBeatmap(beatmap) {
    const li = createElementClassContent("li", "row beatmap");
    li.id = beatmap.beatmap_id;
    
    li.appendChild(getGradeElement(beatmap.grade ?? ""));
    li.appendChild(createElementClassContent("div", "accuracy", accuracy(beatmap)));
    li.appendChild(createElementClassContent("div", "title", beatmap.title));
    li.appendChild(createElementClassContent("div", "artist", beatmap.artist));
    li.appendChild(createElementClassContent("div", "difficulty-name", `[${beatmap.difficulty_name}]`));
    li.appendChild(createElementClassContent("div", "star-rating", starRating(beatmap)));
    li.appendChild(createElementClassContent("div", "bpm", `${beatmap.bpm} BPM`));
    li.appendChild(createElementClassContent("div", "combo", beatmap.combo ?? ""));
    li.appendChild(createElementClassContent("div", "max-combo", beatmap.max_combo ?? ""));
    li.appendChild(createElementClassContent("div", "beatmap-id", beatmap.beatmap_id));
    li.appendChild(createElementClassContent("div", "mapper-id", beatmap.mapper_id ?? ""));
    li.appendChild(createElementClassContent("div", "mapper", beatmap.mapper ?? ""));

    li.appendChild(createElementClassContent("div", "beatmap-db-id", beatmap.beatmap_db_id, true));
    li.appendChild(createElementClassContent("div", "beatmap-set-id", beatmap.beatmap_set_id, true));

    if (beatmap.beatmap_set_id == selectedBeatmapSetId() && !disableBeatmapSets()) {
        li.classList.add("highlighted");        
    }

    if (beatmap.beatmap_id == selectedBeatmapId()) {
        li.classList.add("highlighted");
        li.classList.add("inner-outline-red");
    }
    
    return li;
}

export { RowBeatmap };