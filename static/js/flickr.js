$(document).ready(function() {
       $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?id=47421840@N06&format=json&jsoncallback=?", function(data) {
               var target = "#latest-flickr-images ul"; // Where is it going?
               for (i = 0; i <= 9; i = i + 1) { // Loop through the 10 most recent, [0-9]
                       var pic = data.items[i];
                       var liNumber = i + 1; // Add class to each LI (1-10)
                       $(target).append("<li class='flickr-image no-" + liNumber + "'><a title='" + pic.title + "' href='" + pic.link + "'><img src='" + pic.media.m + "' /></a></li>");
               }
       });
});