async function beatmapsQuery(request) {
    const res = await fetch("http://127.0.0.1:8000/api/beatmaps/query", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        },
        // body: JSON.stringify(request),
    });
    if (!res.ok) {
        throw Error("Failed to query beatmaps");
    }
    return res.json();
}

export { beatmapsQuery };