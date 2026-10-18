import { createElementClassContent, posixTimestampFormatter, getGradeElement, getModsElement } from "../utils.js";

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function RowScore(score) {
    const li = createElementClassContent("li", "row score");
    
    li.appendChild(getGradeElement(score.grade));
    li.appendChild(createElementClassContent("div", "player-name", score.player_name));
    li.appendChild(createElementClassContent("div", "replay-score", `Score: ${numberWithCommas(score.replay_score)}`));
    li.appendChild(getModsElement(score.mods));
    li.appendChild(createElementClassContent("div", "pp", score.pp ?? ""));
    li.appendChild(createElementClassContent("div", "max-combo", ` (${score.max_combo}x)`));
    li.appendChild(createElementClassContent("div", "played-at", posixTimestampFormatter(score.played_at)));
    li.appendChild(createElementClassContent("div", "accuracy", `${score.accuracy}%`));
    
    return li;
}

export { RowScore };