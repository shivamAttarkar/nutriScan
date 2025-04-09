<script>
    let { data } = $props();
    import PieChart from "$lib/components/PieChart.svelte";
</script>

<main
    class="min-h-screen p-10 max-w-screen flex flex-col items-center justify-center"
>
    {#if $data}
        <h2 class="text-4xl font-bold">Classification Results</h2>
        <p class="py-2">
            Overall Result: <span class="font-bold">{$data.classification}</span
            >
        </p>
        <div class="flex items-center justify-center gap-6">
            <div>
                <PieChart data={$data.count}></PieChart>
            </div>
            <div
                class="max-h-min max-w-[70%] rounded-xl mb-10 bg-base-200 pb-6 px-6"
            >
                <li class="p-4 pb-2 text-base opacity-60 tracking-wide">
                    Classified Ingredients List
                </li>
                <ul
                    class="list bg-base-100 rounded-box shadow-md max-h-[240px] overflow-scroll overflow-x-clip"
                >
                    {#each $data.classified_ingredients as i}
                        <li class="list-row flex justify-between">
                            <p class=" max-w-[70%] truncate">{i.ingredient}</p>
                            {#if i.status == "Healthy"}
                                <p class="badge badge-success">{i.status}</p>
                            {:else if i.status == "Moderately Healthy"}
                                <p class="badge badge-neutral">{i.status}</p>
                            {:else}
                                <p class="badge badge-error">{i.status}</p>
                            {/if}
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    {/if}
</main>
