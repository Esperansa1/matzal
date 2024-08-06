const socket = io();

socket.on('initial_data', (data) => {
    updateList(data.names);
    document.getElementById('removedCount').textContent = data.removed_names;
});

socket.on('update_data', (data) => {
    updateList(data.names);
    document.getElementById('removedCount').textContent = data.removed_names;
});

socket.on('name_not_found', () => {
    alert('Name not found in the list.');
});

function updateList(names) {
    const nameList = document.getElementById('nameList');
    nameList.innerHTML = '';
    names.forEach(name => {
        const li = document.createElement('li');
        li.textContent = name;
        nameList.appendChild(li);
    });
    document.getElementById('inListCount').textContent = names.length;
}

function removeName() {
    const nameInput = document.getElementById('nameInput').value.trim();
    if (nameInput === '') {
        alert('Please enter a name.');
        return;
    }
    socket.emit('remove_name', { name: nameInput });
    document.getElementById('nameInput').value = '';
}

function addName() {
    const nameInput = document.getElementById('nameInput').value.trim();
    if (nameInput === '') {
        alert('Please enter a name.');
        return;
    }
    socket.emit('add_name', { name: nameInput });
    document.getElementById('nameInput').value = '';
}

function resetNames() {
    socket.emit('reset_names');
}