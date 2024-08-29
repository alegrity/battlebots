function sendGetRequest(url, data) {
    // Construct URL with parameters
    const params = new URLSearchParams(data).toString();
    const fullUrl = `${url}?${params}`;

    fetch(fullUrl, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(responseText => {
        console.log('Response from server:', responseText);
    })
    .catch(error => {
        console.error('Error sending GET request:', error);
    });
}

// Vector representation logic
const vectorLine = document.getElementById('vector-line');
const joystickContainer = document.getElementById('joystick-container');
let containerRect = joystickContainer.getBoundingClientRect();
let lastSendTime = 0;

function updateVectorPosition(clientX, clientY) {
    let offsetX = clientX - containerRect.left;
    let offsetY = clientY - containerRect.top;

    let x = (offsetX / containerRect.width) * 2 - 1;
    let y = (offsetY / containerRect.height) * 2 - 1;

    if (x > 1) x = 1;
    if (x < -1) x = -1;
    if (y > 1) y = 1;
    if (y < -1) y = -1;

    let angle = Math.atan2(y, x) * (180 / Math.PI);
    let length = Math.sqrt(x * x + y * y);

    vectorLine.style.transform = `translateX(-50%) rotate(${angle + 90}deg) scaleY(${length * 1.5})`;

    const now = Date.now();
    if (now - lastSendTime > 250) {
        sendGetRequest('/vector', { x: x.toFixed(2), y: y.toFixed(2) });
        lastSendTime = now;
    }
}

function resetVectorPosition() {
    vectorLine.style.transform = 'translateX(-50%) rotate(0deg) scaleY(0)';
    sendGetRequest('/vector', { x: 0, y: 0 });
}

joystickContainer.addEventListener('touchstart', (e) => {
    updateVectorPosition(e.touches[0].clientX, e.touches[0].clientY);
});

joystickContainer.addEventListener('touchmove', (e) => {
    e.preventDefault(); 
    updateVectorPosition(e.touches[0].clientX, e.touches[0].clientY);
});

joystickContainer.addEventListener('touchend', resetVectorPosition);
joystickContainer.addEventListener('mousedown', (e) => {
    updateVectorPosition(e.clientX, e.clientY);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
});

function onMouseMove(e) {
    updateVectorPosition(e.clientX, e.clientY);
}

function onMouseUp() {
    resetVectorPosition();
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
}

document.getElementById("slider").addEventListener("input", function() {
    let value = this.value;
    sendGetRequest("/slider", { value: value });
});

document.getElementById("button1").addEventListener("click", function() {
    sendGetRequest("/button1", { state: 'pressed' });
});

document.getElementById("button2").addEventListener("click", function() {
    sendGetRequest("/button2", { state: 'pressed' });
});

document.getElementById("button3").addEventListener("click", function() {
    sendGetRequest("/button3", { state: 'pressed' });
});

document.getElementById("button4").addEventListener("click", function() {
    sendGetRequest("/button4", { state: 'pressed' });
});

window.addEventListener('resize', () => {
    containerRect = joystickContainer.getBoundingClientRect();
});
