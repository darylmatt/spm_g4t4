// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  fetch("/create/get_data")
    .then((response) => response.json())
    .then((data) => {
      const roleSelect = document.getElementById("createRoleDropdown");
      const roleList = data.data.roles;

      const countrySelect = document.getElementById("createCountryDropdown");
      const countryList = data.data.countries;

      const deptSelect = document.getElementById("createDepartmentDropdown");
      const deptList = data.data.departments;

      roleList.forEach((role) => {
        const selectOption = document.createElement("option");
        selectOption.value = role;
        selectOption.textContent = role;

        roleSelect.appendChild(selectOption);
      });

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

// Role is selected

document.addEventListener("DOMContentLoaded", function () {
  // Role is selected
  var selected_role = document.getElementById("createRoleDropdown");

  selected_role.addEventListener("change", function () {
    // Fetch the correct description from the database
    fetch("/get_role_description/" + selected_role.value)
      .then((response) => response.json())
      .then((data) => {
        //Populate the description box with this data
        text_area = document.getElementById("create_role_desc");
        desc = data.data;
        text_area.value = desc;
      });
  });
});
