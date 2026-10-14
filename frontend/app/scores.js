import { createSignal, createEffect } from "../reactive.js";
import { ScoreContainerHandler } from "../components/ScoreContainerHandler.js";
import { ScoreContentHandler } from "../components/ScoreContentHandler.js";
import { RowScore } from "../components/RowScore.js";

import { 
    scoreTopBy,
    modsExactFilter,	
    modsIncludeFilter,
    modsExcludeFilter,
    selectedBeatmapId,
} from "../app/settings.js";

function buildRequest(top_by, mods_exact, mods_include, mods_exclude, beatmap_db_id) {
    return {
        score_sq_spec: {
            top_by: top_by,
            top_score_only: false,
            mods_exact: mods_exact,
            mods_include: mods_include,
            mods_exclude: mods_exclude,
        },
        beatmap_db_id: beatmap_db_id,
    }
}

function getBeatmapDbId(beatmapId) {
    if (!beatmapId) return;
    const beatmapRow = document.getElementById(beatmapId)
    return beatmapRow.getElementsByClassName("beatmap-db-id")[0].innerText;
}

const [request, setRequest] = createSignal();

createEffect(() => {
    const top_by = scoreTopBy();
    const mods_exact = modsExactFilter();
    const mods_include = modsIncludeFilter();
    const mods_exclude = modsExcludeFilter();
    const beatmap_db_id = getBeatmapDbId(selectedBeatmapId());
    const newRequest = buildRequest(top_by, mods_exact, mods_include, mods_exclude, beatmap_db_id);
    console.log("groupings: newRequest:", newRequest);
    setRequest(newRequest);
});

const scoreContentHandler = ScoreContentHandler();
const [scoreQueryRows, setScoreQueryRows] = createSignal([]);

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    if (selectedBeatmapId()) {
        scoreContentHandler.queryScores(req)
            .then(response => { 
                if (id === latestId) setScoreQueryRows(response.rows);
            });
    }
});

const scoreContainerHandler = ScoreContainerHandler();
const scoreContainer = scoreContainerHandler.init();

createEffect(() => {
    const rows = scoreQueryRows();
    scoreContainer.replaceChildren();
    if (rows.length > 0) {
        for (let row of rows) {
            scoreContainer.appendChild(RowScore(row))
        }
    }
});

let selectedScoreId = undefined;

const scoreOnClick = (element) => {
    const prevSelected = document.getElementById(selectedScoreId);
    if (prevSelected == undefined) {
        element.classList.toggle("highlighted");
        selectedScoreId = element.id;
    }
    else {
        if (prevSelected.id != element.id) {
            prevSelected.classList.toggle("highlighted")
            selectedScoreId = element.id;
        }
        else {
            selectedScoreId = undefined;
        }
        element.classList.toggle("highlighted");
    }
};

window.scoreOnClick = scoreOnClick;