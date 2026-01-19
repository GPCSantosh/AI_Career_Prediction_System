async function predictCareer() {
  let data = {
    domain: document.getElementById("domain").value,
    experience: document.getElementById("experience").value,
    employment: document.getElementById("employment").value,
    company_size: document.getElementById("company_size").value
  };

  let res = await fetch("https://ai-career-backend-vnmr.onrender.com/predict", {

    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(data)
  });

  let result = await res.json();

  document.getElementById("role").innerHTML = "Role: " + result.predicted_role;
  document.getElementById("salary").innerHTML = "Salary: " + result.salary_range_usd;
  document.getElementById("readiness").innerHTML = "Readiness: " + result.readiness_score;
}
