let myDiagram = null;
function init() {
    const $ = go.GraphObject.make;  // for conciseness in defining templates

    myDiagram = $(go.Diagram, "family-tree-container",  // must name or refer to the DIV HTML element
        {
            // Instead of TreeLayout, use ForceDirectedLayout for GraphLinksModel, which works better with multiple parent nodes
            layout: $(go.ForceDirectedLayout),
        });

    // Define a simple node template
    myDiagram.nodeTemplate =
        $(go.Node, "Auto",  // Changed from "Spot" to "Auto" for automatic sizing
            $(go.Shape, "Rectangle",  // This defines the node's outer shape
                { fill: "lightblue", stroke: "gray", strokeWidth: 2 }),
            $(go.TextBlock,  // This defines the text inside the node
                {
                    margin: 10, stroke: "black", font: "bold 14px sans-serif",
                    alignment: go.Spot.Center  // Center the text in the node
                },
                new go.Binding("text", "name"))  // Bind the TextBlock to the node data's "name" property
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
        const clickedNode = obj.part.data;
        // Show form for adding relatives
        showAddRelativeForm(clickedNode.key);  // Changed from id to key, which is used in GraphLinksModel
    };
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
    closeForm();
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