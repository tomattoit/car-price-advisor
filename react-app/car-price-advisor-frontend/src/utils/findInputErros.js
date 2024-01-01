const findInputError = (errors, inputName) => {
  return Object.keys(errors)
    .filter((key) => key.includes(inputName))
    .reduce((acc, key) => {
      return Object.assign(acc, { error: errors[key] });
    }, {});
};

export default findInputError;
