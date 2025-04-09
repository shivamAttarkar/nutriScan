<script>
    let { text } = $props();
</script>

{#each text as w}
    <span class="box-shadow-hover">{w}</span>
{/each}

<style>
    .box-shadow-hover:hover {
        filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.5));
    }
</style>
