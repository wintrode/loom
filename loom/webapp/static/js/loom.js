
function toggle_element(element_id) {
  var x = document.getElementById(element_id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function update_node(uid, type, node) {
    console.log("Updating", uid, node);
    // Creating a XHR object 
    let xhr = new XMLHttpRequest(); 
    let host = window.location.host;
    host = host.match(/^[\d\w]+/);    
    // open a connection
    let url = "/"
    if (type == "Goal") {
	url = "/goal/" + uid
    }
    else {
	url = "/task/" + uid
    }
    
    xhr.open("POST", url, true); 
  
    // Set the request header i.e. which type of content you are sending 
    xhr.setRequestHeader("Content-Type", "application/json"); 
  
    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 
	    
            // Print received data from server 
            console.log(this.responseText); 
	    
        } 
    }; 
  
    // Converting JSON data to string
    //var node = { "idx" : uid}
    //node[field]= value;
    var data = JSON.stringify(node)
    
    // Sending data with the request 
    xhr.send(data);  
}

function get_node(uid, type, my_callback) {
    console.log("Loading", uid);
    // Creating a XHR object 
    let xhr = new XMLHttpRequest(); 
    let host = window.location.host;
    host = host.match(/^[\d\w]+/);    
    // open a connection
    let url = "/"
    if (type == "Goal") {
	url = "/goal/" + uid
    }
    else {
	url = "/task/" + uid
    }

    console.log("Getting", url);
  
    // Create a state change callback 
    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {
	    console.log("RESP", this.responseText);
	    var myNode = JSON.parse(this.responseText);	    
            // Print received data from server 
            console.log("NODE", myNode); 
	    //return myNode;
	    my_callback(myNode);
        }
	else if (xhr.readyState === 4 && xhr.status != 200 ) {
	    //
	    console.log("Error", xhr.status);
	    my_callback(null);
	    // show error message?
	}
    }; 

    xhr.open("GET", url, true);
    xhr.send(null);
    console.log("Done");
    
}


function type_selected() {
    
    var cb = document.getElementById("typeSelect");
    var due = document.getElementById("due_date");
    console.log("selected " + cb.value)
    if (cb.value == "Idea") {
	due.style.display="none";
    }
    else  {
	due.style.display="inline";
    }
}

function mark_complete(ttype, idx) {
    tl = ttype.toLowerCase()
    var cb = document.getElementById(tl +"-done-"+idx);
    
    var x = document.getElementById(tl + "-row-"+idx);
    if (cb.checked) {
	x.className = "taskcomplete";
    }
    else {
	x.className = "none";
    }

    var id = document.getElementById(tl +"-id-"+idx);
    if (id) {
	node = {"complete" : cb.checked};
	update_node(id.value,  ttype, node);
    }
}

function close_window() {

    var modal = document.getElementById("edit_model");
    modal.style.display = "none";
}
    
function edit_node(uid, ttype) {
    // Get the modal
    console.log ("Edit clicked", uid);
    
    var modal = document.getElementById("edit_model");
    var content = document.getElementById("edit_content");

    var sidebar = document.getElementById("mysidebar");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    var sbwidth = sidebar.offsetWidth
    sidebar = document.getElementById("mymain");
    
    modal.style.display = "block";
    content.style.left=sbwidth/2;
    content.style.width=sidebar.offsetWidth * 0.8;
    if (content.style.width > 480) {
	content.style.width="480px";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
	if (event.target == modal) {
	    modal.style.display = "none";
	}
    }    

    //  now load data
    var node = get_node(uid, ttype, function (node) {

	console.log("Got", node);

	if (node == null) {
	    close_window();
	    return;
	}
	
	var input = document.getElementById("edit_title");
	input.value = node.title;
	input = document.getElementById("edit_desc");
	input.value = node.description;
	input = document.getElementById("edit_due_date");
	console.log(node.due_date);
	if (node.due_date != null && node.due_date.length > 0) {
	    input.value = node.due_date.substr(0,10);
	}
	input = document.getElementById("edit_uid");
	input.value=uid;

    });


    
    
}

function update_node_form() {
    var input = document.getElementById("edit_uid");
    var node = {};
    var uid = input.value;
    input = document.getElementById("edit_ttype");
    var ttype = input.value;
	
    input = document.getElementById("edit_title");
    node['title'] = input.value;
    input = document.getElementById("edit_desc");
    node['description'] = input.value;
    input = document.getElementById("edit_due_date");

    if (input.value != null && input.value.length.length > 0) {
	node['due_date'] = input.value + " 00:00:00.000000";
    }

    console.log("Updating", uid, ttype, node);
    update_node(uid, ttype, node);

    close_window();
    
}
