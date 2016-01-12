function setup_gallery() {

    var find_closest = function(pos,list) {
        var closest=99999;
        var index=0;
        var count=0;
        list.forEach(function(lpos) {
            if (Math.abs(lpos-pos)<closest) {
                closest=lpos-pos;
                index=count;
            }
            count++;
        });

        if (index==list.length-1) index--;
        return index;
    };

    var image_positions=[0];
    var current_pos=0;
    var last_x=0;
    var auto_scroll=true;
    var disabled=false;

    // set up the arrow buttons
    $(".arrow-left").click(function() { auto_scroll=false; scroll_left(); });
    $(".arrow-right").click(function() { auto_scroll=false; scroll_right(); });

    $(".arrow-left").hover(function () {
        $(this).attr("src", "../media/images/arrow-left.png");
    }, function () {
        $(this).attr("src", "../media/images/arrow-left-t.png");
    });

    $(".arrow-right").hover(function () {
        $(this).attr("src", "../media/images/arrow-right.png");
    }, function () {
        $(this).attr("src", "../media/images/arrow-right-t.png");
    });

    $(".arrow-left").hide();

    var image_width = $(".gallery").innerWidth();
    var image_height = $(".gallery").innerHeight();

    var reset_sizes = function() {
        image_height = $(".gallery").innerHeight();
        image_width = $(".gallery").innerWidth();
        image_positions = [0];
        current_pos=0;

        // get the positions of all the images
        $(".slider-items").children().each(function(t,v) {
            // need to set the width here, can't do it automatically
            // todo: update this all the time
            $(this).height(image_height);
            $(this).width(image_width);
            $(this).css({left:current_pos});
            current_pos+=image_width;
            image_positions.push(-current_pos);
        });

        $('.slider-items').css({
            left: ""+image_positions[current_image]+"px", top: "0px"
        });

    };

    reset_sizes();
    $(window).resize(reset_sizes);

    // only one image, disable everything
    if (image_positions.length==2) {
        disabled=true;
        $(".arrow-left").hide();
        $(".arrow-right").hide();
    }

    // deal with the dragging
    var up = function(event) {
        auto_scroll=false;
        last_x=event.clientX;
    };

    $('.slider-items').mousedown(up);
    $('.slider-items').mouseout(up);

    $('.slider-items').mouseup(function(event) {
        var cur = parseInt($(this).css("left"), 10);
        var pos = cur+(event.clientX-last_x);

        $('.slider-items').animate({
            left: ""+image_positions[find_closest(pos,image_positions)]+"px"
        });
    });

    $('.slider-items').bind('drag',function(event){
        if (!disabled) {
            var cur = parseInt($(this).css("left"), 10);
            var pos = cur+(event.clientX-last_x);
            $(this).css({
                left: pos
            });
            last_x = event.clientX;
        }
    });

    var current_image=0;

    var scroll_right = function() {
        current_image++;
        scroll();
    };

    var scroll_left = function() {
        current_image--;
        scroll();
    };

    var scroll = function() {
        if (current_image>image_positions.length-2) current_image=0;
        $('.slider-items').animate({
            left: ""+image_positions[current_image]+"px", top: "0px"
        });

        $(".arrow-left").show();
        $(".arrow-right").show();

        if (current_image==0) {
            $(".arrow-left").hide();
        }
        if (current_image==image_positions.length-2) {
            $(".arrow-right").hide();
        }
    };

};
