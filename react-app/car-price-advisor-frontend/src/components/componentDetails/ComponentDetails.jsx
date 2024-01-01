import { useForm, FormProvider } from "react-hook-form";

import InputForm from "../inputForm/InputForm";
import SelectForm from "../selectForm/SelectForm";
import RadioForm from "../radioForm/RadioForm";

const ComponentDetails = () => {
  const methods = useForm();

  const onSubmit = methods.handleSubmit((data) => {
    console.log(data);
  });

  const description =
    "Nasz projekt wykorzystuje zaawansowany model uczenia maszynowego, \
    aby dokładnie przewidzieć wartość Twojego pojazdu na podstawie podanych danych. \
    Sprawdź teraz i odkryj, ile jest wart Twój samochód!";

  return (
    <div className="component__details">
      <h1 className="component__details-title">Doradca cen samochodów</h1>
      <p className="component__details-description">{description}</p>
      <FormProvider {...methods}>
        <form
          className="component-details__form-wrapper form-wrapper"
          onSubmit={(e) => e.preventDefault()}
          noValidate
        >
          <InputForm label="Marka" name="brand" placeholder="Marka pojazdu np. Audi" isNumeric={false} />
          <InputForm
            label="Rok produkcji"
            name="year"
            placeholder="Rok produkcji pojazdu"
            isNumeric={true}
            min={1900}
            max={2023}
          />
          <InputForm
            label="Przebieg"
            name="mileage"
            placeholder="Przebieg pojazdu w km"
            isNumeric={true}
            min={0}
          />
          <SelectForm
            label="Rodzaj paliwa"
            name="fuel_type"
            options={["Benzyna", "Diesel", "Benzyna+LPG", "Elektryczny", "Hybryda"]}
          />
          <InputForm
            label="Pojemność skokowa"
            name="capacity"
            placeholder="Pojemność skokowa w cm^3"
            isNumeric={true}
            min={0}
          />
          <InputForm label="Moc" name="horse_power" placeholder="Moc pojazdu w km" isNumeric={true} min={0} />
          <SelectForm label="Skrzynia biegów" name="transmission" options={["Automatyczna", "Manualna"]} />
          <InputForm
            label="Liczba drzwi"
            name="doors_number"
            placeholder="Liczba dzrwi pojazdu"
            isNumeric={true}
            min={0}
          />
          <InputForm label="Kolor" name="color" placeholder="Kolor pojazdu np. czarny" isNumeric={false} />
          <InputForm
            label="Kraj pochodzenia"
            name="origin_country"
            placeholder="Kraj pochodzenia pojazdu np. Polska"
            isNumeric={false}
          />
          <RadioForm label="Czy pojazd jest serwisowany w ASO?" name="aso" options={["Tak", "Nie"]} />
          <RadioForm label="Bezwypadkowy?" name="no_accidents" options={["Tak", "Nie"]} />
          <RadioForm label="Używany?" name="is_used" options={["Tak", "Nie"]} />
          <button onClick={onSubmit} className="component__button-prediction prediction-btn">
            Sprawdź cenę
          </button>
        </form>
      </FormProvider>
    </div>
  );
};

export default ComponentDetails;
