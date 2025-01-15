/**
 * Toggles the visibility of a section's view and form.
 * @param {string} section - The section to toggle (e.g., 'contact-info', 'about-me').
 */
function toggleEdit(section) {
    var view = document.getElementById(section + '-view');
    var form = document.getElementById(section + '-form');
    if (view.style.display === 'none') {
        view.style.display = 'block';
        form.style.display = 'none';
    } else {
        view.style.display = 'none';
        form.style.display = 'block';
    }
}

/**
 * Clears all input fields in a form.
 * @param {string} formId - The ID of the form to clear.
 */
function clearForm(formId) {
    var form = document.getElementById(formId);
    var inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(function (input) {
        if (input.type === 'checkbox' || input.type === 'radio') {
            input.checked = false;
        } else if (input.tagName === 'SELECT') {
            input.selectedIndex = -1;
        } else {
            input.value = '';
        }
    });
}

/**
 * Adds a new skill to the user's profile.
 */
function addNewSkill() {
    var newSkillInput = document.getElementById('new_skill');
    var newSkillName = newSkillInput.value.trim();
    if (newSkillName) {
        // Send an AJAX request to add the new skill
        fetch('/add_skill/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ name: newSkillName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    var skillsList = document.getElementById('skills-list');
                    var newListItem = document.createElement('li');
                    newListItem.dataset.skillId = data.skill_id;
                    newListItem.innerHTML = `${newSkillName} <i class="fas fa-edit" onclick="editSkill('${data.skill_id}', '${newSkillName}')"></i> <i class="fas fa-trash-alt" onclick="deleteSkill('${data.skill_id}')"></i>`;
                    skillsList.appendChild(newListItem);
                    newSkillInput.value = '';
                } else {
                    alert('Error adding skill: ' + data.error);
                }
            });
    }
}

/**
 * Deletes a skill from the user's profile.
 * @param {string} skillId - The ID of the skill to delete.
 */
function deleteSkill(skillId) {
    // Send an AJAX request to delete the skill
    fetch('/delete_skill/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ skill_id: skillId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var skillListItem = document.querySelector(`li[data-skill-id="${skillId}"]`);
                if (skillListItem) {
                    skillListItem.remove();
                }
            } else {
                alert('Error deleting skill: ' + data.error);
            }
        });
}

/**
 * Populates the edit form with the skill's current data and displays the form.
 * @param {string} skillId - The ID of the skill to edit.
 * @param {string} skillName - The current name of the skill.
 */
function editSkill(skillId, skillName) {
    document.getElementById('edit_skill_id').value = skillId;
    document.getElementById('edit_skill_name').value = skillName;
    document.getElementById('edit-skill-form').style.display = 'block';
}

/**
 * Saves the edited skill to the user's profile.
 */
function saveEditedSkill() {
    var skillId = document.getElementById('edit_skill_id').value;
    var skillName = document.getElementById('edit_skill_name').value.trim();
    if (skillName) {
        // Send an AJAX request to save the edited skill
        fetch('/edit_skill/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ skill_id: skillId, name: skillName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    var skillListItem = document.querySelector(`li[data-skill-id="${skillId}"] .skill-name`);
                    if (skillListItem) {
                        skillListItem.textContent = skillName;
                    }
                    document.getElementById('edit-skill-form').style.display = 'none';
                } else {
                    alert('Error editing skill: ' + data.error);
                }
            });
    }
}

/**
 * Deletes the user's profile picture and reverts to the default image.
 */
function deleteProfilePicture() {
    // Send an AJAX request to delete the profile picture
    fetch('/delete_profile_picture/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ delete_profile_picture: true })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var profilePicture = document.querySelector('img[alt="Profile Image"]');
                if (profilePicture) {
                    profilePicture.src = 'https://i.imgur.com/2Q3XOlp.jpeg';
                }
            } else {
                alert('Error deleting profile picture: ' + data.error);
            }
        });
}

/**
 * Retrieves the value of a cookie by name.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie, or null if not found.
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}