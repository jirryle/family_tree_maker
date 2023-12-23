function init() {
    const $ = go.GraphObject.make;  // for conciseness in defining templates

    const myDiagram = $(go.Diagram, "family-tree-container",  // must name or refer to the DIV HTML element
        {
            // configure the diagram layout
            layout: $(go.TreeLayout, { angle: 90, layerSpacing: 35 }),
        });

    // Define a simple node template
    myDiagram.nodeTemplate =
    $(go.Node, "Spot",  // Use Spot Panel for more control over positioning
        // define the node's outer shape, which will surround the TextBlock
        $(go.Shape, "Rectangle", 
            { fill: "lightblue", stroke: null, width: 100, height: 40 }), // Specify shape size
        $(go.TextBlock,
            { 
              alignment: go.Spot.Center, // Center the text
              stroke: "black", 
              font: "bold 14px sans-serif" 
            },
            new go.Binding("text", "name"))
    );

    // Define what happens when a node is clicked
    myDiagram.nodeTemplate.click = function(e, obj) {
        const clickedNode = obj.part.data;
        // Show form for adding relatives
        showAddRelativeForm(clickedNode.key);
    };

    // Set up a Part as a legend, and place it directly on the diagram
    myDiagram.add(
        $(go.Part, "Table",
            { position: new go.Point(300, 10), selectable: false },
            $(go.TextBlock, "Legend",
                { row: 0, font: "bold 16px sans-serif" })
            // add additional text blocks for legend here
        ));
    // create the model for the family tree
    fetchFamilyTreeData(myDiagram);
}

// Show the form for adding relatives to a specific node
function showAddRelativeForm(nodeId) {
    // Assuming you have a form in your HTML with id="relative-form"
    const form = document.getElementById('add-relative-form');
    form.style.display = 'block'; // Show the form

    // Set the nodeId in a hidden input so you know which node is being added to
    document.getElementById('node-id').value = nodeId;
}

function setRelationship(relationship) {
    // Set the relationship when Parent or Child button is clicked
    document.getElementById('relationship').value = relationship;
}

function closeForm() {
    // Hide the form without submitting
    document.getElementById('add-relative-form').style.display = 'none';
}

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

    // ERROR starts here
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
        console.log(data.message);
        // Refresh the diagram to show the new relative
        fetchFamilyTreeData(myDiagram);
    })
    .catch(error => {
        console.error('Error adding relative:', error);
    });
    event.target.reset();
    closeForm();
});

function fetchFamilyTreeData(myDiagram) {
    fetch('/get_family_trees')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            myDiagram.model = new go.TreeModel(data);
        });
}
// start everything once the DOM is loaded
document.addEventListener("DOMContentLoaded", init);