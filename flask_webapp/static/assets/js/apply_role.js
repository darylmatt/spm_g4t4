// apply_role.js

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the Apply buttons
    const confirmButton = document.getElementById("applyButton");
    const fakeApplyButton = document.getElementById("fakeApplyButton");
    
    // Add a click event listener to each Apply button
    confirmButton.addEventListener("click", function () {
            /// Get the card title containing the role name
            const cardTitle = confirmButton.closest(".tab-pane").querySelector(".card-title");

            // Extract the role name from the card title
            const roleName = cardTitle.textContent.trim();
            console.log("rolename:",roleName)
            
            // Send an HTTP GET request to get the listing ID by name
            fetch(`/get_listing_id_by_name/${encodeURIComponent(roleName)}`, {
                method: "GET",
            })
                .then((response) => {
                    if (response.status === 200) {
                        return response.json();
                    } else {
                        throw new Error("Failed to get listing ID by name");
                    }
                })
                .then((data) => {
                    // Extract the listing ID from the response
                    const listingId = data.listingId;

                    // Send an HTTP POST request to apply for the role by listing ID
                    fetch(`/apply_role/${listingId}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({}),
                    })
                        .then((response) => {
                            if (response.status === 201) {
                                // Application was submitted successfully
                                alert("Application submitted successfully");
                                // You can close the modal or perform other actions here
                            } else {
                                // Handle other response statuses (e.g., error cases)
                                alert("Error submitting application");
                            }
                        })
                        .catch((error) => {
                            console.error("Error:", error);
                            alert("An error occurred while submitting the application");
                        });
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred while getting the listing ID by name");
                });
        });
    });