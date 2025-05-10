<script>
    import { goto } from "$app/navigation";
    import Shine from "$lib/components/Shine.svelte";
</script>

<div class="hero min-h-screen" style="background-image: url(./hero.png);">
    <div class="hero-overlay"></div>
    <div class="hero-content text-neutral-content text-center">
        <div class="max-w-md">
            <div class="mb-5 text-7xl font-bold">
                <Shine text="NutriScan"></Shine>
            </div>
            <p class="mb-5 text-xl italic">
                <span>Packet Pe Likha Har Shabd Padhne Ki Zarurat Nahi</span>
                <br />Nutri Scan Hai Na, Sab Bataa Dega Bhai! NutriScan
            </p>
            <button class="btn btn-primary" onclick={() => goto("/predict")}
                >Get Started</button
            >
        </div>
    </div>
</div>
