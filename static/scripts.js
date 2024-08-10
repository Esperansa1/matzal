$(document).ready(function() {
    // Autocomplete function for the name input field
    $("#nameInput").autocomplete({
        source: function(request, response) {
            const filteredNames = allNames.filter(name => name.startsWith(request.term));
            response(filteredNames.slice(0, 10));
        }
    });

    // Show or hide the reason input field based on the selected status
    $('#statusInput').change(function() {
        if ($(this).val() === 'אחר') {
            $('#reasonInput').show();
        } else {
            $('#reasonInput').hide();
        }
    });

    // Initial data update when the page loads
    updateList(namesData);
});

// Function to update the list of names and their statuses
function updateList(names) {
    const nameList = $('#nameList');
    nameList.empty();

    // Sort the names alphabetically
    const sortedNames = Object.entries(names).sort((a, b) => a[0].localeCompare(b[0]));

    // Create list items for each name and their status
    for (const [name, status] of sortedNames) {
        const listItem = $('<li>').text(`${name} - ${status}`).addClass('list-group-item');
        nameList.append(listItem);
    }

    // Update the counts of present and removed students
    $('#inListCount').text(Object.values(names).filter(status => status === 'נוכח').length);
    $('#removedCount').text(Object.values(names).filter(status => status !== 'נוכח').length);
}

// Function to handle adding or updating a name's status
function addName() {
    const nameInput = $('#nameInput').val().trim();
    const statusInput = $('#statusInput').val();
    let reasonInput = $('#reasonInput').val().trim();

    if (statusInput === 'אחר' && reasonInput === '') {
        alert('הכנס סיבה בבקשה.');
        return;
    }

    const status = reasonInput ? `${statusInput} - ${reasonInput}` : statusInput;

    if (nameInput === '') {
        alert('הכנס שם בבקשה.');
        return;
    }

    // Perform an AJAX POST request to update the name's status
    $.post('/update', { name: nameInput, status: status, reason: reasonInput }, function() {
        location.reload(); // Reload the page to reflect the updated data
    }).fail(function(response) {
        alert(response.responseJSON.error);
    });
}

// Function to handle resetting the names list
function resetNamesPrompt() {
    const password = prompt('הכנס סיסמה:');
    if (password) {
        $.post('/reset', { password: password }, function(response) {
            if (response.success) {
                location.reload(); // Reload the page to reflect the reset data
            } else {
                alert('סיסמה שגויה.');
            }
        });
    }
}

// Function to show the status tables for non-present students
function showTables() {
    const tablesContainer = $('#tablesContainer');
    tablesContainer.empty();

    const statuses = {
        'שירותים': [],
        'בהפסקה': [],
        'אחר': []
    };

    $('#nameList li').each(function() {
        const [name, ...parts] = $(this).text().split(' - ');
        const mainStatus = parts[0];
        const reason = parts.length > 1 ? parts.slice(1).join(' - ') : '';

        if (mainStatus !== 'נוכח') {
            if (!statuses[mainStatus]) {
                statuses[mainStatus] = [];
            }
            if (mainStatus !== 'שירותים' && mainStatus !== 'בהפסקה') {
                statuses['אחר'].push(`${name} - ${reason}`);
            } else {
                statuses[mainStatus].push(`${name} - ${mainStatus}`);
            }
        }
    });

    for (const [status, names] of Object.entries(statuses)) {
        if (names.length > 0) {
            const table = $('<table>').addClass('table table-striped status-table');
            const thead = $('<thead>');
            const tbody = $('<tbody>');
            const th = $('<th>').text(`${status} (${names.length})`).attr('colspan', '2');
            thead.append(th);
            names.forEach(name => {
                const tr = $('<tr>');
                const td = $('<td>').text(name);
                tr.append(td);
                tbody.append(tr);
            });
            table.append(thead);
            table.append(tbody);
            tablesContainer.append(table);
        }
    }
}
