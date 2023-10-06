document.addEventListener("DOMContentLoaded", function () {
    // Add a click event listener to all buttons with the class "cancel-button"
    const cancelButtons = document.querySelectorAll(".cancel-button");

    cancelButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const applicationId = sessionStorage.getItem("ApplicationID");

            if (applicationId) {
                // Call your cancel application function with the application ID
                cancelApplication(applicationId);
            } else {
                // Handle the case where applicationId is not found in local storage
                alert("Application ID not found in local storage");
            }
        });
    });

    // Function to send an HTTP DELETE request to cancel an application
    function cancelApplication(applicationId) {
        // Define the URL of your Flask route
        const url = `/delete_application/${applicationId}/19`;

        // Send an HTTP DELETE request using the Fetch API
        fetch(url, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.status === 200) {
                    // Application was deleted successfully
                    sessionStorage.removeItem("ApplicationID");
                    alert("Application deleted successfully");
                    // You can also remove the associated HTML element if needed
                    // button.parentElement.remove();
                } else if (response.status === 404) {
                    // Application not found
                    alert("Application not found. It may have already been deleted.");
                } else if (response.status === 400) {
                    // Application past the deadline
                    alert("Application cannot be deleted as it's past the deadline.");
                } else {
                    // Handle other errors
                    alert("Error deleting application. Please try again later.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An unexpected error occurred while deleting the application.");
            });
    }
});
