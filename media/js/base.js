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
	console.log("csrf token before");
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	    console.log("csrf token set");
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// do the dragging magic

/*$(document).ready(function(){
    $(".box_container").draggable({
        axis:"y",
    });
});*/

// video/tagging business

// global variables?! come on dear...
var pop = false;
var events = [];

// called before video loaded, so store them...
function render_event(type, start_time) {
    events.push([type, start_time]);
}

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

        // scrubbing
        $("#time").draggable({
            axis:"x",
            drag: function( event, ui ) {
                var pos = pop.duration() * parseFloat($('#time').css('left')) /
                        parseFloat($('#time').parent().css('width'));
                pop.currentTime(pos);
            }
        });

        // click on timeline
        $("#timeline").click(function(e) {
            var offset = $(this).offset();
            var x = e.clientX - offset.left;
            var pos = pop.duration() * x / parseFloat($('#timeline').css('width'));
            pop.currentTime(pos);
        });

        pop.on("timeupdate", function() {
            var percentage = Math.floor((100 / pop.duration()) *
                                        pop.currentTime());
            $("#time").css({left: percentage+"%"});
        });

        pop.on("loadeddata", function () {
            // go through the events we collected earlier...
            events.forEach(function(e) {
                console.log("rendering event...");
                inner_render_event(e[0],e[1]);
            });
        });

        pop.on("ended", function() {
            console.log("ended...");
            $("#movie_end").css("visibility", "visible");
        });

        // play the video right away
        pop.play();
    },false);
};

function restart_video() {
    $("#movie_end").css("visibility", "hidden");
    pop.currentTime(0);
    pop.play();
}


// actually render the event
function inner_render_event(type, start_time) {
    // convert time into %
    var left = (start_time/pop.duration())*100;
    $("#timeline").append(
        '<div class="event micro_circle" style="left:'+left+'%; margin-top:-0.75em">\
        </div>');
}

// actually render the event
function inner_render_my_event(type, start_time) {
    // convert time into %
    var left = (start_time/pop.duration())*100;
    $("#timeline").append(
        '<div class="event small_circle" style="left:'+left+'%;">\
            <div class="event_text button_text">'+type+'</div>\
        </div>');
}

// sends the event to the server and renders it
function add_event(event_type, event_id, movie_id,user_id) {
    // only works if we have a video running of course...
    if (pop!=false) {
        t = pop.currentTime();

        // save to django ->
        if (user_id=="None") {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_id,
                user: "",
                start_time: t,
                end_time: t+1
            });
        } else {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_id,
                user: parseInt(user_id),
                start_time: t,
                end_time: t+1
            });
        }

        // add to the page
        inner_render_my_event(event_type, t);
    }

}
