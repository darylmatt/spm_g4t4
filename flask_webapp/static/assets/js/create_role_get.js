let has_role = false,
  has_dept = false,
  has_country = false,
  has_skills = false,
  has_startDate = false,
  has_deadline = false,
  has_manager = false,
  has_vacancy = false,
  has_desc = false;

function checkFields() {
  console.log("checking fields");
  if (
    has_role &&
    has_country &&
    has_deadline &&
    has_dept &&
    has_skills &&
    has_startDate &&
    has_manager &&
    has_vacancy &&
    has_desc
  ) {
    document.getElementById("create_btn").disabled = false;
  } else {
    document.getElementById("create_btn").disabled = true;
  }
}

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

      const vacancy = document.getElementById("createVacancyInput");

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

  skillSelectModal = document.getElementById("skillSelectModalBody");

  defaultSkillBtn = document.getElementById("defaultSkillBtn");
  selected_skills = document.getElementById("selectedSkills");
  defaultSkillBtn.addEventListener("click", function () {

    selected_skills.innerHTML = "";
    get_default_skills();
  });

  clearBtn = document.getElementById("clearAllBtn");
  clearBtn.addEventListener("click", function () {
    selected_skills.innerHTML = "";
    has_skills = false;

    var checkboxes = document
      .getElementById("skillSelectModalBody")
      .querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
      checkbox.checked = false;
    });

    checkFields();
  });

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

        checkboxDiv.appendChild(checkbox);
        checkboxDiv.appendChild(checkboxLabel);
        skillSelectModal.appendChild(checkboxDiv);
      });
    });

  const selected_role = document.getElementById("createRoleDropdown");

  function get_default_skills() {
    fetch("/get_skills_required/" + selected_role.value)
      .then((response) => response.json())
      .then((data) => {
        var selected_skills = document.getElementById("selectedSkills");
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

  var desc = document.getElementById("create_role_desc");
  desc.addEventListener("change", function () {
    if (desc.value.trim() === "") {
      has_desc = false;
    } else {
      has_desc = true;
    }
    checkFields();
  });

  selected_role.addEventListener("change", function () {
    fetch("/get_role_description/" + selected_role.value)
      .then((response) => response.json())
      .then((data) => {
        has_role = true;
        text_area = document.getElementById("create_role_desc");
        description = data.data;
        text_area.value = description;
        document.getElementById("no_desc_error").hidden = true;
        has_desc = true;
      });

    get_default_skills();

    skillsError.hidden = true;

    checkFields();
  });

  function handleSelectedSkillsChange() {
    var selected_skill_values = [];
    var selected_skills = document.getElementById("selectedSkills");
    var noSkillsError = document.getElementById("noSkillsError");

    if (selected_skills.childNodes.length == 0) {
      has_skills = false;
      noSkillsError.hidden = false;
    } else {
      has_skills = true;
      noSkillsError.hidden = true;
      selected_skills.childNodes.forEach((child) => {
        selected_skill_values.push((skill_id = child.childNodes[0].id));
      });

      var checkboxes = document
        .getElementById("skillSelectModalBody")
        .querySelectorAll('input[type="checkbox"]');

      checkboxes.forEach((checkbox) => {
        if (selected_skill_values.includes(checkbox.value)) {
          checkbox.checked = true;
        } else {
          checkbox.checked = false;
        }
      });
    }
    checkFields();
  }

  const observer = new MutationObserver(handleSelectedSkillsChange);

  observer.observe(selected_skills, { childList: true });

  var saveBtn = document.getElementById("saveSelection");
  saveBtn.addEventListener("click", function () {
    container = document.getElementById("selectedSkills");
    container.innerHTML = "";

    checkedSkills = [];
    var checkboxes = document
      .getElementById("skillSelectModalBody")
      .querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach((checkbox) => {
      if (checkbox.checked == true) {
        checkedSkills.push(checkbox.id);
      }
    });

    checkedSkills.forEach((skill) => {
      const skillDiv = document.createElement("div");

      const skillContainer = document.createElement("div");
      skillContainer.id = skill;
      skillContainer.className = "non-clickable-container";

      const skillText = document.createElement("span");
      skillText.className = "non-clickable-text text-success";
      skillText.textContent = skill;
      const skillCloseBtn = document.createElement("button");
      skillCloseBtn.type = "button";
      skillCloseBtn.className = "btn-close";
      skillCloseBtn.setAttribute("aria-label", "Close");

      skillCloseBtn.addEventListener("click", function () {
        skillDiv.remove();
      });

      skillContainer.appendChild(skillText);
      skillContainer.appendChild(skillCloseBtn);
      skillDiv.appendChild(skillContainer);
      selected_skills.appendChild(skillDiv);
    });
  });

  const selected_country = document.getElementById("createCountryDropdown");
  const selected_dept = document.getElementById("createDepartmentDropdown");

  function get_manager() {
    fetch("/get_manager/" + selected_country.value + "/" + selected_dept.value)
      .then((response) => response.json())
      .then((data) => {
        code = data.code;
        if (code != 200) {
          document.getElementById("createManagerDropdown").hidden = true;
          document.getElementById("reportingMngError").value = data.message;
          document.getElementById("reportingMngError").hidden = false;
          return;
        }

        manager_names = data.data.name_list;
        manager_ids = data.data.id_list;

        document.getElementById("reportingMngError").hidden = true;

        const managerOptions = document.getElementById("createManagerDropdown");

        managerOptions.innerHTML = "";
        const defaultOption = document.createElement("option");
        defaultOption.value = "Select a manager";
        defaultOption.textContent = "Select a manager";
        defaultOption.disabled = true;
        defaultOption.selected = true;

        managerOptions.appendChild(defaultOption);

        manager_names.forEach((name, index) => {
          const option = document.createElement("option");
          option.value = manager_ids[index];
          option.textContent = name;

          managerOptions.appendChild(option);
        });

        managerOptions.hidden = false;
      });
  }

  var desc = document.getElementById("create_role_desc");
  desc.addEventListener("change", function () {
    console.log(desc.value);
    if (desc.value.trim() === "") {
      document.getElementById("no_desc_error").hidden = false;
      has_desc = false;
    } else {
      document.getElementById("no_desc_error").hidden = true;
      has_desc = true;
    }
    checkFields();
  });

  var selected_manager = document.getElementById("createManagerDropdown");
  selected_manager.addEventListener("change", function () {
    if (selected_manager.hidden == false) {
      has_manager = true;
    } else {
      has_manager = false;
    }
    checkFields();
  });

  var vacancy = document.getElementById("createVacancyInput");
  vacancy.addEventListener("change", function () {
    if (vacancy.value < 1) {
      has_vacancy = false;
      document.getElementById("vacancyInputWarning").hidden = false;
    } else {
      has_vacancy = true;
      document.getElementById("vacancyInputWarning").hidden = true;
    }
    checkFields();
  });

  selected_country.addEventListener("change", function () {
    has_country = true;
    if (selected_dept.value != "Select a department") {
      get_manager();
    } else {
      document.getElementById("reportingMngError").value =
        "Please select a department.";
    }
    checkFields();
  });

  selected_dept.addEventListener("change", function () {
    has_dept = true;
    if (selected_country.value != "Select a country") {
      get_manager();
    } else {
      document.getElementById("reportingMngError").value =
        "Please select a country.";
    }
    checkFields();
  });

  var today = new Date().toISOString().split("T")[0];
  document.getElementById("startDate").setAttribute("min", today);

  var startDate = document.getElementById("startDate");
  var errorMsg = document.getElementById("deadlineError");
  var endDate = document.getElementById("endDate");

  startDate.addEventListener("change", function () {
    has_startDate = true;
    console.log(startDate.value);
    console.log(endDate.value);
    if (errorMsg.hidden == false) {
      errorMsg.hidden = true;
      endDate.setAttribute("min", startDate.value);
      endDate.hidden = false;
    }

    else {
      endDate.setAttribute("min", startDate.value);
    }
    checkFields();
  });

  endDate = document.getElementById("endDate");

  endDate.addEventListener("change", function () {
    has_deadline = true;
    console.log(startDate.value);
    console.log(endDate.value);
    startDate.setAttribute("max", endDate.value);
    if (endDate.value < startDate.value) {
      endDate.setAttribute("min", startDate.value);
      endDate.value = startDate.value;
    }
    checkFields();
  });
  var createBtn = document.getElementById("create_btn");

  createBtn.addEventListener("click", function () {
    var skillList = [];
    selected_skills.childNodes.forEach((child) => {
      skillList.push(child.childNodes[0].id);
    });
    var requestData = {
      title: selected_role.value,
      department: selected_dept.value,
      country: selected_country.value,
      startDate: startDate.value,
      endDate: endDate.value,
      manager: selected_manager.value,
      vacancy: vacancy.value,
    };

    fetch("/create/check_listing_exist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        code = data.code;
        if (code == 201) {
          document.getElementById("createMsgLabel").innerHTML =
            "Role creation success!";
          document.getElementById("createMsgBody").innerHTML = data.message;
          document.getElementById("cannotCreate").hidden = true;
          document.getElementById("backToListings").hidden = false;
        } else {
          document.getElementById("createMsgLabel").innerHTML =
            "Role creation failure.";
          document.getElementById("createMsgBody").innerHTML = data.message;
          document.getElementById("cannotCreate").hidden = false;
          document.getElementById("backToListings").hidden = true;
        }
      });
  });

  var backButton = document.getElementById("backToListings");

  backButton.addEventListener("click", function () {
    window.location.href = "../../all_listings_HR/1";
  });
});
