import { createElementClassContent, getGradeElement } from "../utils.js";
import { selectedBeatmapSetId, selectedBeatmapId, disableBeatmapSets } from "../app/settings.js";


function accuracy(beatmap) {
    if (beatmap.accuracy) return `${beatmap.accuracy}%`;
    else return "";
}

function starRating(beatmap) {
    let starRatingString = "";
    if (beatmap.star_rating) {
        starRatingString = starRatingString.concat(`${beatmap.star_rating}* `);
    }
    if (beatmap.star_rating_aim) {
        starRatingString = starRatingString.concat(`${beatmap.star_rating_aim}* `);
    } 
    if (beatmap.star_rating_speed) {
        starRatingString = starRatingString.concat(`${beatmap.star_rating_speed}* `);
    } 
    if (beatmap.star_rating_reading) {
        starRatingString = starRatingString.concat(`${beatmap.star_rating_reading}* `);
    }   
    return starRatingString;
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