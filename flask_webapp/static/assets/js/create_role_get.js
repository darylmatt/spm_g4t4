// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  fetch("/create/get_depts_and_countries")
    .then((response) => response.json())
    .then((data) => {
      // Access and render the skills data in the skills card
      const countrySelect = document.getElementById("createCountryDropdown");
      const countryList = data.data.countries;

      const deptSelect = document.getElementById("createDepartmentDropdown");

      const deptList = data.data.departments;

      countryList.forEach((country) => {
        const selectOption = document.createElement("option");
        selectOption.value = country;
        selectOption.textContent = country;

        countrySelect.appendChild(selectOption);
      });

      deptList.forEach((dept) => {
        const selectOption = document.createElement("option");
        selectOption.value = dept;
        selectOption.textContent = dept;

        deptSelect.appendChild(selectOption);
      });
    })

    .catch((error) => console.error("Error:", error));
});
