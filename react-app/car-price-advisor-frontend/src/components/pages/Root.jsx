import header_image from "../../recources/img/car-present.svg";
import { Outlet } from "react-router-dom";

function Root() {
  return (
    <div className="component">
      <div className="component__img">
        <img src={header_image} alt="Car as a present" />
      </div>
      <Outlet />
    </div>
  );
}

export default Root;
