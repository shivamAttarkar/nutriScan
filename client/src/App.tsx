import React, { useState } from "react";

type PredictionResult = {
  classification: string;
  extracted_ingredients: string;
};

const App: React.FC = () => {
  const [image, setImage] = useState<File | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setImage(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!image) {
      setError("Please select an image.");
      return;
    }
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Failed to fetch results");
      }
      const data: PredictionResult = await response.json();
      setResult(data);
    } catch (error) {
      setError("Error processing the image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <header className="h-[8vh] flex items-center p-6">
        <p className="font-bold text-xl">Healthify</p>
      </header>
      <div className={"flex flex-col items-center justify-center p-4 gap-4 bg-gray-900 text-white min-h-[92vh]"}>
        <h1 className="text-3xl font-bold text-center">Product Classification & Ingredient Extraction</h1>
        {image && (
          <img
            src={URL.createObjectURL(image)}
            alt="Uploaded preview"
            className="max-w-[30vw] object-cover rounded-lg border border-gray-600"
          />
        )}
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="file-input file-input-bordered w-full max-w-xs bg-gray-800 text-white border-gray-600"
        />
        <button
          onClick={handleUpload}
          className="btn btn-primary bg-blue-600 border-none hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Processing..." : "Upload & Analyze"}
        </button>
        {error && <p className="text-red-400">{error}</p>}
        {result && (
          <div className="p-4 bg-gray-800 shadow-md rounded-lg border border-gray-600 max-w-[60vw]">
            <h2 className="text-lg font-bold">Result:</h2>
            <p><strong>Classification:</strong> {result.classification}</p>
            <p><strong>Extracted Ingredients:</strong> {result.extracted_ingredients}</p>
          </div>
        )}
      </div>
    </main>
  );
};

export default App;
