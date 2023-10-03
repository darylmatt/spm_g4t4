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

  //Get all skills
  //Get modal body
  skillSelectModal = document.getElementById("skillSelectModalBody");

  // Assuming you have a valid URL for fetching skills data
  fetch("/get_all_skills")
    .then((response) => response.json())
    .then((data) => {
      var skills = data.data;
      skills.forEach((skill) => {
        const checkboxDiv = document.createElement("div");
        checkboxDiv.className = "mb-3";
        const checkbox = document.createElement("input");
        checkbox.value = skill;
        checkbox.id = skill;
        checkbox.type = "checkbox";
        checkbox.className = "form-check-input";
        const checkboxLabel = document.createElement("label");
        checkboxLabel.className = "form-check-label";
        checkboxLabel.textContent = skill;

        // Append checkboxLabel to checkbox
        checkboxDiv.appendChild(checkbox);
        checkboxDiv.appendChild(checkboxLabel); // Append the label after the checkbox
        skillSelectModal.appendChild(checkboxDiv);
      });
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

    //Fetch the required skills from the database

    //Hide skills error
    skillsError.hidden = true;

    //Enable select skills button

    skillsSelectBtn.disabled = false;
    console.log(selected_role.value);
    const selected_skills = document.getElementById("selectedSkills");
    fetch("/get_skills_required/" + selected_role.value)
      .then((response) => response.json())
      .then((data) => {
        var required_skills = data.data.skills_required;
        required_skills.forEach((skill) => {
          console.log(skill);
          const skillDiv = document.createElement("div");
          // skillDiv.className = "col-md-3";

          const skillContainer = document.createElement("div");
          skillContainer.className = "non-clickable-container";

          const skillText = document.createElement("span");
          skillText.className = "non-clickable-text text-success";
          skillText.textContent = skill;
          const skillCloseBtn = document.createElement("button");
          skillCloseBtn.type = "button";
          skillCloseBtn.className = "btn-close";
          skillCloseBtn.setAttribute("aria-label", "Close");

          skillContainer.appendChild(skillText);
          skillContainer.appendChild(skillCloseBtn);
          skillDiv.appendChild(skillContainer);
          selected_skills.appendChild(skillDiv);
        });
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
  var startDate = document.getElementById("startDate");
  var errorMsg = document.getElementById("deadlineError");
  var endDate = document.getElementById("endDate");

  startDate.addEventListener("change", function () {
    //User setting date for the first time
    console.log(startDate.value);
    console.log(endDate.value);
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
    console.log(startDate.value);
    console.log(endDate.value);
    startDate.setAttribute("max", endDate.value);
    //Check if earlier than start date
    if (endDate.value < startDate.value) {
      endDate.setAttribute("min", startDate.value);
      endDate.value = startDate.value;
    }
  });
});
