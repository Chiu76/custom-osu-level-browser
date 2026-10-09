async function openapiSchemas() {
    return (
        fetch(`http://127.0.0.1:8000/openapi.json`, {
            method: "GET",
            headers: {
                "Content-type": "application/json",
            },
        })
        .then((response) => response.json())
        .then((json) => json["components"]["schemas"])
    );  
}

async function beatmapQuery(request) {
    // console.log("api: beatmapQuery: request:", request);
    const res = await fetch(`http://127.0.0.1:8000/api/beatmap_query`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(request),
    });
    if (!res.ok) {
        throw Error("Failed to query beatmaps");
    }
    return res.json();
}

async function groupingQuery(request) {
    // console.log("api: groupingQuery: request:", request);
    const res = await fetch(`http://127.0.0.1:8000/api/grouping_query`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(request),
    });
    if (!res.ok) {
        throw Error("Failed to query groupings");
    }
    return res.json();
}

export { openapiSchemas, beatmapQuery, groupingQuery };