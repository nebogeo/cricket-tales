(function () {
  var video = document.querySelector('video');
  var playBtn = document.querySelector('.canvas-play');

  if (playBtn) {
    playBtn.addEventListener('click', function () {
      video.play();
      if (video.paused) {
        console.log("paused")
        video.play();
      } else {
        video.pause();
      }
    });
  }
}());