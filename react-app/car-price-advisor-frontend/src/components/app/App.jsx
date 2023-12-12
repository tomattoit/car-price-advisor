import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [people, setPeople] = useState([]);

  useEffect(() => {
    fetch("/api")
      .then((response) => response.json())
      .then((data) => setPeople(data["people"]));
  }, []);

  const peopleList = people.map((person, idx) => {
    return <li key={idx}>{person}</li>;
  });

  return (
    <>
      <div>
        <p>Data from API:</p>
        <ul>{peopleList}</ul>
      </div>
    </>
  );
}

export default App;
