import { useState } from "react";
import "./App.css";

function App() {
  const [postData, setPostData] = useState({
    aso: false,
    brand: "BMW",
    capacity: 2993,
    color: "Granatowy",
    fuel_type: "Diesel",
    horse_power: 258,
    is_used: true,
    mileage: 230000,
    no_accidents: true,
    number_of_doors: 5,
    origin_country: "Unknown",
    transmission: "Automatyczna",
    year: 2014,
  });

  const [responseData, setResponseData] = useState(null);

  const handlePostRequest = async () => {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });

    const data = await response.json();
    setResponseData(data);
  };

  const response = responseData ? (
    <div>
      <p>{responseData}</p>
    </div>
  ) : null;

  return (
    <>
      <div>
        <button onClick={handlePostRequest}>Send POST Request</button>
      </div>
      {response}
    </>
  );
}

export default App;
