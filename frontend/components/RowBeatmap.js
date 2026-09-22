import { createElementClassContent } from "../utils.js";


function RowBeatmap(beatmap) {
    const li = createElementClassContent("li", "row-beatmap");
    li.appendChild(createElementClassContent("div", "grade", beatmap.grade ?? ""));
    li.appendChild(createElementClassContent("div", "accuracy", beatmap.accuracy ?? ""));
    li.appendChild(createElementClassContent("div", "title", beatmap.title));
    li.appendChild(createElementClassContent("div", "artist", beatmap.artist));
    li.appendChild(createElementClassContent("div", "difficulty-name", `[${beatmap.difficulty_name}]`));
    li.appendChild(createElementClassContent("div", "star-rating", beatmap.star_rating ?? ""));
    li.appendChild(createElementClassContent("div", "bpm", beatmap.bpm));
    li.appendChild(createElementClassContent("div", "combo", beatmap.combo ?? ""));
    li.appendChild(createElementClassContent("div", "max-combo", beatmap.max_combo ?? ""));
    li.appendChild(createElementClassContent("div", "beatmap-id", beatmap.beatmap_id));
    li.appendChild(createElementClassContent("div", "mapper-id", beatmap.mapper_id ?? ""));
    li.appendChild(createElementClassContent("div", "mapper", beatmap.mapper ?? ""));
    return li;
}

export { RowBeatmap };