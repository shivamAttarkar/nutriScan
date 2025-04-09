import { writable } from "svelte/store";

type IngredientStatus = "Healthy" | "Moderately Healthy" | "Unhealthy";

interface ClassifiedIngredient {
    ingredient: string;
    status: IngredientStatus;
}

interface ProductClassification {
    classification: string;
    classified_ingredients: ClassifiedIngredient[];
    count: {
        Healthy: number;
        ModeratelyHealthy: number;
        Unhealthy: number;
    };
    extracted_ingredients: string;
}

export const data = writable<ProductClassification | null>(null);
export const imageURI = writable<string | null>(null);