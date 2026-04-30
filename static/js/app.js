//// debug check if loaded
//console.log("app.js loaded");
//console.log("forms found:", document.querySelectorAll("form").length);

let isLoading = false;

function setBar(stat, value) {
    const fill = document.getElementById(stat + "-fill");

    if (!fill) {
        console.log("Missing:", stat + "-fill")
        return;
    }

    const percent = Math.max(0, Math.min(100, value)); // clamp 0–100
    fill.style.width = percent + "%";
}

function updateUI(data) {

    setBar("hunger", data.hunger);
    setBar("loneliness", data.loneliness);
    setBar("sleepy", data.sleepy);
    setBar("social_fatigue", data.social_fatigue);
}

document.addEventListener("DOMContentLoaded", () => {
    fetch("/status")
        .then(res => res.json())
        .then(data => {
            updateUI(data);
        })
        .catch(err => console.error("Initial fetch error:", err));
});

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // stop page reload

        //avoid spamming buttons by blocking while loading
        if(isLoading) return;
        isLoading = true;

        const formData = new FormData(form);
        // This captures which button was clicked
        if (e.submitter) {
            formData.set(e.submitter.name, e.submitter.value);
        }

        const button = e.submitter;

        // disable button + show loading
        if (button) {
//            button.dataset.originalText = button.innerText;
            if (button.value === "ask"){
                button.disabled = true;
                }
        }
        // show thinking state
        document.getElementById("answer").innerText = "The oracle is thinking";
        document.getElementById("answer").classList.add("loading");

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            // update UI immediately
            document.getElementById("answer").classList.remove("loading");
            updateUI(data.state);
            document.getElementById("answer").innerText = data.message;
        })
        .catch(err => {
            console.error("Fetch error:", err);
            document.getElementById("answer").innerText = "⚠️ Something went wrong";
        })
        .finally(() => {
            // re-enable button
            if (button) {
                button.disabled = false;
                // restore label
                isLoading = false;
            }
        });
    });
});