import { createSignal, createEffect, createMemo } from "./reactive.js";

import { beatmapsQuery } from "./api.js";
import { RowBeatmapSet } from "./components/RowBeatmapSet.js";
import { RowBeatmap } from "./components/RowBeatmap.js";


async function updateRequest() {
    setRequest(request + 1);
}
window.updateRequest = updateRequest;

const [request, setRequest] = createSignal(0);

const [s, set] = createSignal();
createEffect(async () => set(async () => {
    console.log("About to call beatmapsQuery()..");
    return await beatmapsQuery(request());
}));
const beatmapsQueryResult = s();

createEffect(() => {
    const beatmapsListContainer = document.getElementById("beatmaps-list-container");
    console.log("aqui", typeof beatmapsQueryResult(), beatmapsQueryResult());
    if (beatmapsQueryResult()[Symbol.iterator] === 'function') {
        for (let result of beatmapsQueryResult()) {
            beatmapsListContainer.appendChild(RowBeatmap(result));
        }
    }
});
