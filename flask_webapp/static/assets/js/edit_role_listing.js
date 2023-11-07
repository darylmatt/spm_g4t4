document.addEventListener("DOMContentLoaded", function () {
  fetch("/create/get_data")
    .then((response) => response.json())
    .then((data) => {
      var roleSelect = document.getElementById("editRoleDropdown");
      var countrySelect = document.getElementById("editCountryDropdown");
      var deptSelect = document.getElementById("editDeptDropdown");

      const editButtons = document.querySelectorAll("button.edit-listing-btn");

      editButtons.forEach((button) => {
        button.addEventListener("click", function () {
          console.log("Edit button with ID:", this.id, "was clicked");

          const modal = new bootstrap.Modal(
            document.getElementById("editListingModal")
          );

          document.getElementById("editManagerDropdown").value =
            "Searching our database...";
          document.getElementById("editManagerDropdown").disabled = true;
          const id = this.id.substring(7);
          fetch("/get_listing_by_id/" + id)
            .then((response) => response.json())
            .then((data) => {
              var currName = data.data.role_name;
              var currCountry = data.data.country;
              var currDept = data.data.dept;
              var currVacancy = data.data.num_opening;
              var currStart = data.data.date_open.substring(0, 10);
              var currEnd = data.data.date_close.substring(0, 10);
              var currManager = data.data.reporting_mng;

              const roleSelectOption = document.createElement("option");
              roleSelectOption.value = currName;
              roleSelectOption.textContent = currName;
              roleSelect.appendChild(roleSelectOption);
              roleSelectOption.selected = true;

              const countrySelectOption = document.createElement("option");
              countrySelectOption.value = currCountry;
              countrySelectOption.textContent = currCountry;
              countrySelect.appendChild(countrySelectOption);
              countrySelectOption.selected = true;

              const deptSelectOption = document.createElement("option");
              deptSelectOption.value = currDept;
              deptSelectOption.textContent = currDept;
              deptSelect.appendChild(deptSelectOption);
              deptSelectOption.selected = true;

              fetchRoleDescription(roleSelect.value);
              fetchDefaultSkills(roleSelect.value);

              get_manager(currCountry, deptSelect.value, currManager);

              setDropdownDefault("editManagerDropdown", data.data.manager_id);

              document.getElementById("editVacancyInput").value = currVacancy;
              document.getElementById("editStartDate").value = currStart;
              document.getElementById("editEndDate").value = currEnd;

              document
                .getElementById("editEndDate")
                .setAttribute("min", startDate.value);
            });

          save_btn.addEventListener("click", function () {
            console.log("save button clicked for id:", id);
            var requestData = {
              title: selected_role.value,
              department: selected_dept.value,
              country: selected_country.value,
              startDate: document.getElementById("editStartDate").value,
              endDate: document.getElementById("editEndDate").value,
              manager: document.getElementById("editManagerDropdown").value,
              vacancy: document.getElementById("editVacancyInput").value,
            };

            fetch("/update/check_listing_exist/" + id, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(requestData),
            })
              .then((response) => response.json())
              .then((data) => {
                //Get the code
                code = data.code;
                if (code == 201) {
                  document.getElementById("saveEditMsg").innerHTML =
                    "Role update success! Refresh to view changes.";
                } else {
                  document.getElementById("saveEditMsg").innerHTML =
                    "Role update failed.";
                }
                document.getElementById("saveEditMsg").hidden = false;
              });
          });

          modal.show();

          const selected_role = document.getElementById("editRoleDropdown");

          selected_role.addEventListener("change", function () {
            fetchRoleDescription(selected_role.value);
            fetchDefaultSkills(selected_role.value);
          });

          const selected_country = document.getElementById(
            "editCountryDropdown"
          );
          const selected_dept = document.getElementById("editDeptDropdown");

          selected_country.addEventListener("change", function () {
            has_country = true;
            if (selected_dept.value != "Select a department") {
              get_manager(selected_country.value, selected_dept.value, null);
            } else {
              document.getElementById("reportingMngError").value =
                "Please select a department.";
            }
          });

          selected_dept.addEventListener("change", function () {
            has_dept = true;
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
    document.getElementById("save_btn").disabled = true;
    document.getElementById("editManagerDropdown").disabled = true;
    fetch("/get_manager/" + country + "/" + dept)
      .then((response) => response.json())
      .then((data) => {
        code = data.code;
        if (code != 200) {
          document.getElementById("editManagerDropdown").hidden = true;
          document.getElementById("reportingMngError").value = data.message;
          document.getElementById("reportingMngError").hidden = false;
          return;
        }

        manager_names = data.data.name_list;
        manager_ids = data.data.id_list;
        document.getElementById("editManagerDropdown").disabled = false;
        document.getElementById("reportingMngError").hidden = true;

        const managerOptions = document.getElementById("editManagerDropdown");

        managerOptions.innerHTML = "";
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
        document.getElementById("save_btn").disabled = false;
      });
  }

  var save_btn = document.getElementById("save_btn");
  save_btn.disabled = true;
  var vacancyInput = document.getElementById("editVacancyInput");
  vacancyInput.addEventListener("change", function () {
    console.log(vacancyInput.value);
    if (vacancyInput.value < 1) {
      document.getElementById("vacancyInputWarning").hidden = false;
      document.getElementById("save_btn").disabled = true;
    } else {
      document.getElementById("save_btn").disabled = false;
      document.getElementById("vacancyInputWarning").hidden = true;
    }
  });

  var startDate = document.getElementById("editStartDate");
  var endDate = document.getElementById("editEndDate");
  endDate.addEventListener("change", function () {
    if (endDate.value < startDate.value) {
      endDate.setAttribute("min", startDate.value);
      endDate.value = startDate.value;
    }
    checkFields();
  });
  
});
