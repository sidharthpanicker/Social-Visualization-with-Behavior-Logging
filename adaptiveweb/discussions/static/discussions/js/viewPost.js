console.log('executing viewPost.js file')
//var csvFile;
//groupMouseClicksAndSendJson();

var date = new Date();
var timestamp = date.getTime();
var csrf;
var dictJson = {}
var mouseClickArray = []
var scrollArray = []

function setcsrf(csr){
	csrf = csr
}

function hideUnhide(id) {
	console.log('hideUnhide called'+id)
	var x = document.getElementById(id);
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

function captureMouseMoments(e) {
	var x = e.clientX;
	var y = e.clientY;
	//var coor = "(" + x + "," + y + ")";
    var coor = {x:x,y:y};
	dictJson = {coordinates:coor,timestamp:String(new Date().getTime())}
	if(mouseClickArray.length<100){
		mouseClickArray.push(dictJson);
	}else{
		sendMouseData(mouseClickArray)
		mouseClickArray = [];
	}
}

function sendMouseData(dictJson){
	const url1 = 'http://127.0.0.1:8000/discussions/saveMouseMovements'
	$.ajax({
		type: "POST",
		url: url1,
		data: {
			mousemovements: JSON.stringify(dictJson),
			csrfmiddlewaretoken: csrf
		},
		success: function() {
			console.log("Success")
		}
	})
}

function getMouseData(){
	console.log('Sending getmouse data')
	const url1 = 'http://127.0.0.1:8000/discussions/getMouseMovements'
	$.ajax({
		type: "GET",
		url: url1,
		data: {
			csrfmiddlewaretoken: csrf
		},
		success:function(result){
			mp = JSON.parse(result)
			generateHeapMap(mp)
			//console.log(mp)
		},
		error:function(result){
			console.log(result)
		}
	})
}

function groupMouseClicksAndSendJson(){
	const url1 = 'http://127.0.0.1:8000/discussions/groupMouseClicksAndSendJson'
	$.ajax({
		type: "GET",
		url: url1,
		data: {
			csrfmiddlewaretoken: csrf
		},
		success:function(result){
			csvFile = result
			console.log(result)
		},
		error:function(result){
			console.log(result)
		}
	})
}

function getGeneralClickCount(){
	console.log('Sending getmouse data')
	const url1 = 'http://127.0.0.1:8000/discussions/getGeneralClickCount'
	$.ajax({
		type: "GET",
		url: url1,
		data: {
			csrfmiddlewaretoken: csrf
		},
		success:function(result){
			mp = JSON.parse(result)
			//console.log(mp)
			return mp;
		},
		error:function(result){
			console.log(result)
		}
	})
}


function amountscrolled(){
	var winheight = $(window).height()
	var docheight = $(document).height()
	var scrollTop = $(window).scrollTop()
	var trackLength = docheight - winheight
    var pctScrolled = Math.floor(scrollTop/trackLength * 100) // gets percentage scrolled (ie: 80 NaN if tracklength == 0)
    //console.log(pctScrolled + '% scrolled')
    dictJson = {scrolled:pctScrolled,timestamp:String(new Date().getTime())}
    if(scrollArray.length<10){
    	scrollArray.push(dictJson);
    }else{
    	sendMouseScroll(mouseClickArray)
    	scrollArray = [];
    }
}

function sendMouseScroll(dictJson){
	const url1 = 'http://127.0.0.1:8000/discussions/saveMouseScrolls'
	$.ajax({
		type: "POST",
		url: url1,
		data: {
			mousescrolls: JSON.stringify(dictJson),
			csrfmiddlewaretoken: csrf
		},
		success: function() {
			console.log("Success")
		}
	})
}

function onClickFunction(typeofaction,id){
	dictJson = {type:typeofaction,postId:id,timestamp:String(new Date().getTime())}
	sendMouseClick(dictJson)
}

function sendMouseClick(dictJson){
	const url1 = 'http://127.0.0.1:8000/discussions/saveMouseClicks'
	$.ajax({
		type: "POST",
		url: url1,
		data: {
			mouseclicks: JSON.stringify(dictJson),
			csrfmiddlewaretoken: csrf
		},
		success: function() {
			console.log("Success")
		}
	})
}

function generateHeapMap(cordinates){
	console.log("generateHeapMap");
	// minimal heatmap instance configuration
	var heatmapInstance = heatmap = window.h337.create(
	{
		"container": document.getElementById("heatmapArea"),
		"element": document.getElementById("heatmapArea"),
		"radius" : 11,
		"opacity": 40,
		"visible": true,
		"gradient" : { 0.45: "rgb(0,0,255)", 0.55: "rgb(0,255,255)", 0.65: "rgb(0,255,0)", 0.95: "yellow", 1: "rgb(255,0,0)"}
	});

// now generate some random data
var points = [];
var max = 0;
var width = 1050;
var height = 700;

//tmp = JSON.parse(cordinates)


/*while (len--) {
	var val = Math.floor(Math.random()*100);
	max = Math.max(max, val);
	var point = {
		x: Math.floor(Math.random()*width),
		y: Math.floor(Math.random()*height),
		value: val
	};
	points.push(point);
}
*/
var len = Object.keys(cordinates).length;
console.log(len);

var i;
for (i = 0; i < len; i++) { 
	var point = {
		x: cordinates[i]["coordinates"]["x"],
		y: cordinates[i]["coordinates"]["y"],
		value: 1
	};
	//var x = cordinates[i]["coordinates"]["x"]
	//var y = cordinates[i]["coordinates"]["x"]
	points.push(point);
}
//console.log(points)
// heatmap data format
var data = { 
	max: 1, 
	data: points 
};
// if you have a set of datapoints always use setData instead of addData
// for data initialization
heatmapInstance.setData(data);
}




$(window).on("scroll", function(){
	amountscrolled()
})