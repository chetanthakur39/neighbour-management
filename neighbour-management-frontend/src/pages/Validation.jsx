import { useState } from "react";

import { API_BASE_URL } from "../config";
import {
  ShieldCheck,
  Play,
  MapPin,
  Radio,
  CheckCircle,
  ChevronDown,
  AlertTriangle,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import { useValidation } from "../context/ValidationContext";


// ======================================================
// STATE + JC DATA
// Matches the dataset inserted into MySQL
// ======================================================

const stateData = {

  Delhi: [
    {
      name: "JC_Central_Delhi",
      latitude: 28.6139,
      longitude: 77.2090,
    },
  ],

  "Uttar Pradesh": [
    {
      name: "JC_Lucknow",
      latitude: 28.6208,
      longitude: 77.2185,
    },
  ],

  Rajasthan: [
    {
      name: "JC_Jaipur",
      latitude: 26.9124,
      longitude: 75.7873,
    },
    {
      name: "JC_Jaipur_North",
      latitude: 26.9124,
      longitude: 75.7873,
    },
  ],

  Maharashtra: [
    {
      name: "JC_Mumbai",
      latitude: 19.0760,
      longitude: 72.8777,
    },
  ],

  Gujarat: [
    {
      name: "JC_Ahmedabad",
      latitude: 23.0225,
      longitude: 72.5714,
    },
  ],

  Karnataka: [
    {
      name: "JC_Bangalore",
      latitude: 12.9716,
      longitude: 77.5946,
    },
  ],

  "Tamil Nadu": [
    {
      name: "JC_Chennai",
      latitude: 13.0827,
      longitude: 80.2707,
    },
  ],

  "West Bengal": [
    {
      name: "JC_Kolkata",
      latitude: 22.5726,
      longitude: 88.3639,
    },
  ],

  Bihar: [
    {
      name: "JC_Patna",
      latitude: 25.5941,
      longitude: 85.1376,
    },
  ],

  "Madhya Pradesh": [
    {
      name: "JC_Bhopal",
      latitude: 23.2599,
      longitude: 77.4126,
    },
  ],

  Kerala: [
    {
      name: "JC_Kochi",
      latitude: 9.9312,
      longitude: 76.2673,
    },
  ],

  Odisha: [
    {
      name: "JC_Bhubaneswar",
      latitude: 20.2961,
      longitude: 85.8245,
    },
  ],

  Punjab: [
    {
      name: "JC_Chandigarh",
      latitude: 30.7333,
      longitude: 76.7794,
    },
  ],

  Haryana: [
    {
      name: "JC_Gurgaon",
      latitude: 28.4595,
      longitude: 77.0266,
    },
  ],

  Jharkhand: [
    {
      name: "JC_Ranchi",
      latitude: 23.3441,
      longitude: 85.3096,
    },
  ],

  Assam: [
    {
      name: "JC_Guwahati",
      latitude: 26.1445,
      longitude: 91.7362,
    },
  ],

  Chandigarh: [
    {
      name: "JC_Chandigarh",
      latitude: 30.7333,
      longitude: 76.7794,
    },
  ],

  "Jammu and Kashmir": [
    {
      name: "JC_Srinagar",
      latitude: 34.0837,
      longitude: 74.7973,
    },
  ],

  Uttarakhand: [
    {
      name: "JC_Dehradun",
      latitude: 30.3165,
      longitude: 78.0322,
    },
  ],

  "Himachal Pradesh": [
    {
      name: "JC_Shimla",
      latitude: 31.1048,
      longitude: 77.1734,
    },
  ],

  Goa: [
    {
      name: "JC_Panaji",
      latitude: 15.4909,
      longitude: 73.8278,
    },
  ],

  Telangana: [
    {
      name: "JC_Hyderabad",
      latitude: 17.3850,
      longitude: 78.4867,
    },
  ],

  "Andhra Pradesh": [
    {
      name: "JC_Vijayawada",
      latitude: 16.5062,
      longitude: 80.6480,
    },
  ],

};


function Validation() {

  const navigate = useNavigate();

  const {
    runValidation,
  } = useValidation();


  // ====================================================
  // LOCATION
  // ====================================================

  const [state, setState] =
    useState("");

  const [jc, setJc] =
    useState("");


  // ====================================================
  // VALIDATION RULES
  // ====================================================
  //
  // Only PCI and TAC are supported.
  //
  // ====================================================

  const [validatePCI, setValidatePCI] =
    useState(true);

  const [validateTAC, setValidateTAC] =
    useState(true);


  // ====================================================
  // RULE DROPDOWN
  // ====================================================

  const [
    showRulesDropdown,
    setShowRulesDropdown,
  ] = useState(false);


  // ====================================================
  // LOADING
  // ====================================================

  const [loading, setLoading] =
    useState(false);


  // ====================================================
  // ERROR
  // ====================================================

  const [error, setError] =
    useState("");


  // ====================================================
  // AVAILABLE JCs
  // ====================================================

  const availableJCs =
    state
      ? stateData[state] || []
      : [];


  // ====================================================
  // SELECTED RULES
  // ====================================================

  const selectedRules = [];

  if (validatePCI) {
    selectedRules.push("PCI");
  }

  if (validateTAC) {
    selectedRules.push("TAC");
  }


  // ====================================================
  // STATE CHANGE
  // ====================================================

  const handleStateChange = (
    event
  ) => {

    const selectedState =
      event.target.value;


    setState(
      selectedState
    );


    setJc("");

    setError("");

  };


  // ====================================================
  // TOGGLE RULE
  // ====================================================

  const toggleRule = (
    rule
  ) => {

    if (
      rule === "PCI"
    ) {

      setValidatePCI(
        (previous) =>
          !previous
      );

    }


    if (
      rule === "TAC"
    ) {

      setValidateTAC(
        (previous) =>
          !previous
      );

    }

  };


  // ====================================================
  // SELECT / CLEAR ALL
  // ====================================================

  const toggleAllRules = () => {

    const allSelected =
      validatePCI &&
      validateTAC;


    if (allSelected) {

      setValidatePCI(false);

      setValidateTAC(false);

    } else {

      setValidatePCI(true);

      setValidateTAC(true);

    }

  };


  // ====================================================
  // RUN REAL BACKEND VALIDATION
  // ====================================================

  const handleValidation =
    async () => {

      // ----------------------------------------------
      // STATE
      // ----------------------------------------------

      if (!state) {

        alert(
          "Please select a State."
        );

        return;

      }


      // ----------------------------------------------
      // JC
      // ----------------------------------------------

      if (!jc) {

        alert(
          "Please select a Jio Center."
        );

        return;

      }


      // ----------------------------------------------
      // RULES
      // ----------------------------------------------

      if (
        selectedRules.length === 0
      ) {

        alert(
          "Please select at least one validation rule."
        );

        return;

      }


      try {

        setLoading(true);

        setError("");


        // --------------------------------------------
        // REQUEST
        // --------------------------------------------

        const requestBody = {

          state,

          jc,

          rules:
            selectedRules,

        };


        console.log(
          "Validation request:",
          requestBody
        );


        // --------------------------------------------
        // CALL SPRING BOOT
        // --------------------------------------------

        const response =
          await fetch(
            `${API_BASE_URL}/validation/run`,
            {

              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",
              },

              body:
                JSON.stringify(
                  requestBody
                ),

            }
          );


        // --------------------------------------------
        // HANDLE HTTP ERROR
        // --------------------------------------------

        if (!response.ok) {

          let message =
            `Validation failed (${response.status})`;


          try {

            const errorBody =
              await response.json();


            message =
              errorBody.message ||
              errorBody.error ||
              message;

          } catch {

            // Keep default message.

          }


          throw new Error(
            message
          );

        }


        // --------------------------------------------
        // GET REAL BACKEND RESPONSE
        // --------------------------------------------

        const data =
          await response.json();


        console.log(
          "Validation response:",
          data
        );


        // --------------------------------------------
        // STORE RESULT IN CONTEXT
        // --------------------------------------------

        runValidation({

          state:
            data.state,

          jc:
            data.jc,

          totalNeighbours:
            data.totalNeighbours,

          validCount:
            data.validNeighbours,

          invalidCount:
            data.invalidNeighbours,

          invalidNeighbours:
            Array.isArray(
              data.results
            )
              ? data.results.filter(
                  (item) =>
                    item.status ===
                    "INVALID"
                )
              : [],

          results:
            Array.isArray(
              data.results
            )
              ? data.results
              : [],

          validationRules: {

            pci:
              selectedRules.includes(
                "PCI"
              ),

            tac:
              selectedRules.includes(
                "TAC"
              ),

          },

        });


        // --------------------------------------------
        // GO TO NEIGHBOURS
        // --------------------------------------------

        navigate(
          "/neighbours"
        );

      } catch (error) {

        console.error(
          "Validation failed:",
          error
        );


        setError(
          error.message ||
          "Unable to run validation."
        );

      } finally {

        setLoading(false);

      }

    };


  // ====================================================
  // PAGE
  // ====================================================

  return (

    <div className="max-w-5xl mx-auto space-y-8">


      {/* ================================================= */}
      {/* HEADER                                            */}
      {/* ================================================= */}

      <div>

        <div className="flex items-center gap-3">

          <div className="p-3 bg-blue-50 rounded-xl">

            <ShieldCheck
              size={27}
              className="text-blue-600"
            />

          </div>


          <div>

            <h1 className="text-3xl font-bold text-slate-800">

              Neighbour Validation

            </h1>


            <p className="mt-1 text-slate-500">

              Select a State and Jio Center to validate
              4G → 5G neighbour relationships.

            </p>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* ERROR                                             */}
      {/* ================================================= */}

      {error && (

        <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-xl">

          <AlertTriangle
            size={20}
            className="text-red-600 mt-0.5"
          />


          <div>

            <p className="text-sm font-semibold text-red-800">

              Validation Error

            </p>


            <p className="text-sm text-red-700 mt-1">

              {error}

            </p>

          </div>

        </div>

      )}


      {/* ================================================= */}
      {/* LOCATION CARD                                     */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

        <h2 className="text-lg font-semibold text-slate-800">

          Select Location

        </h2>


        <p className="text-sm text-slate-500 mt-1">

          The backend will validate neighbours belonging
          to the selected State and Jio Center.

        </p>


        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">


          {/* STATE */}

          <div>

            <label
              htmlFor="validation-state"
              className="block text-sm font-medium text-slate-700 mb-2"
            >

              <span className="flex items-center gap-2">

                <MapPin
                  size={17}
                  className="text-blue-600"
                />

                State

              </span>

            </label>


            <select
              id="validation-state"
              value={state}
              onChange={
                handleStateChange
              }
              disabled={loading}
              className="w-full px-4 py-3 border border-slate-300 rounded-xl bg-white text-slate-700 outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
            >

              <option value="">

                Select State

              </option>


              {Object.keys(
                stateData
              ).map(
                (item) => (

                  <option
                    key={item}
                    value={item}
                  >

                    {item}

                  </option>

                )
              )}

            </select>

          </div>


          {/* JC */}

          <div>

            <label
              htmlFor="validation-jc"
              className="block text-sm font-medium text-slate-700 mb-2"
            >

              <span className="flex items-center gap-2">

                <Radio
                  size={17}
                  className="text-indigo-600"
                />

                Jio Center

              </span>

            </label>


            <select
              id="validation-jc"
              value={jc}
              disabled={
                !state ||
                loading
              }
              onChange={(event) =>
                setJc(
                  event.target.value
                )
              }
              className="w-full px-4 py-3 border border-slate-300 rounded-xl bg-white text-slate-700 outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100 disabled:text-slate-400"
            >

              <option value="">

                {state
                  ? "Select Jio Center"
                  : "Select State First"}

              </option>


              {availableJCs.map(
                (location) => (

                  <option
                    key={
                      location.name
                    }
                    value={
                      location.name
                    }
                  >

                    {location.name}

                  </option>

                )
              )}

            </select>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* VALIDATION RULES                                  */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

        <label className="block text-sm font-medium text-slate-700 mb-2">

          Validation Rules

        </label>


        <div className="relative">


          {/* DROPDOWN */}

          <button
            type="button"
            onClick={() =>
              setShowRulesDropdown(
                (previous) =>
                  !previous
              )
            }
            disabled={loading}
            className="w-full min-h-[52px] px-4 py-3 border border-slate-300 rounded-xl bg-white flex items-center justify-between text-left disabled:bg-slate-100"
          >

            <div className="flex flex-wrap gap-2">

              {selectedRules.length ===
              0 ? (

                <span className="text-slate-400">

                  Select validation rules

                </span>

              ) : (

                selectedRules.map(
                  (rule) => (

                    <span
                      key={rule}
                      className={
                        rule ===
                        "PCI"

                          ? "px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-semibold"

                          : "px-3 py-1 bg-purple-50 text-purple-700 rounded-lg text-xs font-semibold"
                      }
                    >

                      {rule}

                    </span>

                  )
                )

              )}

            </div>


            <ChevronDown
              size={19}
              className={
                `text-slate-500 transition-transform ${
                  showRulesDropdown
                    ? "rotate-180"
                    : ""
                }`
              }
            />

          </button>


          {showRulesDropdown && (

            <div className="absolute z-50 mt-2 w-full bg-white border border-slate-200 rounded-xl shadow-xl overflow-hidden">


              {/* PCI */}

              <label className="flex items-center gap-3 px-4 py-3 hover:bg-blue-50 cursor-pointer">

                <input
                  type="checkbox"
                  checked={
                    validatePCI
                  }
                  onChange={() =>
                    toggleRule(
                      "PCI"
                    )
                  }
                  className="w-4 h-4 accent-blue-600"
                />


                <div>

                  <p className="text-sm font-semibold text-slate-700">

                    PCI

                  </p>


                  <p className="text-xs text-slate-400">

                    PCI must match.

                  </p>

                </div>

              </label>


              {/* TAC */}

              <label className="flex items-center gap-3 px-4 py-3 hover:bg-purple-50 cursor-pointer">

                <input
                  type="checkbox"
                  checked={
                    validateTAC
                  }
                  onChange={() =>
                    toggleRule(
                      "TAC"
                    )
                  }
                  className="w-4 h-4 accent-purple-600"
                />


                <div>

                  <p className="text-sm font-semibold text-slate-700">

                    TAC

                  </p>


                  <p className="text-xs text-slate-400">

                    TAC must match.

                  </p>

                </div>

              </label>


              {/* SELECT ALL */}

              <div className="border-t border-slate-200 px-4 py-3">

                <button
                  type="button"
                  onClick={
                    toggleAllRules
                  }
                  className="text-sm font-semibold text-blue-600 hover:text-blue-800"
                >

                  {validatePCI &&
                  validateTAC
                    ? "Clear All"
                    : "Select All"}

                </button>

              </div>

            </div>

          )}

        </div>


        <p className="text-xs text-slate-500 mt-2">

          PCI and TAC are the only supported validation
          rules. Both are selected by default.

        </p>

      </div>


      {/* ================================================= */}
      {/* SAFETY INFORMATION                                */}
      {/* ================================================= */}

      <div className="flex items-start gap-3 p-5 bg-amber-50 border border-amber-200 rounded-xl">

        <ShieldCheck
          size={20}
          className="text-amber-600 mt-0.5"
        />


        <div>

          <p className="text-sm font-semibold text-amber-800">

            Validation Safety

          </p>


          <p className="text-sm text-amber-700 mt-1 leading-6">

            Validation checks the selected neighbour
            relationships using PCI and TAC values from
            the database. This manual validation only
            identifies invalid neighbours; it does not
            delete them.

          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* RUN VALIDATION                                    */}
      {/* ================================================= */}

      <div className="flex justify-end">

        <button
          type="button"
          onClick={
            handleValidation
          }
          disabled={
            loading
          }
          className="flex items-center justify-center gap-3 px-7 py-3.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold rounded-xl shadow-sm transition"
        >

          {loading ? (

            <>

              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />

              Validating...

            </>

          ) : (

            <>

              <Play
                size={19}
              />

              Run Validation

            </>

          )}

        </button>

      </div>


      {/* ================================================= */}
      {/* INFORMATION                                      */}
      {/* ================================================= */}

      <div className="flex items-start gap-3 p-5 bg-blue-50 border border-blue-100 rounded-xl">

        <CheckCircle
          size={20}
          className="text-blue-600 mt-0.5 flex-shrink-0"
        />


        <div>

          <p className="text-sm font-semibold text-blue-800">

            How validation works

          </p>


          <p className="text-sm text-blue-700 mt-1 leading-6">

            The selected State and Jio Center are sent to
            the Spring Boot backend. The backend fetches
            the corresponding neighbour relationships from
            MySQL and validates their PCI and TAC values.
            Only invalid relationships are shown on the
            Neighbours page.

          </p>

        </div>

      </div>


    </div>

  );

}


export default Validation;
