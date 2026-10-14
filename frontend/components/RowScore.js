import { createElementClassContent } from "../utils.js";

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function RowScore(score) {
    const li = createElementClassContent("li", "row score");
    
    li.appendChild(createElementClassContent("div", "grade", score.grade));
    li.appendChild(createElementClassContent("div", "player-name", score.player_name));
    li.appendChild(createElementClassContent("div", "replay-score", `Score: ${numberWithCommas(score.replay_score)}`));
    li.appendChild(createElementClassContent("div", "pp", score.pp ?? ""));
    li.appendChild(createElementClassContent("div", "max-combo", ` (${score.max_combo}x)`));
    li.appendChild(createElementClassContent("div", "mods", score.mods));
    li.appendChild(createElementClassContent("div", "accuracy", `${score.accuracy}%`));
    li.appendChild(createElementClassContent("div", "played-at", score.played_at));
    
    return li;
}

export { RowScore };