document.addEventListener("DOMContentLoaded", function () {
  // Fetch data and populate dropdowns
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
      console.log("done");
    });

  // Role is selected
  var selected_role = document.getElementById("createRoleDropdown");

  selected_role.addEventListener("change", function () {
    // Fetch the correct description from the database
    fetch("/get_role_description/" + selected_role.value)
      .then((response) => response.json())
      .then((data) => {
        // Populate the description box with this data
        text_area = document.getElementById("create_role_desc");
        desc = data.data;
        text_area.value = desc;
      });
  });

  var selected_country = document.getElementById("createCountryDropdown");
  var selected_dept = document.getElementById("createDepartmentDropdown");

  function get_manager() {
    fetch("/get_manager/" + selected_country.value + "/" + selected_dept.value)
      .then((response) => response.json())
      .then((data) => {
        // Populate the reporting manager box
        code = data.code;
        if (code != 200) {
          //Error message on the reporting manager box
          document.getElementById("createManagerDropdown").hidden = true;
          document.getElementById("reportingMngError").value = data.message;
          document.getElementById("reportingMngError").hidden = false;
          return;
        }

        manager_names = data.data.name_list;
        manager_ids = data.data.id_list;

        // Provide select options
        document.getElementById("reportingMngError").hidden = true;

        // Create select element
        const managerOptions = document.getElementById("createManagerDropdown");

        managerOptions.innerHTML = "";
        // Create default option
        const defaultOption = document.createElement("option");
        defaultOption.value = "Select a manager";
        defaultOption.textContent = "Select a manager";
        defaultOption.disabled = true;
        defaultOption.selected = true;

        managerOptions.appendChild(defaultOption);

        // Populate the select element with manager options
        manager_names.forEach((name, index) => {
          const option = document.createElement("option");
          option.value = manager_ids[index];
          option.textContent = name;

          managerOptions.appendChild(option);
        });

        managerOptions.hidden = false;
      });
  }

  // If user selected country first
  selected_country.addEventListener("change", function () {
    // Fetch the correct description from the database
    if (selected_dept.value != "Select a department") {
      get_manager();
    } else {
      document.getElementById("reportingMngError").value =
        "Please select a department.";
    }
  });

  // If user selected department first
  selected_dept.addEventListener("change", function () {
    // Fetch the correct description from the database
    if (selected_country.value != "Select a country") {
      get_manager();
    } else {
      document.getElementById("reportingMngError").value =
        "Please select a country.";
    }
  });

  // Set the calendar date
  var today = new Date().toISOString().split("T")[0];
  document.getElementById("startDate").setAttribute("min", today);

  //Get start date
  startDate = document.getElementById("startDate");
  var errorMsg = document.getElementById("deadlineError");
  var endDate = document.getElementById("endDate");

  startDate.addEventListener("change", function () {
    //User setting date for the first time
    if (errorMsg.hidden == false) {
      errorMsg.hidden = true;
      endDate.setAttribute("min", startDate.value);
      endDate.hidden = false;
    }

    //User setting date for the second time
    else {
      endDate.setAttribute("min", startDate.value);
    }
  });

  endDate = document.getElementById("endDate");

  endDate.addEventListener("change", function () {
    startDate.setAttribute("max", endDate.value);
    //Check if earlier than start date
    if (endDate.value < startDate.value) {
      endDate.setAttribute("min", startDate.value);
      endDate.value = startDate.value;
    }
  });
});
