document.addEventListener("DOMContentLoaded", function () {
    // Fetch staff skills from your API
    fetch('http://127.0.0.1:5500/skills')
      .then((response) => response.json())
      .then((data) => {
        console.log("Staff skills fetched:", data);
        const staffSkills = data.data.skill_names.map((skill) => skill.toLowerCase());
        console.log(staffSkills);
  
        // Loop through listingData to update progress bars and skills
        listingData.forEach(function (listing) {
          const listingId = listing.listing_id;
  
          // Get the skills required for this listing
          const skillsRequiredList = listing.skills_required_list.map((skill) => skill.toLowerCase());
  
          // Calculate the number of matched skills
          const matchedSkills = staffSkills.filter((skillItem) =>
            skillsRequiredList.includes(skillItem)
          );
  
          console.log("Matched Skills:", matchedSkills);
  
          // Calculate the total number of required skills (matched + unmatched)
          const totalRequiredSkillsCount = skillsRequiredList.length;
  
          console.log("Total Required Skills Count:", totalRequiredSkillsCount);
  
          // Update the progress bar with the calculated percentage
          const skillProgressBar = document.getElementById(`skillProgressBar-${listingId}`);
          skillProgressBar.style.width = (matchedSkills.length / totalRequiredSkillsCount) * 100 + "%";
          skillProgressBar.textContent = Math.ceil((matchedSkills.length / totalRequiredSkillsCount) * 100) + "%";
          skillProgressBar.setAttribute("aria-valuenow", Math.ceil((matchedSkills.length / totalRequiredSkillsCount) * 100));
  
          // Define colors for different percentage ranges
          let progressBarColor = "";
          if (matchedSkills.length === 0) {
            progressBarColor = "bg-danger"; // Red
          } else if (matchedSkills.length < totalRequiredSkillsCount) {
            progressBarColor = "bg-warning"; // Orange
          } else {
            progressBarColor = "bg-success"; // Green
          }
  
          // Remove existing color classes and set the new color
          skillProgressBar.classList.remove("bg-danger", "bg-warning", "bg-success");
          skillProgressBar.classList.add(progressBarColor);
  
          // Display skills as matched and unmatched
          const matchedSkillsContainer = document.getElementById(`matched-skills-${listingId}`);
          const unmatchedSkillsContainer = document.getElementById(`unmatched-skills-${listingId}`);
  
          // Clear both containers
          matchedSkillsContainer.innerHTML = "";
          unmatchedSkillsContainer.innerHTML = "";
  
          listing.skills_required_list.forEach(function (skill) {
            const skillLowerCase = skill.toLowerCase();
            if (matchedSkills.includes(skillLowerCase)) {
              // Display matched skills in green
              const matchedSkillItem = document.createElement("li");
              matchedSkillItem.textContent = skill;
              matchedSkillItem.style.color = "green";
              matchedSkillsContainer.appendChild(matchedSkillItem);
            } else {
              // Display unmatched skills in red
              const unmatchedSkillItem = document.createElement("li");
              unmatchedSkillItem.textContent = skill;
              unmatchedSkillItem.style.color = "red";
              unmatchedSkillsContainer.appendChild(unmatchedSkillItem);
            }
          });
  
          // Display "You have no matched skills" if there are no matched skills
          if (matchedSkills.length === 0) {
            const noMatchedSkillsMessage = document.createElement("li");
            noMatchedSkillsMessage.textContent = "You have no matched skills";
            matchedSkillsContainer.appendChild(noMatchedSkillsMessage);
          }
  
          // Display "You have no unmatched skills" if there are no unmatched skills
          if (matchedSkills.length === totalRequiredSkillsCount) {
            const noUnmatchedSkillsMessage = document.createElement("li");
            noUnmatchedSkillsMessage.textContent = "You have no unmatched skills";
            unmatchedSkillsContainer.appendChild(noUnmatchedSkillsMessage);
          }

             // Define feedback based on the progress bar color
            let feedback = "";
            if (skillProgressBar.classList.contains("bg-danger")) {
            feedback = "You are not recommended for this role.";
            } else if (skillProgressBar.classList.contains("bg-warning")) {
            feedback = "You are recommended for this role.";
            } else {
            feedback = "You are highly recommended for this role.";
            }

            // Update the feedback div
            const feedbackContainer = document.getElementById(`feedback-${listingId}`);
            feedbackContainer.textContent = feedback;
        });
      })
      .catch((error) => {
        console.error("Error fetching staff skills:", error);
      });
  });
