import { createSignal, createEffect, createMemo } from "./reactive.js";

import { beatmapsQuery } from "./api.js";
import { RowBeatmapSet } from "./components/RowBeatmapSet.js";
import { RowBeatmap } from "./components/RowBeatmap.js";


async function updateRequest() {
    setRequest(request() + 1);
}
window.updateRequest = updateRequest;

const [request, setRequest] = createSignal(0);

createEffect(async () => {
    const beatmapsQueryResult = await beatmapsQuery(request());
    const beatmapsListContainer = document.getElementById("beatmaps-list-container");
    beatmapsListContainer.replaceChildren(...beatmapsQueryResult.map((result) => RowBeatmap(result)));
});
