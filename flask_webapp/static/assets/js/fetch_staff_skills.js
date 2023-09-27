// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const skillsTabButton = document.getElementById("skillsTabButton");
  console.log("Loaded");

  fetch("/skills")
    .then((response) => response.json())
    .then((data) => {
      // Access and render the skills data in the skills card
      const skillsCard = document.getElementById("skillsCard");
      const skillsList = data.data;
      console.log(skillsList);

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
