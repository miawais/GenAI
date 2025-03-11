// Function to Upload PDF
function uploadPDF() {
    let fileInput = document.getElementById("pdf-upload").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error:", error));
}

// Function to Send Chat Message
function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (!userInput.trim()) return;

    // Display user message
    let userMsg = document.createElement("div");
    userMsg.textContent = userInput;
    userMsg.classList.add("user-message");
    chatBox.appendChild(userMsg);

    // Send request to backend
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"message": userInput})
    })
    .then(response => response.json())
    .then(data => {
        let botMsg = document.createElement("div");
        botMsg.textContent = data.response;
        botMsg.classList.add("bot-message");
        chatBox.appendChild(botMsg);
    })
    .catch(error => console.error("Error:", error));

    document.getElementById("user-input").value = "";
}
