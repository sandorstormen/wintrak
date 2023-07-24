title = document.querySelector("h1")
title.innerText = "xasdasdsadsa"

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

async function read_data(path) {
    const text = await fetch(path)
        .then(response => response.text());
    var dsv = d3.csvParse(text, d3.autoType);
    return dsv;
}

function calc_data(dsv) {
    program_agg = {};

    dsv.forEach(row => {
        if (!row.ProcessName) {
            return;
        }

        row.ProcessName = capitalize(row.ProcessName);
        row.StartTime = new Date(row.StartTime);
        row.EndTime = new Date(row.EndTime);
        row.DeltaTime = row.EndTime - row.StartTime;

        if (isNaN(row.DeltaTime)) {
            return;
        }
        if (!(row.ProcessName in program_agg)) {
            program_agg[row.ProcessName] = 0;
        }
        program_agg[row.ProcessName] += row.DeltaTime;
    });
    dsv.columns.push("DeltaTime");

    return { "dsv": dsv, "program_agg": program_agg };
}

function drawTreeMap(data) {
    const margin = { top: 10, right: 10, bottom: 10, left: 10 },
        width = 500 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

    total_time = Object.values(data).reduce((a, b) => a + b, 0);
    Object.entries(data).forEach(row => {
        percentage = row[1] / total_time;
        if (percentage < 0.025) {
            delete data[row[0]];
        }
    });

    // append the svg object to the body of the page
    const svg = d3.select("#tree")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            `translate(${margin.left}, ${margin.top})`);

    var ready_data = [{ name: 'Origin', parent: '', value: '' }]
    Object.entries(data).forEach(([key, value]) => {
        ready_data.push({ "name": key, "parent": "Origin", "value": value });
    });
    const root = d3.stratify()
        .id(function (d) { return d.name; })   // Name of the entity (column name is name in csv)
        .parentId(function (d) { return d.parent; })   // Name of the parent (column name is parent in csv)
        (ready_data);
    root.sum(function (d) { return d.value })   // Compute the numeric value for each entity

    // Then d3.treemap computes the position of each element of the hierarchy
    // The coordinates are added to the root object above
    d3.treemap()
        .size([width, height])
        .padding(4)
        (root)

    // use this information to add rectangles:
    svg
        .selectAll("rect")
        .data(root.leaves())
        .join("rect")
        .attr('x', function (d) { return d.x0; })
        .attr('y', function (d) { return d.y0; })
        .attr('width', function (d) { return d.x1 - d.x0; })
        .attr('height', function (d) { return d.y1 - d.y0; })
        .style("stroke", "black")
        .style("fill", "#69b3a2");

    // and to add the text labels
    svg
        .selectAll("text")
        .data(root.leaves())
        .join("text")
        .attr("x", function (d) { return d.x0 + 10 })    // +10 to adjust position (more right)
        .attr("y", function (d) { return d.y0 + 20 })    // +20 to adjust position (lower)
        .text(function (d) { return d.data.name })
        .attr("font-size", "15px")
        .attr("fill", "white")
}

read_data("../../data.csv")
    .then(dsv => calc_data(dsv))
    .then(res => {
        dsv = res.dsv;
        program_agg = res.program_agg;
        drawTreeMap(program_agg)
    });

