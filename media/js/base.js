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



// jquery doesn't seem to work from onclick events!?
function make_visible(id,viz) {
    var t = document.getElementById(id);
    if (viz) {
        t.style.border = "3px dotted green";
        t.style.background = "white";
    } else {
        t.style.border = "0px solid";
        t.style.background = "none";
    }
}



function switch_tutorial(from,to) {
    var t = document.getElementById(from);
    t.style.display = "none";
    t = document.getElementById(to);
    t.style.display = "block";

    make_visible("behaviour-buttongroup",false);
    make_visible("FEED-buttongroup",false);
    make_visible("LEAVES FRAME-buttongroup",false);
    make_visible("id-buttongroup",false);

    if (to=="tut-1") make_visible("behaviour-buttongroup",true);
    if (to=="tut-2") make_visible("FEED-buttongroup",true);
    if (to=="tut-3") make_visible("LEAVES FRAME-buttongroup",true);
    if (to=="tut-4") make_visible("id-buttongroup",true);
    if (to=="tut-5") {
        var t = document.getElementById("tutorial-buttons");
       // t.style.display = "none";
    }

    // Checking if slide is tut-5, handle visibility of buttons
    if (to === "tut-5") {
        $('#tutorial-buttons').css({
            'display' : 'none'
        });
    } else {
        $('#tutorial-buttons').css({
            'display' : 'block'
        });
    }

    if (to=="tut-1") {
        // need to build the carousel here
        // as the element is display:none at load time
        // so does not calculate properly
        $('#slider-tutorial').slick({
            infinite: false,
            arrows: true,
            prevArrow: $('.arrow-tut-left'),
            nextArrow: $('.arrow-tut-right')
        });
    }
}


function tut_video_right() {
    var t = document.getElementById("tut_video_scroll");
    t.style.left=-100;

}


// video/tagging business
var pop = false;
var events = [];

function build_id_keyboard(cricket_id_id,something_else_id, movie_id,user_id) {

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
    initialise_operators_keyboard(cricket_id_id,something_else_id, movie_id,user_id);
}


function initialise_operators_keyboard(cricket_id_id, something_else_id, movie_id,user_id) {
        $("#delete").click(function (){
            $('#tag_id').val('');
        });

        $("#save").click(function (){
            cricket_id = $('#tag_id').val();
            if (cricket_id.length == 2) {
                add_event(cricket_id_id,movie_id,user_id, null, null, cricket_id);
                $('p.cricket-id-display').html('ID: <span class="cricket-id-char">'+cricket_id+'</span>');
            }

            toggle_id_cricket();
        });

        $('.save_something').click(function() {
            string = $('#something_else_input').val();
            add_event(something_else_id,movie_id,user_id, null, null, string);
            close_something_else();
        });

        $('.closed').click(function() {
            close_something_else();
        });

        $('.close_id').click(function() {
            close_id();
        });

        $('.close_id_no_tag').click(function() {
            add_event(cricket_id_id,movie_id,user_id, null, null, "No Tag");
            close_id_no_tag();
        });

}

function close_something_else() {
    $('#something_else').hide();
}

function close_id() {
    $('#tag_cricket').hide();
}

function close_id_no_tag() {
    $('#tag_cricket').hide();
    $('p.cricket-id-display').html('ID: <span class="cricket-id-char">'+'--'+'</span>');
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
        return true;
    }
}

function update_infotext() {
    // need to make the font smaller than the usual to fit anything in
    $('.page_title').css("font-size","120%");
    switch(state) {
        case "wait-cricket":
            $('.page_title').html('1. XX Click on the cricket if you can see it, or click <button id="no_cricket">No Cricket</button>');
            break;
        case "wait-burrow":
            $('.page_title').html('2. Click on the middle of the burrow to begin the video');
            break;
        case "movie-playing":
            $('.page_title').html('3. Tag cricket behaviours and ID as the video plays');
            break;
        case "wait-cricket-end":
            $('.page_title').html('4. Click on the cricket to finish the video, or click <button id="no_cricket_end">No cricket</button>');
            break;
        case "movie-end":
            $('.page_title').html('Well done! Video complete');
            break;
        // whyyy
        case "no-cricket-end":
            $('.page_title').html('No cricket clicked [no cricket seen?]');
            break;
        default:
            $('.page_title').html('I have no idea, you broke me');

    }
}


function burrow_event(burrow_start_id,movie_id,user_id) {
    console.log(state);
    update_infotext();
    $("#ourvideo").click(function(e) {
        state = 'movie-playing';
        pop.play();
        var burrowPercent = mouse_pos(e, this);
        add_event(burrow_start_id,movie_id,user_id, burrowPercent['x'], burrowPercent['y'], null);
        update_infotext();
        $(this).off('click');
    });

}

function event_button_change(obj, image) {
    obj.style.backgroundImage="url("+image+")";
}

