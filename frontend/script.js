async function predictCareer() {
  let data = {
    domain: document.getElementById("domain").value,
    experience: document.getElementById("experience").value,
    employment: document.getElementById("employment").value,
    company_size: document.getElementById("company_size").value
  };

  let res = await fetch("https://ai-career-backend-366f.onrender.com/predict", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(data)
  });

  let result = await res.json();

    document.getElementById("role").innerHTML = "Role: " + result.predicted_role;
    document.getElementById("salary").innerHTML = "Salary: " + result.salary_range_usd;

    let score = result.readiness_score || 0;
    document.getElementById("readiness_bar").style.width = score + "%";
    document.getElementById("readiness_text").innerHTML = score + "% (" + result.readiness_level + ")";
}
