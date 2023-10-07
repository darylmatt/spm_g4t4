// application_history.js
document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the table body
    const tableBody = document.querySelector(".table tbody");

    // Function to populate the table with application history data
    function populateTable(data) {
        const applicationHistory = data.application_history; // Access the application history array

        // Clear existing table rows
        tableBody.innerHTML = "";

        // Loop through the application history data and create table rows
        applicationHistory.forEach((application, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <th scope="row">${index + 1}</th>
                <td>${application.staff_name}</td>
                <td>${application.role_name}</td>
                <td>${application.applied_date}</td>
                <td>
                    <button type="button" class="btn btn-${application.statusClass} rounded-pill">${application.status}</button>
                </td>
            `;

            // Append the row to the table body
            tableBody.appendChild(row);
        });
    }


    // Make an AJAX request to retrieve application history data
    fetch("/get_application_history/17") // Replace 19 with the actual staff_id
        .then((response) => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Error fetching application history data");
            }
        })
        .then((data) => {
            console.log("application_History:", data)
            // Populate the table with the retrieved data
            populateTable(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
