function predictCareer() {
    const domain = document.getElementById("domain").value;
    const experience = document.getElementById("experience").value;
    const employment = document.getElementById("employment").value;
    const company_size = document.getElementById("company_size").value;

    fetch("https://ai-career-backend-366f.onrender.com/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({domain, experience, employment, company_size})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            `Role: ${data.predicted_role}<br>
             Salary: ${data.salary_range_usd}<br>
             Readiness Score: ${data.readiness_score}%`;
    })
    .catch(() => {
        document.getElementById("result").innerText = "Backend not reachable";
    });
}
