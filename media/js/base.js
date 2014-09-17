// security stuff for async to prevent csrf

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// do the dragging magic

$(document).ready(function(){
    $(".box_container").draggable({
        axis:"y",
    });
});

// video/tagging business

// global variables?! come on dear...
pop = false;

function video_setup(image) {
    // Create a popcorn instance by calling Popcorn("#id-of-my-video")
    document.addEventListener("DOMContentLoaded", function () {

        pop = Popcorn("#ourvideo");
        console.log(pop);

/*        pop.image({
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
*/

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

function render_event(type, start_time) {
    // need to wait for video...
    document.addEventListener("DOMContentLoaded", function () {
        inner_render_event(type, start_time);
    });
}

function inner_render_event(type, start_time) {
    // convert time into %
    var left = (start_time/pop.duration())*100;
    $("#timeline").append(
        '<div class="event small_circle" style="left:'+left+'%;">\
            <div class="event_text button_text">'+type+'</div>\
        </div>');
}

function add_event(event_type, event_id, movie_id) {
    // only works if we have a video running of course...
    if (pop!=false) {
        t = pop.currentTime();

        console.log(t);

        // save to django ->
        $.post("/spit_event/", {
            movie: movie_id,
            type: event_id,
            start_time: t,
            end_time: t+1
        });

        // add to the page
        inner_render_event(event_type, t);
    }

}