function percentage(x, y) {
    var container_w = $('#ourvideo').width();
    var container_h = $('#ourvideo').height();

    var percent_x = (x / container_w) * 100;
    var percent_y = (y / container_h) * 100;

    return {'x' : percent_x, 'y' : percent_y};
}

function mouse_pos(e, context) {
    var parentOffset = $(context).parent().offset();
    return percentage(e.pageX - parentOffset.left, e.pageY - parentOffset.top);
}

function video_setup(cricket_start_id, burrow_start_id, cricket_id_id, cricket_end_id, something_else_id, movie_id, user_id) {
    // Create a popcorn instance by calling Popcorn("#id-of-my-video")
    document.addEventListener("DOMContentLoaded", function () {

        state = "wait-cricket";

        build_id_keyboard(cricket_id_id,something_else_id, movie_id,user_id);

        pop = Popcorn("#ourvideo");

        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                $('.top_layer').css({'z-index' : '-1', 'display' : 'none'});

                update_infotext();

                $("#ourvideo").click(function(e) {
                    var cricketStartPercent = mouse_pos(e, this);
                    add_event(cricket_start_id,movie_id,user_id, cricketStartPercent['x'], cricketStartPercent['y'], null);
                    state = "wait-burrow";
                    $(this).off('click');
                    burrow_event(burrow_start_id,movie_id,user_id);
                });


                $('#no_cricket').click(function() {
                    add_event(cricket_start_id,movie_id,user_id, 0, 0, 'No Cricket');
                    state = "wait-burrow";
                    burrow_event(burrow_start_id,movie_id,user_id);
                });

            }

        });

        pop.on("ended", function() {

            if (state === "movie-playing") {
                state = "wait-cricket-end";
                update_infotext();


                $('#ourvideo').click(function(e) {
                   $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    pop.currentTime(pop.duration());
                    state = "movie-end";
                    update_infotext();
                    pop.pause();
                    var pos = mouse_pos(e, this);
                    add_event(cricket_end_id,movie_id,user_id, pos['x'], pos['y'], null);
                    $("#movie_end").css("visibility", "visible");
                    $(this).off('click');
                });

                $('#no_cricket_end').click(function() {
                    add_event(cricket_end_id,movie_id,user_id, 0, 0, 'No Cricket');
                    $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    update_infotext();
                    $("#movie_end").css("visibility", "visible");
                });
            }

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
            $("#time").css({left: percentage*0.9505+"%"});

        });


        pop.on("loadeddata", function () {
            // go through the events we collected earlier...
            events.forEach(function(e) {
                //console.log("rendering event...");
                inner_render_event(e[0],e[1]);
            });
        });

        pop.play();
//        pop.pause();

    },false);
};

function toggle_id_cricket() {
    $('#tag_cricket').toggle();
    if($('#tag_cricket:hidden').length == 0) {
            pop.pause();
        } else {
            if (state === "movie-playing") {
                pop.play();
            }
        }
}

function toggle_something_else() {
    $('#something_else').toggle();
    if($('#something_else:hidden').length == 0) {
            pop.pause();
        } else {
            if (state === "movie-playing") {
                pop.play();
            }
        }
}



function restart_video() {
    state = 'wait-cricket';
    console.log(state);
    $("#movie_end").css("visibility", "hidden");
    pop.currentTime(0);
    pop.pause();
}

function toggle_keyboard() {
    $('#tag_cricket').toggle();
}

function pause_movie() {
    if (state === 'movie-playing') {
        pop.pause();
    }
}

function play_movie() {
    if (state === 'movie-playing') {
        pop.play();
    }
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
function add_event(event_type_id, movie_id,user_id, xpos, ypos, other) {
    // only works if we have a video running of course...
    if (pop!=false) {
        t = pop.currentTime();

        // todo: user_id now comes in as -1 if the player is anonymous
        // not sure what circumstances it can be None now

        // save to django ->
        if (user_id=="None") {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_type_id,
                user: "",
                start_time: t,
                end_time: t+1,
                x_pos : xpos,
                y_pos: ypos,
                other: other
            });
        } else {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_type_id,
                user: parseInt(user_id),
                start_time: t,
                end_time: t+1,
                x_pos : xpos,
                y_pos: ypos,
                other: other
            });
        }
    }

}

// house helpers

function image_from_house(house) {
    if (house=='' || house=="0") {
        var random_file_no = Math.floor(Math.random() * (7 - 1 + 1)) + 1;
        return 'images/burrows/burrow-'+random_file_no+'.png';
    } else {
        return 'images/houses/built/'+house+'.png';
    }
}

function size_from_house(house,zoom) {
    var zooms = [[5,   3.3335],
                 [10,  6.667],
                 [20,  13.334],
                 [30,  20],
                 [70,  46.669],
                 [125, 83.3375]];

    if (house=='' || house=="0") {
        return zooms[zoom-1];
    } else {
        ret = zooms[zoom-1];
        ret[0]*=2;
        ret[1]*=5;
        return ret;
    }
}
