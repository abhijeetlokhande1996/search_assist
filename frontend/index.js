function go() {
  const query = document.getElementById("search_box").value;
  const URL = "http://127.0.0.1:8080/api/search_similar_products/";

  fetch(URL, {
    method: "POST",
    body: JSON.stringify({ query: query }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((resp) => resp.json())
    .then((data) => {
      console.log("---------- Result -----------");

      let table = "<table class='table'>";
      table += "<tr><td>Id</td><td>Name</td><td>Gender</td></tr>";

      data["products"].forEach((product) => {
        table += "<tr>";
        table += `<td>${product["id"]}</td>`;
        table += `<td>${product["product_name"]}</td>`;
        table += `<td>${product["gender"]}</td>`;
        table += "</tr>";
      });

      table += "</table>";
      document.getElementById("result").innerHTML = table;
    })
    .catch((err) => {
      console.error(err);
      document.getElementById("result").innerHTML = "Error Occured";
    });
}
