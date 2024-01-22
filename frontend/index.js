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
      console.log(data);
      document.getElementById("result").innerHTML = "See the Console";
    })
    .catch((err) => {
      document.getElementById("result").innerHTML = "Error Occured";
    });
}
