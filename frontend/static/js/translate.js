document.getElementById("translate-btn").addEventListener("click", () => {
    const description = document.getElementById("description").innerText;
    fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: description, to: "fr" }) // Translate to ...
    })
        .then(response => response.json())
        .then(data => {
            if (data.translated_text) {
                document.getElementById("translated-description").innerText = `Translated: ${data.translated_text}`;
            } else {
                console.error("Error:", data.error);
            }
        });
});
