<script lang="ts">
    import { goto } from "$app/navigation";
    import { data, imageURI } from "$lib/store";
    import { fade, fly, scale, slide } from "svelte/transition";

    let images: FileList;
    let imagePreview: string | null = null;
    let button: HTMLButtonElement;

    $: if (images && images[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview = e.target?.result as string;
        };
        reader.readAsDataURL(images[0]);
    } else {
        imagePreview = null;
    }

    const handleSubmit = async (e: Event) => {
        e.preventDefault();
        button.innerText = "Processing...";
        const formData = new FormData();
        formData.set("image", images[0]);
        const res = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            body: formData,
        });
        if (res.ok) {
            data.set(await res.json());
            imageURI.set(imagePreview);
            goto("/result");
        } else {
            alert("Cannot Connect to the Server");
            console.log(res);
        }
        button.innerText = "Submit";
    };
</script>

<main class="bg-base-200 h-screen flex justify-center items-center">
    <div class=" bg-base-100 shadow-lg hover:shadow-2xl p-10 rounded-xl">
        <form class="mx-auto w-min" onsubmit={handleSubmit}>
            <h2 class="py-2 text-xl font-semibold">Upload an Image</h2>
            <div
                class:border-2={!imagePreview}
                class:p-4={!imagePreview}
                class=" border-dashed mb-2 mx-auto outline-0 rounded-xl"
            >
                {#if !imagePreview}
                    <div
                        class=" p-10 flex items-center justify-center outline-0 rounded-lg outline-dashed"
                    >
                        <p>No Image Selected</p>
                    </div>
                {:else}
                    <div
                        class="flex items-center justify-center rounded-xl overflow-hidden m-0 p-0"
                    >
                        <img
                            src={imagePreview}
                            alt="Preview"
                            class="max-w-full max-h-full object-contain"
                        />
                    </div>
                {/if}
            </div>
            <fieldset class="fieldset w-fit">
                <legend class="fieldset-legend">Pick a file</legend>
                <input
                    name="image"
                    type="file"
                    accept="image/*"
                    bind:files={images}
                    required
                    class="file-input min-w-[400px]"
                />
                <label for="image" class="fieldset-label"
                    >File must be an Image</label
                >
            </fieldset>
            <button bind:this={button} class="btn btn-primary w-full"
                >Submit</button
            >
        </form>
    </div>
</main>
