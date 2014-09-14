$(document).ready(function(){
    $(".box_container").draggable({
        axis:"y",
    });
});

function video_setup(image) {
    // Create a popcorn instance by calling Popcorn("#id-of-my-video")
    document.addEventListener("DOMContentLoaded", function () {

        var pop = Popcorn("#ourvideo");
        console.log(pop);

        pop.image({
        // seconds
            start: 2,
            // seconds
            end: 15,
            href: "",
            src: image,
            text: "DRUMBEAT",
            target: "footnotediv"
        });

        pop.code({
            start: 2.2,
            end: 20.7,
            onStart: function() {
              }
        });

        $("#time").draggable({
            axis:"x",
        });


        pop.on("timeupdate",
               function() {
                   var percentage = Math.floor((100 / pop.duration()) *
                                               pop.currentTime());
                   $("#time").css({left: percentage+"%"});
               }
              );

        // play the video right away
        pop.play();
    },false);

};
