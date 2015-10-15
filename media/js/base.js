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

function burrow_event() {
    $(this).off( 'click' );
    $('.info-text').html('Click on the burrow to begin the video.');
    $("#ourvideo").click(function(e) {
    var parentOffset = $(this).parent().offset(); 
    var burrowX = e.pageX - parentOffset.left;
    var burrowY = e.pageY - parentOffset.top;
    
    burrowClicked = true;

    $("#cricket_player").append('<div class="click-video-circle" style="width: 100px; height: 100px; border-radius: 50px; background: #BECC6D; position: absolute; opacity: 0.7; display: block; top:'+(burrowY)+'px; left:'+(burrowX - 50)+'px;"></div>');
    $('.click-video-circle').fadeOut();
    pop.play();

    videoClickEvents['burrowXY'] = [burrowX, burrowY];
    $('.info-text').html('Enter the ID of the cricket when or if you see it.');
    
    });
}


function video_setup(image) {
    // Create a popcorn instance by calling Popcorn("#id-of-my-video")
    document.addEventListener("DOMContentLoaded", function () {

        burrowClicked = false;
        noCricket = false;
        noCricketEnd = false;
        cricketFirstClicked = false;
        idEntered = false;
        cricketLastClicked = false;

        videoClickEvents = {'burrowXY' : '', 'cricketStartXY' : '', 'cricketEndXY' : ''}

        pop = Popcorn("#ourvideo");

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

*/
        
        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                $('.top_layer').css({'z-index' : '-1'});

                if (cricketFirstClicked === false) {

                    $('.info-text').html('Click on the cricket if you can see it <button id="no_cricket">No Cricket</button>.');
                    $("#ourvideo").click(function(e) {
                        $(this).off( 'click' );
                        var parentOffset = $(this).parent().offset(); 
                        var cricketStartX = e.pageX - parentOffset.left;
                        var cricketStartY = e.pageY - parentOffset.top;

                        if (noCricket === false){
                            videoClickEvents['cricketStartXY'] = [cricketStartX, cricketStartY];
                            console.log(videoClickEvents['cricketStartXY'])
                            $("#cricket_player").append('<div class="click-video-circle" style="width: 100px; height: 100px; border-radius: 50px; background: #F8AFC2; position: absolute; opacity: 0.7; display: block; top:'+(cricketStartY)+'px; left:'+(cricketStartX - 50)+'px;"></div>');
                            $('.click-video-circle').fadeOut();
                        } else {
                            videoClickEvents['cricketStartXY'] = '';
                        }

                        $(this).off('click');

                        burrow_event();
                        });
                };


                $('#no_cricket').click(function() {
                    console.log('No cricket')
                    $('.info-text').html('Click on the burrow to begin the video.');
                    $(this).off( 'click' );
                    noCricket = true;
                    burrow_event();
                });

                }
        });

        pop.on("ended", function() {
            $('.top_layer').css({'z-index' : '1'});

            if (burrowClicked === true) {
                $('.info-text').html('Click on the cricket to finish the video <button id="no_cricket_end">No cricket</button>'); 
                $('#ourvideo').click(function(e) {
                    $(this).off( 'click' );
                    $('.info-text').html('Events Complete');
                    pop.pause();

                    var parentOffset = $(this).parent().offset(); 
                    var cricketEndX = e.pageX - parentOffset.left;
                    var cricketEndY = e.pageY - parentOffset.top;

                    cricketLastClicked = true;

                    if (noCricketEnd === false) {
                        videoClickEvents['cricketEndXY'] = [cricketEndX, cricketEndY];
                        $("#cricket_player").append('<div class="click-video-circle" style="width: 100px; height: 100px; border-radius: 50px; background: #717892; position: absolute; opacity: 0.7; display: block; top:'+(cricketEndY)+'px; left:'+(cricketEndX - 50)+'px;"></div>');
                        $('.click-video-circle').fadeOut();
                    } else {
                        videoClickEvents = '';
                    }
                    $("#movie_end").css("visibility", "visible");
                });  
            } else if (cricketFirstClicked === false) {
                $('.info-text').html('No cricket clicked [no cricket seen?]'); 
            }

             $('#no_cricket_end').click(function() {
                    $(this).off( 'click' );
                    $('.info-text').html('Events Complete');                
                    noCricketEnd = true;   
                    $('#ourvideo').off( 'click' );
                    $("#movie_end").css("visibility", "visible");
            });


            console.log(videoClickEvents);

        });

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

        // pop.on("ended", function() {
        //     console.log("ended...");
        //     $("#movie_end").css("visibility", "visible");

        // });


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
