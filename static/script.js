let myDiagram = null;
function init() {
    const $ = go.GraphObject.make;  // for conciseness in defining templates

    myDiagram = $(go.Diagram, "family-tree-container",  // must name or refer to the DIV HTML element
        {
            layout: $(go.LayeredDigraphLayout,  // use a LayeredDigraphLayout
                { direction: 90, columnSpacing: 30, setsPortSpots: false }),
        });

    // Define a simple node template
    myDiagram.nodeTemplate =
    $(go.Node, "Auto", // Node panel
        { // Outer shape of the node
            selectionObjectName: "PANEL",
            resizable: false, resizeObjectName: "PANEL", // Don't allow users to resize nodes
        },
        $(go.Shape, "Rectangle", // Outer rectangular shape that encapusulates the vertical panel
            { stroke: "gray", strokeWidth: 2}, new go.Binding("fill", "gender", function(gender) {
                if (gender == "Female") {
                    return "pink";
                } else if (gender == 'Male') {
                    return "lightblue";
                } else {
                    return "lightgray";
                }
            })),
        $(go.Panel, "Vertical", // Vertically stacks the inner Picture and TextBlock objects
            {name: "PANEL", margin: 10},
            $(go.Picture,
                {
                    margin: 10,
                    width: 50,
                    height: 50,
                    background: 'white',
                    // Specify the errorFunction for handling image loading errors
                    errorFunction: function(picture, error) {
                        // If there's an error loading the image, set the source to the default kitten image
                        picture.source = 'https://placekitten.com/50/50';
                    }
                },
                new go.Binding("source", "photoUrl", function(url) { 
                    // Return the URL or a default one if the URL is missing or empty
                    return url || 'https://placekitten.com/50/50';
                })
            ),
            $(go.TextBlock,
                {
                    margin: new go.Margin(5, 0),
                    stroke: "black",
                    font: "bold 11px sans-serif",
                    textAlign: "center",
                    wrap: go.TextBlock.WrapFit,
                    maxSize: new go.Size(80, NaN)
                },
                new go.Binding("text", "name")
            )            
        ),
    );

    // Define a simple link template
    myDiagram.linkTemplate =
    $(go.Link,  // Define how links are drawn
        { routing: go.Link.Orthogonal, corner: 5 },
        $(go.Shape,  // This represents the link shape
            { strokeWidth: 2, stroke: "#555" }),
        $(go.Shape,  // This represents the arrowhead at the end of the link
            { toArrow: "Standard", stroke: null, fill: "#555" })
    );

    // Define what happens when a node is clicked
    myDiagram.nodeTemplate.click = function (e, obj) {
        hideCurrNodeDetails();
        const clickedNode = obj.part.data;
        // Show node details
        fetchNodeDetails(clickedNode.key);
    };
    // create the model for the family tree
    fetchFamilyTreeData(myDiagram);
}

function fetchNodeDetails(nodeId) {
    fetch(`/get_node_details/${nodeId}`, {
        method: 'GET',
    })
    .then (response => {
        if (!response.ok) {
            throw new Error("Network response was not ok: ", response.statusText);
        }
        return response.json(); // Parses the JSON in the response
    })
    .then (data => {
        // Handle data from server
        displayNodeDetails(nodeId, data);
    })
    .catch(error => {
        console.error('There is a problem with the fetch operation: ', error);
    })
}

function displayNodeDetails(nodeId, data) {
    const nodeDetails = document.getElementById('node-details');
    const sidebarInstructions = document.getElementById('sidebar-instructions');
    sidebarInstructions.style.display = 'none';
    nodeDetails.style.display = '';
    nodeDetails.innerHTML = "";
    if (data && Object.keys(data).length > 0) {
        const content = `
            <img src="${data.photo_url || 'https://placekitten.com/200/300'}" style="max-width: 300px; max-height: 200px; width: auto;
            height: auto;" onerror="this.onerror=null;this.src='https://placekitten.com/200/300';">
            <p><strong>Name:</strong> ${data.name || 'N/A'}</p>
            <p><strong>Gender:</strong> ${data.gender || 'N/A'}</p>
            <p><strong>Birth Date:</strong> ${data.birth_date || 'N/A'}</p>
            <p><strong>Photo URL:</strong> ${data.photo_url ? `<a href="${data.photo_url}" target="_blank">View Photo</a>` : 'N/A'}</p>
            <button onclick='showEditPersonForm("${nodeId}")'>Edit this person</button>
            <button onclick='showAddRelativeForm("${nodeId}")'>Add a relative</button>
            <button onclick='resetToInstructions()'>Cancel</button>
        `;
        nodeDetails.innerHTML = content;
    } else {
        nodeDetails.innerHTML = '<p> No details available </p>';
    }
}

