import {
  createContext,
  useContext,
  useState,
} from "react";


// ======================================================
// CONTEXT
// ======================================================

const ValidationContext =
  createContext(null);


// ======================================================
// PROVIDER
// ======================================================

export function ValidationProvider({
  children,
}) {

  const [
    validationResult,
    setValidationResult,
  ] = useState(null);


  // ====================================================
  // STORE BACKEND VALIDATION RESULT
  // ====================================================

  const runValidation = (
    result
  ) => {

    setValidationResult(
      result
    );

  };


  // ====================================================
  // CLEAR RESULT
  // ====================================================

  const clearValidation = () => {

    setValidationResult(
      null
    );

  };


  // ====================================================
  // CONTEXT VALUE
  // ====================================================

  const value = {

    validationResult,

    runValidation,

    clearValidation,

  };


  return (

    <ValidationContext.Provider
      value={value}
    >

      {children}

    </ValidationContext.Provider>

  );

}


// ======================================================
// HOOK
// ======================================================

export function useValidation() {

  const context =
    useContext(
      ValidationContext
    );


  if (!context) {

    throw new Error(
      "useValidation must be used inside ValidationProvider"
    );

  }


  return context;

}