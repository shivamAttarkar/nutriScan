<script>
    // @ts-nocheck

    import { onMount } from "svelte";
    import * as d3 from "d3";

    let { data } = $props();
    let svg;
    console.log(data);

    const total = Object.values(data).reduce((acc, val) => acc + val, 0);

    const filteredData = Object.entries(data)
        .filter(([label, value]) => value > 0)
        .map(([label, value]) => ({ label, value }));

    if (filteredData.length === 0) {
        filteredData.push({ label: "No data", value: 1 });
    }

    onMount(() => {
        const width = 400;
        const height = 400;
        const radius = Math.min(width, height) / 2;

        const color = d3.scaleOrdinal([
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#AA00FF",
            "#FF5733",
        ]);

        const pie = d3.pie().value((d) => d.value);
        const arc = d3
            .arc()
            .outerRadius(radius - 10)
            .innerRadius(0);

        const g = d3

            .select(svg)
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${width / 2}, ${height / 2})`);

        const slices = g
            .selectAll(".slice")

            .data(pie(filteredData))
            .enter()
            .append("g")
            .attr("class", "slice");

        slices
            .append("path")

            .attr("d", arc)

            .attr("fill", (d, i) => color(i));

        slices
            .append("text")
            .attr("transform", (d) => {
                const [x, y] = arc.centroid(d);
                return `translate(${x}, ${y})`;
            })
            .attr("dy", ".35em")
            .attr("text-anchor", "middle")

            .text((d) => `${d.data.label}: ${d.data.value}`);
    });
</script>

<div>
    <svg bind:this={svg}></svg>
    <p class="text-center">Ingredients Classification</p>
</div>
