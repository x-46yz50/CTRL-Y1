const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const declineButton = document.getElementById("decline-button");
const acceptButton = document.getElementById("accept-button");

let hasClicked = false;

function enterFullscreen() {
    const docEl = document.documentElement;
    if (docEl.requestFullscreen) docEl.requestFullscreen();
    else if (docEl.mozRequestFullScreen) docEl.mozRequestFullScreen();
    else if (docEl.webkitRequestFullscreen) docEl.webkitRequestFullscreen();
    else if (docEl.msRequestFullscreen) docEl.msRequestFullscreen();
}

function buttonClick(event) {
    event.preventDefault();
    if (!hasClicked) hasClicked = true;
    overlay.hidden = true;

    // Play + force fullscreen immediately
    video.play();
    enterFullscreen();

    // Try to fullscreen video itself (more reliable on mobile)
    if (video.requestFullscreen) {
        video.requestFullscreen().catch(() => {});
    } else if (video.webkitEnterFullscreen) {
        video.webkitEnterFullscreen(); // iOS fallback
    }
}

function videoClick(event) {
    event.preventDefault();
    enterFullscreen();
}

acceptButton.addEventListener("click", buttonClick);
declineButton.addEventListener("click", buttonClick);
video.addEventListener("click", videoClick);