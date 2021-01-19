/* League table variables */
var tab = $('#leagueTab tr'); // Grab the leage table
var n = $('#leagueTab >tbody >tr').length; // Find table length so we can loop through

//Test loop
$(document).ready(function(){
    $('table.rep').each(function(){
        $(this).find('tr').each(function(){
            console.log("hi");
        });
    });
});

// Loop through the table and set the images
for (var i = 1; i <= n; ++i) {
    var str = tab.eq(i).find('td').eq(0).text();
    var ele = tab.eq(i).find('td').eq(0);
    str = str.trim();
    var src1 = "<source media=\"(min-width:1024px)\" srcset=\"https://static.www.nfl.com/t_q-best/league/api/clubs/logos/\">"
    var src2 = "<source media=\"(min-width:768px)\" srcset=\"https://static.www.nfl.com/t_q-best/league/api/clubs/logos/\">"
    var src3 = "<source srcset=\"https://static.www.nfl.com/t_q-best/league/api/clubs/logos/\">"
    var img = "<img alt=\"TEMP logo\" class=\"img-fluid\" src=\"https://static.www.nfl.com/t_q-best/league/api/clubs/logos/\">"
    if (str === "HST") {
        var src1_n = src1.replace("/logos/", "/logos/"+"HOU");
        var src2_n = src2.replace("/logos/", "/logos/"+"HOU");
        var src3_n = src3.replace("/logos/","/logos/"+"HOU");
        var img_n = img.replace("/logos/","/logos/"+"HOU");
        img_n = img.replace("TEMP", "HOU");
    }
    else if (str === "OAK") {
        var src1_n = src1.replace("/logos/", "/logos/"+"LV");
        var src2_n = src2.replace("/logos/", "/logos/"+"LV");
        var src3_n = src3.replace("/logos/","/logos/"+"LV");
        var img_n = img.replace("/logos/","/logos/"+"LV");
        img_n = img.replace("TEMP", "OAK");
    }
    else if (str === "SL") {
        var src1_n = "<source media=\"(min-width:1024px)\" srcset=\"https://assets.stickpng.com/thumbs/580b585b2edbce24c47b2b5b.png\">";
        var src2_n = "<source media=\"(min-width:768px)\" srcset=\"https://assets.stickpng.com/thumbs/580b585b2edbce24c47b2b5b.png\">"
        var src3_n = "<source srcset=\"https://assets.stickpng.com/thumbs/580b585b2edbce24c47b2b5b.png\">"
        var img_n = "<img alt=\"SL logo\" class=\"img-fluid\" src=\"https://assets.stickpng.com/thumbs/580b585b2edbce24c47b2b5b.png\">"
    }
    else if (str === "SD") {
        var src1_n = "<source media=\"(min-width:1024px)\" srcset=\"https://sportslogohistory.com/wp-content/uploads/2017/12/los_angeles_chargers_2017-pres.png\">";
        var src2_n = "<source media=\"(min-width:768px)\" srcset=\"https://sportslogohistory.com/wp-content/uploads/2017/12/los_angeles_chargers_2017-pres.png\">"
        var src3_n = "<source srcset=\"https://sportslogohistory.com/wp-content/uploads/2017/12/los_angeles_chargers_2017-pres.png\">"
        var img_n = "<img alt=\"SL logo\" class=\"img-fluid\" src=\"https://sportslogohistory.com/wp-content/uploads/2017/12/los_angeles_chargers_2017-pres.png\">"
    }
    else {
        var src1_n = src1.replace("/logos/", "/logos/"+str);
        var src2_n = src2.replace("/logos/", "/logos/"+str);
        var src3_n = src3.replace("/logos/","/logos/"+str);
        var img_n = img.replace("/logos/","/logos/"+str);
        img_n = img.replace("TEMP", str);
    }
    ele.prepend("<picture>"+src1_n+src2_n+src3_n+img_n+"</picture>");
}    
