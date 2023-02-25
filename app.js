function test() {
    // const text1 = document.getElementById("text1").value;


    // // Send the API requests
    // sendApiRequest("http://localhost:80/text1/", text1, "response1");
}

function submitText1() {
    // Get the input values
    const text1 = document.getElementById("text1").value;


    // Send the API requests
    sendApiRequest("http://localhost:80/text1/", text1, "response1");
}

function submitText2() {
    // Get the input values
    const text = document.getElementById("text2").value;

    // Send the API requests
    sendApiRequest("http://localhost:80/text2/", text, "response2");
}

function submitText3() {
    // Get the input values
    const text = document.getElementById("text3").value;

    // Send the API requests
    sendApiRequest("http://localhost:80/text3/", text, "response3");
}

async function sendApiRequest(url, text, responseId) {
    // Send the POST request to the API
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    // Get the response from the API
    let data = await response.json();
    data = data.response
    // Display the response under the input field
    const responseDiv = document.getElementById(responseId);
    responseDiv.innerHTML = data;
}
