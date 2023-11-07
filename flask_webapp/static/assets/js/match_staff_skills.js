document.addEventListener("DOMContentLoaded", function () {
    fetch('/skills')
      .then((response) => response.json())
      .then((data) => {
        const staffSkills = data.data.skill_names.map((skill) => skill.toLowerCase());

        listingData.forEach(function (listing) {
          const listingId = listing.listing_id;
  
          const skillsRequiredList = listing.skills_required_list.map((skill) => skill.toLowerCase());
  
          const matchedSkills = staffSkills.filter((skillItem) =>
            skillsRequiredList.includes(skillItem)
          );
  
          const totalRequiredSkillsCount = skillsRequiredList.length;
  
          const matchPercentage = (matchedSkills.length / totalRequiredSkillsCount) * 100;

          const skillProgressBar = document.getElementById(`skillProgressBar-${listingId}`);
          skillProgressBar.style.width = matchPercentage + "%";
          skillProgressBar.textContent = Math.ceil(matchPercentage) + "%";
          skillProgressBar.setAttribute("aria-valuenow", Math.ceil(matchPercentage));

          let progressBarColor = "";
          if (matchPercentage < 20) {
            progressBarColor = "bg-danger";
          } else if (matchPercentage >= 40) {
            progressBarColor = "bg-success";
          } else {
            progressBarColor = "bg-warning";
          }
  
          skillProgressBar.classList.remove("bg-danger", "bg-warning", "bg-success");
          skillProgressBar.classList.add(progressBarColor);
  
          const matchedSkillsContainer = document.getElementById(`matched-skills-${listingId}`);
          const unmatchedSkillsContainer = document.getElementById(`unmatched-skills-${listingId}`);
  
          matchedSkillsContainer.innerHTML = "";
          unmatchedSkillsContainer.innerHTML = "";
  
          listing.skills_required_list.forEach(function (skill) {
            const skillLowerCase = skill.toLowerCase();
            if (matchedSkills.includes(skillLowerCase)) {
              const matchedSkillItem = document.createElement("li");
              matchedSkillItem.textContent = skill;
              matchedSkillItem.style.color = "green";
              matchedSkillsContainer.appendChild(matchedSkillItem);
            } else {
              const unmatchedSkillItem = document.createElement("li");
              unmatchedSkillItem.textContent = skill;
              unmatchedSkillItem.style.color = "red";
              unmatchedSkillsContainer.appendChild(unmatchedSkillItem);
            }
          });

          if (matchedSkills.length === 0) {
            const noMatchedSkillsMessage = document.createElement("li");
            noMatchedSkillsMessage.textContent = "You have no matched skills";
            matchedSkillsContainer.appendChild(noMatchedSkillsMessage);
          }
  
          if (matchedSkills.length === totalRequiredSkillsCount) {
            const noUnmatchedSkillsMessage = document.createElement("li");
            noUnmatchedSkillsMessage.textContent = "You have no unmatched skills";
            unmatchedSkillsContainer.appendChild(noUnmatchedSkillsMessage);
          }

            let feedback = "";
            if (skillProgressBar.classList.contains("bg-danger")) {
            feedback = "You are not recommended for this role.";
            } else if (skillProgressBar.classList.contains("bg-warning")) {
            feedback = "You are recommended for this role.";
            } else {
            feedback = "You are highly recommended for this role.";
            }

            const feedbackContainer = document.getElementById(`feedback-${listingId}`);
            feedbackContainer.textContent = feedback;
        });
      })
      .catch((error) => {
        console.error("Error fetching staff skills:", error);
      });
  });
