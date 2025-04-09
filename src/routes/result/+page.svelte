<script>
    import { onMount } from "svelte";
    import { data } from "$lib/store";
    import { goto } from "$app/navigation";
    import Result from "$lib/components/Result.svelte";
    onMount(() => {
        if (!$data) {
            goto("/predict");
        }
    });
</script>

<Result {data}></Result>
