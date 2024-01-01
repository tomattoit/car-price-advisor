import { useFormContext } from "react-hook-form";

const SelectForm = ({ name, label, options }) => {
  const { register } = useFormContext();

  const formClasses = `form-wrapper__${name}-form form-input-group`;
  return (
    <div className={formClasses}>
      <label className="form-input-group__label form-label"> {label}: </label>

      <select
        className="form-input-group__select form-select"
        name={name}
        id={name}
        {...register(name, { required: true })}
      >
        {options.map((option, idx) => (
          <option value={option} key={idx}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SelectForm;
