// Get edit listing button

document.addEventListener("DOMContentLoaded", function () {
  // Get all elements with the specified class name
  var pillButtons = document.querySelectorAll(
    ".list-group-item.list-group-item-action"
  );

  // Define the event listener function
  function handlePillButtonClick(event) {
    // You can access the data-listing-id attribute using the dataset property
    var listingId = event.currentTarget.dataset.listingId;
    console.log("Button clicked for listing ID: " + listingId);
    // Add your custom logic here

    var btnId = "editBtnListing" + listingId;

    document.getElementById(btnId).addEventListener("click", function () {
      console.log("edit listing button clicked");
      //Fetch data
      //Get all default values
      const currRoleName = document.getElementById(
        "update_role_dropdown"
      ).value;
      const currDept = document.getElementById("update_dept_dropdown").value;
      const currCountry = document.getElementById(
        "update_country_dropdown"
      ).value;

      console.log(currRoleName);
      console.log(currDept);
      console.log(currCountry);
      fetch("/create/get_data")
        .then((response) => response.json())
        .then((data) => {
          const roleSelect = document.getElementById("update_role_dropdown");
          const roleList = data.data.roles;

          const countrySelect = document.getElementById(
            "update_country_dropdown"
          );
          const countryList = data.data.countries;

          const deptSelect = document.getElementById("update_dept_dropdown");
          const deptList = data.data.departments;

          roleList.forEach((role) => {
            // Don't create select option for default role value
            if (role != currRoleName) {
              const selectOption = document.createElement("option");
              selectOption.value = role;
              selectOption.textContent = role;

              roleSelect.appendChild(selectOption);
            }
          });

          countryList.forEach((country) => {
            // Don't create select option for default country value
            if (country != currCountry) {
              const selectOption = document.createElement("option");
              selectOption.value = country;
              selectOption.textContent = country;

              countrySelect.appendChild(selectOption);
            }
          });

          deptList.forEach((dept) => {
            // Don't create select option for default dept value
            if (dept != currDept) {
              const selectOption = document.createElement("option");
              selectOption.value = dept;
              selectOption.textContent = dept;

              deptSelect.appendChild(selectOption);
            }
          });
          console.log("done");
        });
    });
  }

  // Add the event listener to each button
  pillButtons.forEach(function (button) {
    button.addEventListener("click", handlePillButtonClick);
  });
});
