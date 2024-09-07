function sendGetRequest(url, data) {
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

function updateVectorPosition(touch) {
    let offsetX = touch.clientX - containerRect.left;
    let offsetY = touch.clientY - containerRect.top;

    let x = (offsetX / containerRect.width) * 2 - 1;
    let y = (offsetY / containerRect.height) * 2 - 1;

    x = Math.max(-1, Math.min(1, x));
    y = Math.max(-1, Math.min(1, y));

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

function handleTouchEvent(event) {
    for (let i = 0; i < event.touches.length; i++) {
        const touch = event.touches[i];
        if (touch.target.id === 'joystick-container') {
            updateVectorPosition(touch);
        }
    }
}

joystickContainer.addEventListener('touchstart', handleTouchEvent);
joystickContainer.addEventListener('touchmove', handleTouchEvent);
joystickContainer.addEventListener('touchend', resetVectorPosition);
joystickContainer.addEventListener('mousedown', (e) => {
    updateVectorPosition(e);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
});

function onMouseMove(e) {
    updateVectorPosition(e);
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

document.getElementById("button5").addEventListener("click", function() {
    sendGetRequest("/button5", { state: 'pressed' });
});

window.addEventListener('resize', () => {
    containerRect = joystickContainer.getBoundingClientRect();
});
