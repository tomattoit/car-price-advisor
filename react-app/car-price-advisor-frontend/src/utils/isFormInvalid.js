const isFormInvalid = (err) => {
  return Object.keys(err).length > 0;
};

export default isFormInvalid;
