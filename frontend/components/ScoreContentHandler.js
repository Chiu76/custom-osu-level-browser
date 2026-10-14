import { scoreQuery } from "../api.js";

export function ScoreContentHandler() {
    function queryScores(request) {
        return scoreQuery(request);
    }

    return {
        queryScores,
    }
}