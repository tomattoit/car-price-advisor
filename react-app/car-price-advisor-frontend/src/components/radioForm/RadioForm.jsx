import { AnimatePresence } from "framer-motion";
import { useFormContext } from "react-hook-form";

import findInputError from "../../utils/findInputErros";
import isFormInvalid from "../../utils/isFormInvalid";
import InputError from "../inputForm/InputError";

const RadioForm = ({ label, name, options }) => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  const inputError = findInputError(errors, name);
  const isInvalid = isFormInvalid(inputError);

  const registerOptions = {
    required: { value: true, message: "To pole jest wymagane" },
  };

  const formClasses = `form-wrapper__${name}-form input-radio-wrapper`;
  return (
    <div className={formClasses}>
      <label htmlFor={name} className="input-radio-wrapper__label form-label">
        {label}
      </label>
      <AnimatePresence mode="wait" initial={false}>
        {isInvalid && <InputError message={inputError.error.message} key={inputError.error.message} />}
      </AnimatePresence>
      {options.map((option, idx) => {
        return (
          <div className="choices-flex__radio-group radio-group" key={idx}>
            <label className="radio-group__label radio-choice-label">
              <input
                className="radio-choice-label__input"
                type="radio"
                name={name}
                id={name}
                value={option}
                {...register(name, { ...registerOptions })}
              />
              {option}
              <span className="radio-choice-label__checkmark"></span>
            </label>
          </div>
        );
      })}
    </div>
  );
};

export default RadioForm;
