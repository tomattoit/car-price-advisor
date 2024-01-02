import { useLocation, Link } from "react-router-dom";

const ResultPage = () => {
  const location = useLocation();
  const { prediction } = location.state;

  return (
    <div className="component__result result">
      <h1 className="result__title">Wynik</h1>
      <div className="result__details details">
        <p className="details__text">Przewidywana cena pojazdu wynosi:</p>
        <p className="details__value">{prediction.toFixed(2)} PLN</p>
      </div>
      <button className="result__return-button return-button">
        <Link to="/" className="return-button__link">
          Powrót do strony głównej
        </Link>
      </button>
    </div>
  );
};

export default ResultPage;
