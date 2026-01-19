async function predictCareer() {

  const domain = document.getElementById("domain").value;
  const experience = document.getElementById("experience").value;
  const employment = document.getElementById("employment").value;
  const company_size = document.getElementById("company_size").value;

  const payload = {
    domain: domain,
    experience: experience,
    employment: employment,
    company_size: company_size
  };

  try {
    const response = await fetch("https://ai-career-backend-vnmr.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    document.getElementById("role").innerHTML = "Predicted Role: " + result.predicted_role;
    document.getElementById("salary").innerHTML = "Salary Range: " + result.salary_range_usd;

    if (result.readiness_score !== undefined) {
      document.getElementById("readiness").innerHTML = "Readiness Score: " + result.readiness_score + "%";
    } else {
      document.getElementById("readiness").innerHTML = "Readiness Score: N/A";
    }

  } catch (error) {
    document.getElementById("role").innerHTML = "Backend not reachable";
    document.getElementById("salary").innerHTML = "";
    document.getElementById("readiness").innerHTML = "";
  }
}
