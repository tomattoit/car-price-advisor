import { motion } from "framer-motion";

const InputError = ({ message }) => {
  return (
    <motion.p className="form-input-group__error form-error" {...framer_error}>
      {message}
    </motion.p>
  );
};

const framer_error = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 10 },
  transition: { duration: 0.2 },
};

export default InputError;
