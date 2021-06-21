var count = 0;
function goal(){
    $("#page_01_goal").show();
}

function why(){
    $("#page_01_why").show();
}

function how(){
    $("#page_01_how").show();
}

$("#page_01_goal").click(function(){
    $("#page_01_goal").hide();
})

$("#page_01_why").click(function(){
    $("#page_01_why").hide();
})

$("#page_01_how").click(function(){
    $("#page_01_how").hide();
})

function photo1(){
    $("#page_02_01").show();
}

function photo2(){
    $("#page_02_02").show();
}

function photo3(){
    $("#page_03_01").show();
}

function photo4(){
    $("#page_03_02").show();
}

function photo5(){
    $("#page_04_01").show();
}

function photo6(){
    $("#page_04_02").show();
}

function photo7(){
    $("#page_05_01").show();
}

$("#page_02_01").click(function(){
    $("#page_02_01").hide();
})

$("#page_02_02").click(function(){
    $("#page_02_02").hide();
})

$("#page_03_01").click(function(){
    $("#page_03_01").hide();
})

$("#page_03_02").click(function(){
    $("#page_03_02").hide();
})

$("#page_04_01").click(function(){
    $("#page_04_01").hide();
})

$("#page_04_02").click(function(){
    $("#page_04_02").hide();
})

$("#page_05_01").click(function(){
    $("#page_05_01").hide();
})


function next(){
	$("#page_01_goal").hide();
	$("#page_01_why").hide();
	$("#page_01_how").hide();
	$("#page_02_01").hide();
	$("#page_02_02").hide();
	$("#page_03_01").hide();
	$("#page_03_02").hide();
	$("#page_04_01").hide();
	$("#page_04_02").hide();
	$("#page_05_01").hide();
    switch(count){
        case 0:
            $("#first").show();
            $("#previous").show();
            $("#page_01").show();
            document.getElementById("cover").style.backgroundImage = 'url("static/src/inner_page.png")';
            document.getElementById("page_number").innerHTML = '01';
            count += 1;
            break;
        
        case 1:
            $("#first").show();
            $("#page_01").hide();
            $("#page_02").show();
            document.getElementById("page_number").innerHTML = '02';
            count += 1;
            break;
        
        case 2:
            $("#first").show();
            $("#page_02").hide();
            $("#page_03").show();
            document.getElementById("page_number").innerHTML = '03';
            count += 1;
            break;

        case 3:
            $("#first").show();
            $("#page_03").hide();
            $("#page_04").show();
            document.getElementById("page_number").innerHTML = '04';
            count += 1;
            break;
        
        case 4:
            $("#first").show();
            $("#page_04").hide();
            $("#page_05").show();
            document.getElementById("page_number").innerHTML = '05';
            count += 1;
            break;

        case 5:
            $("#first").show();
            $("#page_05").hide();
            $("#page_06").show();
            document.getElementById("page_number").innerHTML = '06';
            count += 1;
            break;

        case 6:
            $("#next").hide();
            $("#first").show();
            $("#last").hide();
            $("#page_06").hide();
            $("#page_07").show();
            document.getElementById("cover").style.backgroundImage = 'url("static/src/back.png")';
            document.getElementById("page_number").innerHTML = '07';
            count += 1;
            break;
    }
}


function previous(){
	$("#page_01_goal").hide();
	$("#page_01_why").hide();
	$("#page_01_how").hide();
	$("#page_02_01").hide();
	$("#page_02_02").hide();
	$("#page_03_01").hide();
	$("#page_03_02").hide();
	$("#page_04_01").hide();
	$("#page_04_02").hide();
	$("#page_05_01").hide();
    switch(count){
        case 1:
            $("#first").hide();
            $("#previous").hide();
            $("#page_01").hide();
            document.getElementById("cover").style.backgroundImage = 'url("static/src/cover.png")';
            document.getElementById("page_number").innerHTML = '00';
            count -= 1;
            break;
        
        case 2:
            $("#page_01").show();
            $("#page_02").hide();
            document.getElementById("page_number").innerHTML = '01';
            count -= 1;
            break;
        
        case 3:
            $("#page_02").show();
            $("#page_03").hide();
            document.getElementById("page_number").innerHTML = '02';
            count -= 1;
            break;

        case 4:
            $("#page_03").show();
            $("#page_04").hide();
            document.getElementById("page_number").innerHTML = '03';
            count -= 1;
            break;
        
        case 5:
            $("#page_04").show();
            $("#page_05").hide();
            document.getElementById("page_number").innerHTML = '04';
            count -= 1;
            break;

        case 6:
            $("#page_05").show();
            $("#page_06").hide();
            document.getElementById("page_number").innerHTML = '05';
            count -= 1;
            break;

        case 7:
            $("#next").show();
            $("#last").show();
            $("#page_06").show();
            $("#page_07").hide();
            document.getElementById("cover").style.backgroundImage = 'url("static/src/inner_page.png")';
            document.getElementById("page_number").innerHTML = '06';
            count -= 1;
            break;
    }
}

function first(){
	$("#page_01_goal").hide();
	$("#page_01_why").hide();
	$("#page_01_how").hide();
	$("#page_02_01").hide();
	$("#page_02_02").hide();
	$("#page_03_01").hide();
	$("#page_03_02").hide();
	$("#page_04_01").hide();
	$("#page_04_02").hide();
	$("#page_05_01").hide();
	
    $("#first").hide();
    $("#last").show();
    $("#previous").hide();
    $("#next").show();
    $("#page_01").hide();
    $("#page_02").hide();
    $("#page_03").hide();
    $("#page_04").hide();
    $("#page_05").hide();
    $("#page_06").hide();
    $("#page_07").hide();
    document.getElementById("cover").style.backgroundImage = 'url("static/src/cover.png")';
    document.getElementById("page_number").innerHTML = '00';
    count = 0;
}

function last(){
	$("#page_01_goal").hide();
	$("#page_01_why").hide();
	$("#page_01_how").hide();
	$("#page_02_01").hide();
	$("#page_02_02").hide();
	$("#page_03_01").hide();
	$("#page_03_02").hide();
	$("#page_04_01").hide();
	$("#page_04_02").hide();
	$("#page_05_01").hide();
	
    $("#previous").show();
    $("#next").hide();
    $("#first").show();
    $("#last").hide();
    $("#page_01").hide();
    $("#page_02").hide();
    $("#page_03").hide();
    $("#page_04").hide();
    $("#page_05").hide();
    $("#page_06").hide();
    $("#page_07").show();
    document.getElementById("cover").style.backgroundImage = 'url("static/src/back.png")';
    document.getElementById("page_number").innerHTML = '07';
    count = 7;
}

function table(){
    window.location.href = "/main?account=" + window.location.href.split('?')[1].split('=')[1];
}