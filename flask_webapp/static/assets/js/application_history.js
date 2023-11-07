document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector(".table tbody");

    function populateTable(data) {
        const applicationHistory = data.application_history;

        tableBody.innerHTML = "";

        applicationHistory.forEach((application, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <th class="align-middle" scope="row">${index + 1}</th>
                <td class="align-middle">${application.staff_name}</td>
                <td class="align-middle">${application.role_name}</td>
                <td class="align-middle">${application.applied_date}</td>
                <td class="align-middle">
                    <div class="d-flex align-items-center">
                        <span style="margin-right: 5px;">${application.status}</span>
                        <button id="cancelButton" type="button" class="btn btn-danger cancel-button" data-bs-target="#verticalycentered" data-application-id="${application.application_id}">Cancel</button>
                    </div>
                </td>
            `;

            tableBody.appendChild(row);

            const cancelButton = row.querySelector(".cancel-button");
            cancelButton.addEventListener("click", function () {
                const applicationId = cancelButton.getAttribute("data-application-id");

                if (applicationId) {
                    cancelApplication(applicationId);
                } else {
                    alert("Application ID not found.");
                }
            });
        });
    }

    function cancelApplication(applicationId) {
        const url = `/delete_application/${applicationId}`;

        fetch(url, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.status === 200) {
                    alert("Application deleted successfully");

                    location.reload();
                } else if (response.status === 404) {
                    alert("Application not found. It may have already been deleted.");
                } else if (response.status === 400) {
                    alert("Application cannot be deleted as it's past the deadline.");
                } else {
                    alert("Error deleting application. Please try again later.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An unexpected error occurred while deleting the application.");
            });
    }

    fetch("/get_application_history")
        .then((response) => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Error fetching application history data");
            }
        })
        .then((data) => {
            console.log("application_History:", data)
            populateTable(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
