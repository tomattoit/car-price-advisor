import { AnimatePresence } from "framer-motion";
import { useFormContext } from "react-hook-form";

import findInputError from "../../utils/findInputErros";
import isFormInvalid from "../../utils/isFormInvalid";
import InputError from "../inputForm/InputError";

const InputForm = ({ label, name, placeholder, isNumeric, min, max }) => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  const inputError = findInputError(errors, name);
  const isInvalid = isFormInvalid(inputError);

  const registerOptions = {
    required: { value: true, message: "To pole jest wymagane" },
  };

  if (isNumeric) {
    if (min !== undefined)
      registerOptions["min"] = { value: min, message: `Wartość musi być większa od ${min}` };
    if (max !== undefined)
      registerOptions["max"] = { value: max, message: `Wartość musi być mniejsza od ${max}` };
  }

  const input = (
    <input
      type={isNumeric ? "number" : "text"}
      name={name}
      id={name}
      placeholder={placeholder}
      className={"form-input-group__input form-input" + (isInvalid ? " form-input_invalid" : "")}
      {...(isNumeric && min !== undefined && { min })}
      {...(isNumeric && max !== undefined && { max })}
      {...register(name, { ...registerOptions })}
    />
  );
  const formClasses = `form-wrapper__${name}-form form-input-group`;

  return (
    <div className={formClasses}>
      <label htmlFor={name} className="form-input-group__label form-label">
        {label}
      </label>
      <AnimatePresence mode="wait" initial={false}>
        {isInvalid && <InputError message={inputError.error.message} key={inputError.error.message} />}
      </AnimatePresence>
      {input}
    </div>
  );
};

export default InputForm;
