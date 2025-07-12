async function testCSRFFetch(url, csrf_token) {
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "X-CSRF-TOKEN": csrf_token
        }
    });
    console.log(response)
}
