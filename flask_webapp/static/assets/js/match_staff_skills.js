document.addEventListener("DOMContentLoaded", function () {

    // Fetch staff skills from your API
    fetch('http://127.0.0.1:5500/skills')
    .then((response) => response.json())
    .then((data) => {
      console.log("Staff skills fetched:", data);
      const staffSkills = data.data.skill_names.map((skill) => skill.toLowerCase());
      console.log(staffSkills);
      console.log("Skills Required for Listing:", skills_required_list);


  
        // Loop through listingData to update progress bars and skills
        listing_data.forEach(function (listing) {
          const listingId = listing.listing_id;
          
          // Query the DOM to get the matched and unmatched skills lists
          const matchedSkillsList = document.querySelectorAll(`#matched-skills-${listingId} li`);
          const unmatchedSkillsList = document.querySelectorAll(`#unmatched-skills-${listingId} li`);
  
          // Calculate the number of matched skills
          const matchedSkillsCount = Array.from(matchedSkillsList).filter((skillItem) =>
            staffSkills.includes(skillItem.textContent.trim().toLowerCase())
          ).length;
  
          console.log("Matched Skills Count:", matchedSkillsCount);
  
          // Calculate the total number of required skills (matched + unmatched)
          const totalRequiredSkillsCount = matchedSkillsList.length + unmatchedSkillsList.length;
  
          console.log("Total Required Skills Count:", totalRequiredSkillsCount);
  
          // Calculate the match percentage
          const matchPercentage = (matchedSkillsCount / totalRequiredSkillsCount) * 100;
  
          console.log("Match Percentage:", matchPercentage);
  
          // Round the percentage up to the nearest integer
          const roundedMatchPercentage = Math.ceil(matchPercentage);
  
          console.log("Rounded Match Percentage:", roundedMatchPercentage);
  
          // Update the progress bar with the calculated percentage
          const skillProgressBar = document.getElementById(`skillProgressBar-${listingId}`);
          skillProgressBar.style.width = roundedMatchPercentage + "%";
          skillProgressBar.textContent = roundedMatchPercentage + "%";
          skillProgressBar.setAttribute("aria-valuenow", roundedMatchPercentage);
  
          // Define colors for different percentage ranges
          let progressBarColor = "";
          if (roundedMatchPercentage <= 35) {
            progressBarColor = "bg-danger"; // Red
          } else if (roundedMatchPercentage <= 65) {
            progressBarColor = "bg-warning"; // Orange
          } else {
            progressBarColor = "bg-success"; // Green
          }
  
          // Remove existing color classes and set the new color
          skillProgressBar.classList.remove("bg-danger", "bg-warning", "bg-success");
          skillProgressBar.classList.add(progressBarColor);

        // Display "You have no matching skills" if there are no matched skills
        if (matchedSkillsCount === 0) {
            const matchedSkillsContainer = document.getElementById(`matched-skills-${listingId}`);
            const noMatchingSkillsMessage = document.createElement("li");
            noMatchingSkillsMessage.textContent = "You have no matching skills";
            matchedSkillsContainer.appendChild(noMatchingSkillsMessage);
          }

        // Display "You have no unmatched skills" if there are no unmatched skills
        if (unmatchedSkillsList.length === 0) {
            const unmatchedSkillsContainer = document.getElementById(`unmatched-skills-${listingId}`);
            const noUnmatchedSkillsMessage = document.createElement("li");
            noUnmatchedSkillsMessage.textContent = "You have no unmatched skills";
            unmatchedSkillsContainer.appendChild(noUnmatchedSkillsMessage);
            }

        });
      })
      .catch((error) => {
        console.error("Error fetching staff skills:", error);
      });
  });
  