function showEditPersonForm(nodeId) {
    const form = document.getElementById('edit-person-form');
    form.style.display = 'block';
    const relativeForm = document.getElementById('add-relative-form');
    relativeForm.style.display = 'none';
    // Set the nodeId in a hidden input so you know which node is being added to
    document.getElementById('node-id').value = nodeId;
}
function resetToInstructions() {
    const nodeDetails = document.getElementById('node-details');
    const sidebarInstructions = document.getElementById('sidebar-instructions');
    const relativeForm = document.getElementById('add-relative-form');
    const editPersonForm = document.getElementById('edit-person-form');
    sidebarInstructions.style.display = '';
    nodeDetails.style.display = 'none';
    editPersonForm.style.display = 'none';
    relativeForm.style.display = 'none';
}
function hideCurrNodeDetails() {
    const nodeDetails = document.getElementById('node-details');
    const relativeForm = document.getElementById('add-relative-form');
    const editPersonForm = document.getElementById('edit-person-form');
    nodeDetails.style.display = 'none';
    editPersonForm.style.display = 'none';
    relativeForm.style.display = 'none';
}

// Show the form for adding relatives to a specific node
function showAddRelativeForm(nodeId) {
    // Gets form in HTML with id="relative-form"
    const form = document.getElementById('add-relative-form');
    const editPersonForm = document.getElementById('edit-person-form'); // Hide edit person form
    editPersonForm.style.display = 'none';
    form.style.display = 'block'; // Show the form

    // Set the nodeId in a hidden input so you know which node is being added to
    document.getElementById('node-id').value = nodeId;
}

function setRelationship(relationship, button) {
    // Remove the selected CSS class from all buttons and add to clicked button
    var buttons = document.querySelectorAll('.relationship-button');
    buttons.forEach(function(btn) {
        btn.classList.remove('selected');
    });
    button.classList.add('selected');
    // Set the relationship when Parent or Child button is clicked
    document.getElementById('relationship').value = relationship;
}

function setGender(gender, button) {
    // Remove the selected CSS class from all buttons and add to clicked button
    var buttons = document.querySelectorAll('.gender-button');
    buttons.forEach(function(btn) {
        btn.classList.remove('selected');
    });
    button.classList.add('selected');
    // Set the relationship when Parent or Child button is clicked
    document.getElementById('relative-gender').value = gender;
}

function closeEditNodeForm() {
    document.getElementById('edit-person-form').style.display = 'none';
}

function closeRelativeForm() {
    // Hide the form without submitting
    document.getElementById('add-relative-form').style.display = 'none';
}

document.getElementById('edit-person-form').addEventListener('submit', function(submission){
    submission.preventDefault();
    const nodeId = document.getElementById('node-id').value;
    const newName = document.getElementById('person-name').value;
    const newGender = document.getElementById('person-gender').value;
    const newBirthDate = document.getElementById('person-birth-date').value;
    const newPhotoURL = document.getElementById('person-photo-url').value;

    // Prepare form data
    const formData = {
        name: newName,
        gender: newGender,
        birth_date: newBirthDate,
        photo_url: newPhotoURL
    };
    // Send data to server
    fetch(`/edit_person/${nodeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then (response => response.json())
    .then(data => {
        // Refresh the diagram to show the new person
        fetchFamilyTreeData(myDiagram);
    })
    .catch(error => {
        console.error('Error adding relative:', error);
    });
    event.target.reset();
    closeRelativeForm();
})
// Handle form submission
document.getElementById('add-relative-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const nodeId = document.getElementById('node-id').value;
    const name = document.getElementById('relative-name').value;
    const gender = document.getElementById('relative-gender').value;
    const birthDate = document.getElementById('relative-birth-date').value;
    const photoUrl = document.getElementById('relative-photo-url').value;
    const relationship = document.getElementById('relationship').value;

    // Prepare the data to send to the server
    const formData = {
        name: name,
        gender: gender,
        birth_date: birthDate,
        photo_url: photoUrl,
        relationship: relationship,
    };
    // Send the data to the server
    fetch(`/add_relative/${nodeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        console.log("data message is ", data.message);
        // Refresh the diagram to show the new relative
        fetchFamilyTreeData(myDiagram);
    })
    .catch(error => {
        console.error('Error adding relative:', error);
    });
    event.target.reset();
    closeRelativeForm();
});

//called by init(), initializes the GoJS diagram
function fetchFamilyTreeData(myDiagram) {
    fetch('/get_family_trees')
        .then(response => response.json())
        .then(data => {
            // Transform data to include nodes and link data for GraphLinksModel
            const nodeDataArray = data.map(node => ({
                key: node.id,
                name: node.name,
                gender: node.gender,
                birthDate: node.birth_date,
                photoUrl: node.photo_url
            }));

            const linkDataArray = data.flatMap(node => {
                const links = [];
                if (node.father_id !== null) {
                    links.push({ from: node.father_id, to: node.id });
                }
                if (node.mother_id !== null) {
                    links.push({ from: node.mother_id, to: node.id });
                }
                return links;
            });

            console.log("node data is ", nodeDataArray);
            console.log("link data is ", linkDataArray);

            myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
        });
}
// start everything once the DOM is loaded
document.addEventListener("DOMContentLoaded", init);