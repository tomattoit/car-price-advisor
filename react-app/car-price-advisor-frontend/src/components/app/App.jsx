import { useState } from "react";

import ComponentDetails from "../componentDetails/ComponentDetails";

import header_image from "../../recources/img/car-present.svg";

function App() {
  return (
    <div className="component">
      <div className="component__img">
        <img src={header_image} alt="Car as a present" />
      </div>
      <ComponentDetails />
    </div>
  );
}

export default App;
