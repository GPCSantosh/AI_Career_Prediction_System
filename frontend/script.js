function predictCareer() {
    const domain = document.getElementById("domain").value;
    const experience = document.getElementById("experience").value;
    const employment = document.getElementById("employment").value;
    const company_size = document.getElementById("company_size").value;

    if (!domain || !experience || !employment || !company_size) {
        document.getElementById("result").innerText = "Please select all fields.";
        return;
    }

    document.getElementById("result").innerText = "Connecting to backend...";

    fetch("https://ai-career-backend-366f.onrender.com/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            domain,
            experience,
            employment,
            company_size
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            `Predicted Role: <b>${data.predicted_role}</b><br>
             Salary Range: <b>${data.salary_range_usd}</b>`;
    })
    .catch(() => {
        document.getElementById("result").innerText = "Backend not reachable";
    });
}
