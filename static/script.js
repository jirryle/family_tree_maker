function init() {
    const $ = go.GraphObject.make;  // for conciseness in defining templates

    const myDiagram = $(go.Diagram, "family-tree-container",  // must name or refer to the DIV HTML element
        {
            // configure the diagram layout
            layout: $(go.TreeLayout, { angle: 90, layerSpacing: 35 }),
        });

    // Define a simple node template
    myDiagram.nodeTemplate =
        $(go.Node, "Horizontal",
            // define the node's outer shape, which will surround the TextBlock
            $(go.Shape, "Rectangle", 
                { fill: "lightblue", stroke: null }),
            $(go.TextBlock,
                { margin: 12, stroke: "black", font: "bold 14px sans-serif" },
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
    myDiagram.model = new go.TreeModel([
        // define the tree's node data
        { key: 1, name: "Person 1" },
        { key: 2, parent: 1, name: "Person 2" },
        { key: 3, parent: 1, name: "Person 3" }
        // and so on for more family members
    ]);
}

// start everything once the DOM is loaded
document.addEventListener("DOMContentLoaded", init);
