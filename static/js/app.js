// debug check if loaded
console.log("app.js loaded");
console.log("forms found:", document.querySelectorAll("form").length);

function updateUI(data) {
    document.getElementById("hunger").innerText = data.hunger.toFixed(1);
    document.getElementById("loneliness").innerText = data.loneliness.toFixed(1);
    document.getElementById("social_fatigue").innerText = data.social_fatigue.toFixed(1);
    document.getElementById("sleepy").innerText = data.sleepy.toFixed(1);
}

//setInterval(() => {
//    fetch("/status")
//        .then(res => res.json())
//        .then(updateUI);
//}, 2000);

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // stop page reload

        const formData = new FormData(form);
        // This captures which button was clicked
        if (e.submitter) {
            formData.set(e.submitter.name, e.submitter.value);
        }

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            // update UI immediately
            updateUI(data.state);

            // optional: show message
            document.getElementById("answer").innerText = data.message;
        })
        .catch(err => console.error("Fetch error:", err));
    });
});