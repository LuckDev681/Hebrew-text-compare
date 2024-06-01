import "./App.css";
import React, { useState } from "react";
function App() {
  const [similarity, setSimilarity] = useState(null);
  const [summary, setSummary] = useState(null);
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);

  const handleClick = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/similarity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image1, image2 }),
      });
      const data = await response.json();
      setSimilarity(data.result);
      setSummary(data.summary);
      console.log(data);
    } catch (error) {
      console.error("Error fetching similarity value:", error);
    }
  };

  const handleImageUpload1 = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      setImage1(reader.result);
    };

    reader.readAsDataURL(file);
  };
  const handleImageUpload2 = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      setImage2(reader.result);
    };

    reader.readAsDataURL(file);
  };
  return (
    <div className="App">
      <p className="text-4xl">Text Compare in Images</p>
      <br />
      <div className="flex justify-center">
        <div className="image-container">
          <input type="file" onChange={handleImageUpload1} />
          {image1 && (
            <img src={image1} alt="Uploaded Image1" className="image" />
          )}
        </div>
        <div className="image-container">
          <input type="file" onChange={handleImageUpload2} />
          {image2 && (
            <img src={image2} alt="Uploaded Image2" className="image" />
          )}
        </div>
      </div>
      <div className="flex justify-center">
        <div className="flex-initial w-48">
          <button className="btn btn-md" onClick={handleClick}>
            Result
          </button>
          <input
            className="text-2xl"
            type="text"
            size="1"
            value={similarity}
            readOnly
          />
          %
        </div>
        <div className="flex-initial w-64">
          {" "}
          <input
            className="text-2xl"
            type="text"
            size="15"
            value={summary}
            readOnly
          />
        </div>
      </div>
    </div>
  );
}

export default App;
