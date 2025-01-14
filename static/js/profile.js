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

function clearForm(formId) {
    var form = document.getElementById(formId);
    var inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(function(input) {
        if (input.type === 'checkbox' || input.type === 'radio') {
            input.checked = false;
        } else if (input.tagName === 'SELECT') {
            input.selectedIndex = -1;
        } else {
            input.value = '';
        }
    });
}

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

function editSkill(skillId, skillName) {
    document.getElementById('edit_skill_id').value = skillId;
    document.getElementById('edit_skill_name').value = skillName;
    document.getElementById('edit-skill-form').style.display = 'block';
}

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