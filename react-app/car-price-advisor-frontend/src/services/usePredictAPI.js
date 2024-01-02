import { useHttp } from "../hooks/http.hook";

const usePredictAPI = () => {
  const _apiBase = "/api";

  const { loading, error, request, cleanError } = useHttp();

  const predict = async (data) => {
    const binaryFeatures = ["aso", "is_used", "no_accidents"];
    const numericFeatures = ["capacity", "number_of_doors", "mileage", "horse_power", "year"];

    _convertBinaryFeatures(data, binaryFeatures);
    _convertNumericFeatures(data, numericFeatures);

    const url = `${_apiBase}/predict`;
    const response = await request(url, "POST", JSON.stringify(data));
    return response;
  };

  const _convertBinaryFeatures = (data, binaryFeatures) => {
    binaryFeatures.forEach((feature) => {
      data[feature] = data[feature] === "Tak";
    });
  };

  const _convertNumericFeatures = (data, numericFeatures) => {
    numericFeatures.forEach((feature) => {
      data[feature] = parseInt(data[feature]);
    });
  };

  return { predict, loading, error, cleanError };
};

export default usePredictAPI;
