// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Get a reference to the "Skills" tab button by its ID
  const skillsTabButton = document.getElementById("skillsTabButton");
  console.log("Yes pressed");

  // Add a click event listener to the "Skills" tab button
  // skillsTabButton.addEventListener("click", function () {
  // Make an AJAX request to the Flask route that returns skills data
  fetch("/skills")
    .then((response) => response.json())
    .then((data) => {
      // Access and render the skills data in the skills card
      const skillsCard = document.getElementById("skillsCard");
      const skillsList = data.data; // Access the "data" field from the JSON response
      console.log(skillsList);

      // Loop through the skills and create HTML elements for each skill
      skillsList.forEach((skill) => {
        const skillCard = document.createElement("div");
        skillCard.classList.add("card");
        skillCard.innerHTML = `
            <div class="card-body">
              <h5 class="card-title">${skill}</h5>
            </div>
          `;
        skillsCard.appendChild(skillCard);
      });
    })
    .catch((error) => console.error("Error:", error));
});
