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
function fetchFamilyTreeData(myDiagram) {
    fetch('/family-tree-data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            myDiagram.model = new go.TreeModel(data);
        });
}
// start everything once the DOM is loaded
document.addEventListener("DOMContentLoaded", init);

//Event Listener for Relative Form Submission
document.getElementById('relative-form').addEventListener('submit', function(event) {
    event.preventDefault();
    //Gather form data
    const formData = {
        name: document.getElementById('name').value,
        gender: document.getElementById('gender').value,
        birth_date: document.getElementById('birth_date').value,
        photo_url: document.getElementById('photo_url').value,
        father_id: document.getElementById('father_id').value,
        mother_id: document.getElementById('mother_id').value,
    };

    //Seend form data to the backend via AJAX POST request to endpoint /add_relative
    fetch('/add_relative', {
        method: 'POST',
        headers: {
            //specify the data is in JSON format
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchFamilyTreeData(myDiagram);  // Refresh the family tree
    })
    .catch(error => console.error('Error:', error));
});