import { useState, useCallback } from "react";

export const useHttp = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(
    async (url, method = "GET", body = null, headers = { "Content-Type": "application/json" }) => {
      setLoading(true);

      try {
        const response = await fetch(url, { method, headers, body });

        if (!response.ok) {
          throw new Error(`Cannot fetch data from ${url}. Error status: ${response.status}`);
        }
        const result = await response.json();

        setLoading(false);
        return result;
      } catch (e) {
        setLoading(false);
        setError(e.message);
        throw e;
      }
    },
    []
  );

  const cleanError = useCallback(() => setError(null), []);
  return { loading, error, request, cleanError };
};
