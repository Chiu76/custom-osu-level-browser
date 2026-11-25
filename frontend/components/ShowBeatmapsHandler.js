import { schemas } from "../utils.js";
import { RadioHandler } from "./RadioHandler.js";

export function ShowBeatmapsHandler() {    
    const showBeatmapsValues = schemas["AttachedScoreSpec"]["properties"]["show_beatmaps"]["enum"];

    function init() {
        return RadioHandler("show-beatmaps").init(showBeatmapsValues, "show-beatmaps");
    }

    return {
        init,
    };
}