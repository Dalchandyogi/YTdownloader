function showLoader() {
    document.getElementById('loader').style.display = 'block';
}

function clearPreviousContent() {
    document.getElementById('video-info').innerHTML = '';
    document.getElementById('tabs').innerHTML = '';
    document.getElementById('download-options').innerHTML = '';
} 

function openTab(tabName) {
    var i;
    var x = document.getElementsByTagName("table");
    var tabs = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "table";
    event.currentTarget.className += " active";
}

// Set the default active tab
document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.tablink.active').click();
});



let videoPlayer = document.getElementById('videoPlayer');
let thumbnail = document.getElementById('thumbnail');
let playPauseIcon = document.getElementById('playPauseIcon');
let playButton = document.querySelector('.play-button');

function startVideo() {
    if (videoPlayer.style.display === 'none') {
        thumbnail.style.display = 'none';
        playButton.style.display = 'none';
        videoPlayer.style.display = 'block';
        videoPlayer.play().then(() => {
            playPauseIcon.classList.replace('bx-play', 'bx-pause');
        }).catch(error => {
            console.error('Error trying to play the video:', error);
        });
    } else {
        playPause();
    }
}

function playPause() {
    if (videoPlayer.paused) {
        videoPlayer.play().then(() => {
            playPauseIcon.classList.replace('bx-play', 'bx-pause');
        }).catch(error => {
            console.error('Error trying to play the video:', error);
        });
    } else {
        videoPlayer.pause();
        playPauseIcon.classList.replace('bx-pause', 'bx-play');
    }
}

// Add event listeners for better control
videoPlayer.addEventListener('play', () => {
    playPauseIcon.classList.replace('bx-play', 'bx-pause');
});

videoPlayer.addEventListener('pause', () => {
    playPauseIcon.classList.replace('bx-pause', 'bx-play');
});
