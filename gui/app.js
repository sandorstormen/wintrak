const svgMargin = { top: 10, right: 10, bottom: 10, left: 10 },
    treeWidth = 500 - svgMargin.left - svgMargin.right,
    treeHeight = 200 - svgMargin.top - svgMargin.bottom;

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function secondsToHMS(seconds) {
    date = new Date(0);
    date.setSeconds(seconds);
    time_string = date.toISOString()
        .split("T")[1]
        .split("Z")[0]
        .replace(/(00:)*/, "")
        .replace(/\.0*/, "");
    return time_string;
}

async function read_data(path) {
    const text = await fetch(path)
        .then(response => response.text());
    var dsv = d3.csvParse(text, d3.autoType);
    return dsv;
}

function calc_data(dsv) {
    program_agg = {};
    total_time = 0;

    dsv.forEach(row => {
        if (!row.ProcessName) {
            return;
        }

        row.ProcessName = capitalize(row.ProcessName);
        row.StartTime = new Date(row.StartTime);
        row.EndTime = new Date(row.EndTime);
        row.DeltaTime = (row.EndTime - row.StartTime) / 1000;

        if (isNaN(row.DeltaTime)) {
            return;
        }
        if (!(row.ProcessName in program_agg)) {
            program_agg[row.ProcessName] = 0;
        }
        program_agg[row.ProcessName] += row.DeltaTime;
        total_time += row.DeltaTime;
    });
    dsv.columns.push("DeltaTime");

    return { "dsv": dsv, "program_agg": program_agg, "total_seconds": total_time };
}

function drawTreeMap(data, svg) {
    total_time = Object.values(data).reduce((a, b) => a + b, 0);
    Object.entries(data).forEach(row => {
        percentage = row[1] / total_time;
        if (percentage < 0.025) {
            delete data[row[0]];
        }
    });

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
        .size([treeWidth, treeHeight])
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

    // and to add the text labels
    svg
        .selectAll("text")
        .data(root.leaves())
        .join("text")
        .attr("x", function (d) { return d.x0 + 10 })    // +10 to adjust position (more right)
        .attr("y", function (d) { return d.y0 + 20 })    // +20 to adjust position (lower)
        .text(function (d) { return d.data.name })
        .attr("transform", function (d) {
            d.w = this.getComputedTextLength();
            if (d.x0 + d.w >= d.x1 - 4) {
                return "rotate(90 " + (d.x0 + 10) + " " + (d.y0 + 20) + ")";
            }
            return "";
        })
        .style("opacity", function (d) {
            d.w = this.getComputedTextLength();
            if (d.x0 + d.w >= d.x1 && d.y0 + d.w >= d.x1) {
                return 0;
            }
            return 1;
        })
}

const divTreeMap = d3
    .select("#tree")
const svgTreeMap = divTreeMap
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", `0 0 ${treeWidth} ${treeHeight}`)
    .classed("svg-content-responsive", true)


d3.select(window).on("resize", function () {
    var newWidth = d3.selectAll("svg").style("width");
    // 600 px as in viewBox width
    const newFontSize = 15 * (600 / parseInt(newWidth));
    d3.selectAll("svg>text")
        .style("font-size", newFontSize)
});

read_data("../../data.csv")
    .then(dsv => calc_data(dsv))
    .then(res => {
        dsv = res.dsv;
        program_agg = res.program_agg;
        drawTreeMap(program_agg, svgTreeMap)

        total_time_elem = document.getElementById("total-time")

        total_time_elem.innerHTML = secondsToHMS(res.total_seconds);

        uls = document.querySelectorAll("#top-programs>ul")
        var name_ul, time_ul = uls;
        Object.entries(program_agg).sort((a, b) => b[1] - a[1]).slice(0, 5).forEach(([key, value]) => {
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(key));
            name_ul.appendChild(li);

            var li = document.createElement("li");
            li.appendChild(document.createTextNode(secondsToHMS(value)));
            time_ul.appendChild(li);
        });

        top_windows_ul = document.getElementById("top-windows");
    });

