import {
  AlertTriangle,
  CheckCircle,
  RefreshCw,
  Search,
  ShieldAlert,
  MapPin,
  Radio,
} from "lucide-react";

import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useValidation } from "../context/ValidationContext";


function Neighbours() {

  const navigate = useNavigate();


  // ======================================================
  // VALIDATION RESULT
  // ======================================================

  const {
    validationResult,
    clearValidation,
  } = useValidation();


  // ======================================================
  // SEARCH
  // ======================================================

  const [
    searchTerm,
    setSearchTerm,
  ] = useState("");


  // ======================================================
  // IF NO VALIDATION HAS BEEN RUN
  // ======================================================

  if (!validationResult) {

    return (

      <div className="max-w-6xl mx-auto">

        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-10 text-center">

          <div className="w-16 h-16 mx-auto bg-blue-50 rounded-full flex items-center justify-center">

            <ShieldAlert
              size={30}
              className="text-blue-600"
            />

          </div>


          <h1 className="text-2xl font-bold text-slate-800 mt-5">

            No Validation Result

          </h1>


          <p className="text-slate-500 mt-2">

            Run a validation first to view invalid neighbours.

          </p>


          <button
            type="button"
            onClick={() =>
              navigate("/validation")
            }
            className="mt-6 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition"
          >

            Run Validation

          </button>

        </div>

      </div>

    );

  }


  // ======================================================
  // BACKEND DATA
  // ======================================================

  const {

    state,

    jc,

    totalNeighbours = 0,

    validCount = 0,

    invalidCount = 0,

    invalidNeighbours = [],

    results = [],

    validationRules = {},

  } = validationResult;


  // ======================================================
  // SEARCH FILTER
  // ======================================================

  const filteredNeighbours =
    useMemo(() => {

      const term =
        searchTerm
          .trim()
          .toLowerCase();


      if (!term) {

        return invalidNeighbours;

      }


      return invalidNeighbours.filter(
        (item) => {

          const values = [

            item.neighbourId,

            item.sourceCell,

            item.targetCell,

            item.sourcePci,

            item.targetPci,

            item.sourceTac,

            item.targetTac,

            item.status,

          ];


          return values.some(
            (value) =>
              String(
                value ?? ""
              )
                .toLowerCase()
                .includes(term)
          );

        }
      );

    }, [
      invalidNeighbours,
      searchTerm,
    ]);


  // ======================================================
  // REFRESH / RUN AGAIN
  // ======================================================

  const handleRunAgain = () => {

    navigate(
      "/validation"
    );

  };


  // ======================================================
  // CLEAR
  // ======================================================

  const handleClear = () => {

    clearValidation();

    navigate(
      "/validation"
    );

  };


  // ======================================================
  // PAGE
  // ======================================================

  return (

    <div className="max-w-7xl mx-auto space-y-7">


      {/* ================================================= */}
      {/* HEADER                                            */}
      {/* ================================================= */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <div>

          <div className="flex items-center gap-3">

            <div className="p-3 bg-red-50 rounded-xl">

              <ShieldAlert
                size={27}
                className="text-red-600"
              />

            </div>


            <div>

              <h1 className="text-3xl font-bold text-slate-800">

                Invalid Neighbours

              </h1>


              <p className="text-slate-500 mt-1">

                Actual validation results returned by the backend.

              </p>

            </div>

          </div>

        </div>


        <div className="flex gap-3">

          <button
            type="button"
            onClick={
              handleRunAgain
            }
            className="flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold transition"
          >

            <RefreshCw
              size={17}
            />

            Run Again

          </button>


          <button
            type="button"
            onClick={
              handleClear
            }
            className="px-4 py-2.5 border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl font-semibold transition"
          >

            Clear

          </button>

        </div>

      </div>


      {/* ================================================= */}
      {/* LOCATION                                          */}
      {/* ================================================= */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">


        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-blue-50 rounded-lg">

              <MapPin
                size={20}
                className="text-blue-600"
              />

            </div>


            <div>

              <p className="text-xs font-medium text-slate-500">

                STATE

              </p>


              <p className="text-lg font-bold text-slate-800">

                {state || "—"}

              </p>

            </div>

          </div>

        </div>


        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-indigo-50 rounded-lg">

              <Radio
                size={20}
                className="text-indigo-600"
              />

            </div>


            <div>

              <p className="text-xs font-medium text-slate-500">

                JIO CENTER

              </p>


              <p className="text-lg font-bold text-slate-800">

                {jc || "—"}

              </p>

            </div>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* SUMMARY                                           */}
      {/* ================================================= */}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">


        {/* TOTAL */}

        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

          <p className="text-sm text-slate-500">

            Total Neighbours

          </p>


          <p className="text-3xl font-bold text-slate-800 mt-2">

            {totalNeighbours}

          </p>

        </div>


        {/* VALID */}

        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

          <div className="flex items-center gap-2">

            <CheckCircle
              size={18}
              className="text-green-600"
            />

            <p className="text-sm text-slate-500">

              Valid

            </p>

          </div>


          <p className="text-3xl font-bold text-green-600 mt-2">

            {validCount}

          </p>

        </div>


        {/* INVALID */}

        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

          <div className="flex items-center gap-2">

            <AlertTriangle
              size={18}
              className="text-red-600"
            />

            <p className="text-sm text-slate-500">

              Invalid

            </p>

          </div>


          <p className="text-3xl font-bold text-red-600 mt-2">

            {invalidCount}

          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* RULES                                             */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

        <div className="flex flex-wrap items-center gap-3">

          <span className="text-sm font-semibold text-slate-700">

            Validation Rules:

          </span>


          {validationRules.pci && (

            <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-semibold">

              PCI

            </span>

          )}


          {validationRules.tac && (

            <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-lg text-xs font-semibold">

              TAC

            </span>

          )}

        </div>

      </div>


      {/* ================================================= */}
      {/* SEARCH                                           */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

        <div className="relative">

          <Search
            size={19}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />


          <input
            type="text"
            value={searchTerm}
            onChange={(event) =>
              setSearchTerm(
                event.target.value
              )
            }
            placeholder="Search by neighbour ID, source cell, target cell, PCI or TAC..."
            className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
          />

        </div>

      </div>


      {/* ================================================= */}
      {/* EMPTY INVALID RESULT                              */}
      {/* ================================================= */}

      {invalidNeighbours.length === 0 ? (

        <div className="bg-green-50 border border-green-200 rounded-2xl p-8 text-center">

          <CheckCircle
            size={40}
            className="mx-auto text-green-600"
          />


          <h2 className="text-xl font-bold text-green-800 mt-4">

            No Invalid Neighbours

          </h2>


          <p className="text-green-700 mt-2">

            All {totalNeighbours} neighbours passed the
            selected PCI/TAC validation.

          </p>

        </div>

      ) : (

        <>

          {/* ================================================= */}
          {/* TABLE                                            */}
          {/* ================================================= */}

          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

            <div className="px-6 py-5 border-b border-slate-200">

              <h2 className="text-lg font-semibold text-slate-800">

                Invalid Neighbour Relationships

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Showing {filteredNeighbours.length} of{" "}
                {invalidNeighbours.length} invalid neighbours.

              </p>

            </div>


            <div className="overflow-x-auto">

              <table className="w-full text-sm">

                <thead className="bg-slate-50">

                  <tr>

                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      ID

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Source Cell

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Target Cell

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Source PCI

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Target PCI

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Source TAC

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Target TAC

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Failed Rules

                    </th>


                    <th className="px-5 py-4 text-left font-semibold text-slate-600">

                      Status

                    </th>

                  </tr>

                </thead>


                <tbody className="divide-y divide-slate-100">

                  {filteredNeighbours.map(
                    (item, index) => (

                      <tr
                        key={
                          item.neighbourId ??
                          index
                        }
                        className="hover:bg-slate-50 transition"
                      >

                        {/* ID */}

                        <td className="px-5 py-4 font-semibold text-slate-800">

                          {item.neighbourId ?? "—"}

                        </td>


                        {/* SOURCE CELL */}

                        <td className="px-5 py-4 text-slate-700">

                          {item.sourceCell ?? "—"}

                        </td>


                        {/* TARGET CELL */}

                        <td className="px-5 py-4 text-slate-700">

                          {item.targetCell ?? "—"}

                        </td>


                        {/* SOURCE PCI */}

                        <td className="px-5 py-4">

                          <span className="font-medium text-blue-700">

                            {item.sourcePci ?? "—"}

                          </span>

                        </td>


                        {/* TARGET PCI */}

                        <td className="px-5 py-4">

                          <span className="font-medium text-blue-700">

                            {item.targetPci ?? "—"}

                          </span>

                        </td>


                        {/* SOURCE TAC */}

                        <td className="px-5 py-4">

                          <span className="font-medium text-purple-700">

                            {item.sourceTac ?? "—"}

                          </span>

                        </td>


                        {/* TARGET TAC */}

                        <td className="px-5 py-4">

                          <span className="font-medium text-purple-700">

                            {item.targetTac ?? "—"}

                          </span>

                        </td>


                        {/* FAILED RULES */}

                        <td className="px-5 py-4">

                          <div className="flex flex-wrap gap-1">

                            {Array.isArray(
                              item.failedRules
                            ) &&
                            item.failedRules.length >
                              0 ? (

                              item.failedRules.map(
                                (rule) => (

                                  <span
                                    key={
                                      rule
                                    }
                                    className="px-2 py-1 bg-red-50 text-red-700 rounded-md text-xs font-semibold"
                                  >

                                    {rule}

                                  </span>

                                )
                              )

                            ) : (

                              <span className="text-slate-400">

                                —

                              </span>

                            )}

                          </div>

                        </td>


                        {/* STATUS */}

                        <td className="px-5 py-4">

                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-red-50 text-red-700 rounded-lg text-xs font-bold">

                            <AlertTriangle
                              size={13}
                            />

                            {item.status ??
                              "INVALID"}

                          </span>

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>


            {/* NO SEARCH RESULTS */}

            {filteredNeighbours.length ===
              0 && (

              <div className="p-10 text-center">

                <Search
                  size={32}
                  className="mx-auto text-slate-300"
                />


                <p className="text-slate-500 mt-3">

                  No invalid neighbours match your search.

                </p>

              </div>

            )}

          </div>

        </>

      )}

    </div>

  );

}


export default Neighbours;