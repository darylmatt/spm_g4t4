// apply_role.js

document.addEventListener("DOMContentLoaded", function () {
    
    // Get a reference to the Apply buttons
    const confirmButton = document.getElementById("applyButton");
    const fakeApplyButton = document.getElementById("fakeApplyButton");

    // Function to disable the "Apply" button
    function disableApplyButton() {
        fakeApplyButton.disabled = true
        fakeApplyButton.textContent = "Applied";
        confirmButton.disabled = true;
        confirmButton.textContent = "Applied"; 
    }

    // Initialize applicationId as undefined
    let applicationId;

    // Check if there's an application ID in sessionStorage
    const storedApplicationId = sessionStorage.getItem("ApplicationID");

    if (storedApplicationId) {
        // The user has already applied, so disable the Apply button
        applicationId = storedApplicationId;
        disableApplyButton();
    } else {
        // Check application status by calling the Flask route
        const staffId = 19; // Replace with the actual staff_id
        fetch(`/check_application_status/${applicationId}/${staffId}`, {
            method: "GET",
        })
        .then((response) => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Error checking application status");
            }
        })
        .then((data) => {
            const applicationStatus = data.status;
            if (applicationStatus === "Pending") {
                // Disable the Apply button if the status is "Pending"
                disableApplyButton();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

    // Add a click event listener to each Apply button
    confirmButton.addEventListener("click", function () {
        // Get the card title containing the role name
        const cardTitle = confirmButton.closest(".tab-pane").querySelector(".card-title");

        // Extract the role name from the card title
        const roleName = cardTitle.textContent.trim();
        console.log("rolename:", roleName);

        // Send an HTTP GET request to get the listing ID by name
        fetch(`/get_listing_id_by_name/${encodeURIComponent(roleName)}`, {
            method: "GET",
        })
            .then((response) => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw Error("Failed to get listing ID by name");
                }
            })
            .then((data) => {
                // Extract the listing ID from the response
                const listingId = data.listingId;
                console.log("listingId:", listingId)

                // Send an HTTP POST request to apply for the role by listing ID
                fetch(`/apply_role/${listingId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({}),
                })
                    .then(async (applyResponse) => {
                        console.log("Before parsing applyResponse.json()");
                        if (applyResponse.status === 201) {
                            console.log("Inside successful status check");
                            disableApplyButton();
                    
                            // Parse the returned application data as JSON
                            const applyData = await applyResponse.json();
                            console.log("applyData:", applyData);
                    
                            // Ensure that applyData contains the application_id
                            if (applyData && applyData.application_id) {
                                // Store the application ID in the variable
                                applicationId = applyData.application_id;
                                sessionStorage.setItem("ApplicationID", applicationId);
                                console.log("appid", applicationId);
                                // Application was submitted successfully
                                alert("Application submitted successfully");
                                return applyData;
                            }
                            
                        } else {
                            // Handle other response statuses (e.g., error cases)
                            alert("Error submitting application");
                        }
                    })
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred while getting the listing ID by name");
            });
    });
    initializeApplicationStatus();
});

