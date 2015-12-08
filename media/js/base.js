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

// precache the images
// todo: convert to sprite sheet
imagelist = [];
function add_to_imagelist(id) {
    imagelist.push("button-"+i+".png");
    imagelist.push("button-"+i+"-offset.png");
    imagelist.push("button-"+i+"-high.png");
}
for (i=1; i<7; i++) {
    add_to_imagelist(i);
}
add_to_imagelist("shrew");
add_to_imagelist("bird");
imagelist.forEach( function(path) {
    new Image().src="/media/images/buttons/"+path;
} );

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

function build_id_keyboard() {

    $('#tag_cricket').draggable();
    //Constructing keyboard
    var id_keyboard_values = [['+', 'A', 'L', 'U'], ['=', 'C', 'N', 'V'], ['1', 'D', 'O', 'X'], ['6', 'E', 'P', 'Z'], ['7', 'H', 'S', '9'], ['J', 'T', 'Delete', 'Save']];
    var operators = ['Not sure', 'Cancel', 'Delete', 'Save'];
    //Enumerate for tr
    var table = '<table id="tag_cricket_id" class="table-striped table table-bordered">';
    $(id_keyboard_values).each(function (i, array) {
        table += '<tr>';
        //Enumerate for td
        $(array).each(function (n, list) {

            in_list = jQuery.inArray(list, operators );

            if (in_list != -1) {
                var operator_id = list.replace(/\s/g, '');
                table += '<td id="'+operator_id.toLowerCase()+'">'+list+'</td>';
            } else {
                table += '<td data-value="'+list+'" onClick="enter_id(this)">'+list+'</td>';
            }


        });
        table += '</tr>';
    });
    table += '</table>';

    //console.log(table);
    initialise_operators_keyboard();
}

function initialise_operators_keyboard() {
        $("#delete").click(function (){
            $('#tag_id').val('');
        });

        $("#save").click(function (){
            cricket_id = $('#tag_id').val();


            if (cricket_id.length == 2) {
                videoClickEvents['cricketId'] = cricket_id;
                $('p.cricket-id-display').html('ID: <span class="cricket-id-char">'+cricket_id+'</span>');
            } else {
                videoClickEvents['cricketId'] = '';
            }

            id_cricket();
        });
}

function enter_id(t) {
   var id_par = $(t).attr('data-value');
   var value = $(t).text();
   var input = $('#tag_id');

   letters = $('#tag_id').val().length;

    if (letters >= 2) {
        return false;
    } else {
        $(input).val($(input).val() + value);
    }

}

function burrow_event() {
    $(this).off( 'click' );
    $('.info-text').html('Click on the burrow to begin the video.');
    $("#ourvideo").click(function(e) {
    var parentOffset = $(this).parent().offset();
    var burrowX = e.pageX - parentOffset.left;
    var burrowY = e.pageY - parentOffset.top;

    burrowClicked = true;
    pop.play();

    videoClickEvents['burrowXY'] = [burrowX, burrowY];
    $('.info-text').html('Enter the ID of the cricket when or if you see it.');

    $('.id-display').show(); //if ended
    });

}

// make the buttons square
function fixup_buttons() {
    $('.button_container .button ').not('.id-display').each(function() {
        var button_width = $(this).width();
        $(this).height(button_width);
    });
}

function event_button_change(obj, image) {
    obj.style.backgroundImage="url("+image+")";
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

        fixup_buttons();

        videoClickEvents = {'burrowXY' : '', 'cricketStartXY' : '', 'cricketEndXY' : '', 'cricketId' : ''};

        build_id_keyboard();

        pop = Popcorn("#ourvideo");

        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                $('.top_layer').css({'z-index' : '-1', 'display' : 'none'});

                if (cricketFirstClicked === false) {
                    $('.info-text').html('Click on the cricket if you can see it <button id="no_cricket">No Cricket</button>.');
                    $("#ourvideo").click(function(e) {
                        $(this).off( 'click' );
                        var parentOffset = $(this).parent().offset();
                        var cricketStartX = e.pageX - parentOffset.left;
                        var cricketStartY = e.pageY - parentOffset.top;

                        if (noCricket === false){
                            videoClickEvents['cricketStartXY'] = [cricketStartX, cricketStartY];
                            console.log(videoClickEvents['cricketStartXY']);

                        } else {
                            videoClickEvents['cricketStartXY'] = '';
                        }

                        $(this).off('click');

                        burrow_event();
                        });
                };


                    $('#no_cricket').click(function() {
                    console.log('No cricket');
                    $('.info-text').html('Click on the burrow to begin the video.');
                    $(this).off( 'click' );
                    noCricket = true;
                    burrow_event();

                });

                }
        });

        pop.on("ended", function() {


            if (burrowClicked === true) {
                $('.info-text').html('Click on the cricket to finish the video <button id="no_cricket_end">No cricket</button>');
                $('#ourvideo').click(function(e) {
                    $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    pop.currentTime(pop.duration());

                    $(this).off( 'click' );
                    $('.info-text').html('Events Complete');
                    pop.pause();

                    var parentOffset = $(this).parent().offset();
                    var cricketEndX = e.pageX - parentOffset.left;
                    var cricketEndY = e.pageY - parentOffset.top;

                    cricketLastClicked = true;

                    if (noCricketEnd === false) {
                        videoClickEvents['cricketEndXY'] = [cricketEndX, cricketEndY];
                        // $("#cricket_player").append('<div class="click-video-circle" style="width: 100px; height: 100px; border-radius: 50px; background: #717892; position: absolute; opacity: 0.7; display: block; top:'+(cricketEndY)+'px; left:'+(cricketEndX - 50)+'px;"></div>');
                        // $('.click-video-circle').fadeOut();
                    } else {
                        videoClickEvents = '';
                    }
                    $(this).off( 'click' );
                    $("#movie_end").css("visibility", "visible");

                });

            } else if (cricketFirstClicked === false) {
                $('.info-text').html('No cricket clicked [no cricket seen?]');
            }

             $('#no_cricket_end').click(function() {
                    $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    $(this).off( 'click' );
                    $('.info-text').html('Events Complete');
                    noCricketEnd = true;
                    $("#movie_end").css("visibility", "visible");
                    $('#ourvideo').off( 'click' );
            });


            //console.log(videoClickEvents);

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
                //console.log("rendering event...");
                inner_render_event(e[0],e[1]);
            });
        });

    },false);
};

function id_cricket() {

    $('#tag_cricket').toggle();

    if($('#tag_cricket:hidden').length == 0)
        {
            pop.pause();
        } else {
            if (pop.duration() != pop.currentTime()) {
                pop.play();
            }
        }
}



function restart_video() {
    $('#ourvideo').off( 'click' );
    $("#movie_end").css("visibility", "visible");
    pop.currentTime(0);
    pop.pause();
}

function toggle_keyboard() {
    $('#tag_cricket').toggle();
}
// actually render the event
function inner_render_event(type, start_time) {
    // convert time into %
    // var left = (start_time/pop.duration())*100;
    // $("#timeline").append(
    //     '<div class="event micro_circle" style="left:'+left+'%;">\
    //     </div>');
}

// actually render the event
function inner_render_my_event(type, start_time) {
    // convert time into %
    var left = (start_time/pop.duration())*100;
    var cricket_image = Math.floor(Math.random() * 10) + 1;
    $("#timeline").append(
        '<div class="event small_circle" style="left:'+left+'%; margin-top: -1.8em"><img class="cricket-line" src="/media/images/crickets/'+cricket_image+'.png" style="z-index: 2; height: 75px; width:auto"></div>');
    $('.cricket-line').fadeOut('slow');
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
