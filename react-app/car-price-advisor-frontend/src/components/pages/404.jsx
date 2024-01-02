import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div className="component__result result">
      <h1 className="result__title">404 - page not found</h1>
      <div className="result__details details">
        <p className="details__text">Ta strona nie istnieje!</p>
      </div>
      <button className="result__return-button return-button">
        <Link to="/" className="return-button__link">
          Powrót do strony głównej
        </Link>
      </button>
    </div>
  );
};

export default NotFoundPage;
