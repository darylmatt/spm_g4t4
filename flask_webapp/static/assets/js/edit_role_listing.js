document.addEventListener("DOMContentLoaded", function () {
  // Fetch all data
  fetch("/create/get_data")
    .then((response) => response.json())
    .then((data) => {
      const roleList = data.data.roles;
      var roleSelect = document.getElementById("editRoleDropdown");
      const countryList = data.data.countries;
      var countrySelect = document.getElementById("editCountryDropdown");
      const deptList = data.data.departments;
      var deptSelect = document.getElementById("editDeptDropdown");

      // Populate the role dropdown
      roleList.forEach((role) => {
        const selectOption = document.createElement("option");
        selectOption.value = role;
        selectOption.textContent = role;
        roleSelect.appendChild(selectOption);
      });

      // Populate the country dropdown
      countryList.forEach((country) => {
        const selectOption = document.createElement("option");
        selectOption.value = country;
        selectOption.textContent = country;
        countrySelect.appendChild(selectOption);
      });

      // Populate the department dropdown
      deptList.forEach((dept) => {
        const selectOption = document.createElement("option");
        selectOption.value = dept;
        selectOption.textContent = dept;
        deptSelect.appendChild(selectOption);
      });

      const editButtons = document.querySelectorAll("button.edit-listing-btn");

      editButtons.forEach((button) => {
        button.addEventListener("click", function () {
          console.log("Edit button with ID:", this.id, "was clicked");

          // Open the modal using Bootstrap attributes
          const modal = new bootstrap.Modal(
            document.getElementById("editListingModal")
          );

          // Reset the manager box
          document.getElementById("editManagerDropdown").value =
            "Searching our database...";
          document.getElementById("editManagerDropdown").disabled = true;

          // Retrieve the listing data from the server
          fetch("get_listing_by_id/" + this.id[7])
            .then((response) => response.json())
            .then((data) => {
              var currName = data.data.role_name;
              var currCountry = data.data.country;
              var currDept = data.data.dept;
              var currVacancy = data.data.num_opening;
              var currStart = data.data.date_open.substring(0, 10);
              var currEnd = data.data.date_close.substring(0, 10);
              var currManager = data.data.reporting_mng;

              // Set the default values for the dropdowns
              setDropdownDefault("editRoleDropdown", currName);
              setDropdownDefault("editCountryDropdown", currCountry);
              setDropdownDefault("editDeptDropdown", currDept);

              fetchRoleDescription(selected_role.value);
              fetchDefaultSkills(selected_role.value);

              get_manager(currCountry, deptSelect.value, currManager);

              setDropdownDefault("editManagerDropdown", data.data.manager_id);

              //set the default values of others
              document.getElementById("editVacancyInput").value = currVacancy;
              document.getElementById("editStartDate").value = currStart;
              document.getElementById("editEndDate").value = currEnd;
            });

          // Show the modal
          modal.show();

          const selected_role = document.getElementById("editRoleDropdown");

          // Fetch the correct description from the database

          selected_role.addEventListener("change", function () {
            fetchRoleDescription(selected_role.value);
            fetchDefaultSkills(selected_role.value);
          });

          const selected_country = document.getElementById(
            "editCountryDropdown"
          );
          const selected_dept = document.getElementById("editDeptDropdown");

          selected_country.addEventListener("change", function () {
            // Fetch the correct description from the database
            has_country = true;
            if (selected_dept.value != "Select a department") {
              get_manager(selected_country.value, selected_dept.value, null);
            } else {
              document.getElementById("reportingMngError").value =
                "Please select a department.";
            }
          });

          // If user selected department first
          selected_dept.addEventListener("change", function () {
            has_dept = true;
            // Fetch the correct description from the database
            if (selected_country.value != "Select a country") {
              get_manager(selected_country.value, selected_dept.value, null);
            } else {
              document.getElementById("reportingMngError").value =
                "Please select a country.";
            }
          });
        });
      });
    });
  function setDropdownDefault(dropdownId, value) {
    const dropdown = document.getElementById(dropdownId);
    const option = dropdown.querySelector(`option[value="${value}"]`);
    if (option) {
      option.selected = true;
    }
  }

  function fetchRoleDescription(roleValue) {
    var text_area = document.getElementById("edit_role_desc");
    text_area.innerHTML = "";
    text_area.value = "";
    fetch("/get_role_description/" + roleValue)
      .then((response) => response.json())
      .then((data) => {
        const description = data.data;
        text_area.value = description;
      });
  }

  function fetchDefaultSkills(roleValue) {
    fetch("/get_skills_required/" + roleValue)
      .then((response) => response.json())
      .then((data) => {
        var selected_skills = document.getElementById("editSelectedSkills");
        selected_skills.innerHTML = "";
        var required_skills = data.data.skills_required;

        required_skills.forEach((skill) => {
          const skillDiv = document.createElement("div");

          const skillContainer = document.createElement("div");
          skillContainer.id = skill;
          skillContainer.className = "non-clickable-container";

          const skillText = document.createElement("span");
          skillText.className = "non-clickable-text text-success";
          skillText.textContent = skill;

          skillContainer.appendChild(skillText);
          skillDiv.appendChild(skillContainer);
          selected_skills.appendChild(skillDiv);
        });
      });
  }

  function get_manager(country, dept, currManager) {
    // Make it disabled first
    //Append a loading option and set it to disabled
    document.getElementById("editManagerDropdown").textContent = "Loading..";
    document.getElementById("editManagerDropdown").disabled = true;
    fetch("/get_manager/" + country + "/" + dept)
      .then((response) => response.json())
      .then((data) => {
        // Populate the reporting manager box
        code = data.code;
        if (code != 200) {
          //Error message on the reporting manager box
          document.getElementById("editManagerDropdown").hidden = true;
          document.getElementById("reportingMngError").value = data.message;
          document.getElementById("reportingMngError").hidden = false;
          return;
        }

        manager_names = data.data.name_list;
        manager_ids = data.data.id_list;
        document.getElementById("editManagerDropdown").disabled = false;
        // Provide select options
        document.getElementById("reportingMngError").hidden = true;

        // Create select element
        const managerOptions = document.getElementById("editManagerDropdown");

        managerOptions.innerHTML = "";
        // Create default option
        const defaultOption = document.createElement("option");
        defaultOption.value = "Select a manager";
        defaultOption.textContent = "Select a manager";
        defaultOption.disabled = true;
        defaultOption.selected = true;

        managerOptions.appendChild(defaultOption);

        var mIndex = -2;

        if (currManager != null) {
          mIndex = manager_ids.indexOf(currManager);
        }

        // Populate the select element with manager options
        manager_names.forEach((name, index) => {
          var option = document.createElement("option");
          option.value = manager_ids[index];
          option.textContent = name;

          if (mIndex >= 0 && index == mIndex) {
            option.selected = true;
          }

          managerOptions.appendChild(option);
        });

        managerOptions.hidden = false;
      });
  }
});
