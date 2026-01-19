function predictCareer() {
    const domain = document.getElementById("domain").value;
    const expCode = document.getElementById("experience").value;
    const empCode = document.getElementById("employment").value;
    const sizeCode = document.getElementById("company_size").value;

    if (!domain || !expCode || !empCode || !sizeCode) {
        document.getElementById("result").innerText = "Please select all fields.";
        return;
    }

    // Convert codes to CSV values
    const experienceMap = { EN: "EN", MI: "MI", SE: "SE", EX: "EX" };
    const employmentMap = { FT: "Full Time", PT: "Part Time", CT: "Contract" };
    const sizeMap = { S: "Small", M: "Medium", L: "Large" };

    const experience = experienceMap[expCode];
    const employment = employmentMap[empCode];
    const company_size = sizeMap[sizeCode];

    document.getElementById("result").innerText = "Connecting to backend...";

    fetch("https://ai-career-backend-366f.onrender.com/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ domain, experience, employment, company_size })
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
