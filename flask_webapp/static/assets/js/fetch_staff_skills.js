// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const skillsTabButton = document.getElementById("skillsTabButton");

  fetch("/skills")
    .then((response) => response.json())
    .then((data) => {
      // Access and render the skills data in the skills card
      const skillsCard = document.getElementById("skillsCard");
      const skillsList = data.data;
      const accordionId = "skillsAccordion";

      skillsList.forEach((skill) => {
        const skillCard = document.createElement("div");
        skillCard.classList.add("accordion-item");

        skillCard.innerHTML = `
            <h2 class="accordion-header" id="panelsStayOpen-heading${skill}">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse${skill}" aria-expanded="true" aria-controls="panelsStayOpen-collapse${skill}">
                Accordion Item #1
              </button>
            </h2>
            <div id="panelsStayOpen-collapse${skill}" class="accordion-collapse collapse collapse" aria-labelledby="panelsStayOpen-heading${skill}">
              <div class="accordion-body">
                <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>

        `;

        skillsCard.appendChild(skillCard);
      });
    })
    .catch((error) => console.error("Error:", error));
});
