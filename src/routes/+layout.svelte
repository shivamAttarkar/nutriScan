<script lang="ts">
	import "../app.css";
	import { onMount } from "svelte";
	import { themeChange } from "theme-change";
	import { fade, fly } from "svelte/transition";
	import Header from "$lib/components/Header.svelte";
	onMount(() => {
		themeChange(false);
	});
	let { children, data } = $props();
</script>

<div class="relative">
	<Header pathname={data.pathname}></Header>
	{#key data.pathname}
		<div class="relative" in:fly={{ x: -150 }}>
			{@render children()}
		</div>
	{/key}
</div>
