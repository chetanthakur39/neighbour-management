import {
  AlertTriangle,
  MapPin,
  Radio,
  ArrowLeft,
  Eye,
  Activity,
} from "lucide-react";

import { Link } from "react-router-dom";

import { useValidation } from "../context/ValidationContext";


function Neighbours() {

  // Get latest validation result
  const { validationResult } = useValidation();


  // =====================================================
  // NO VALIDATION RESULT
  // =====================================================

  if (!validationResult) {

    return (
      <div className="max-w-6xl mx-auto">

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-10 text-center">

          {/* Icon */}

          <div className="mx-auto w-16 h-16 flex items-center justify-center bg-blue-50 rounded-2xl">

            <AlertTriangle
              size={32}
              className="text-blue-600"
            />

          </div>


          {/* Heading */}

          <h1 className="mt-6 text-3xl font-bold text-slate-800">
            No Validation Result
          </h1>


          {/* Description */}

          <p className="mt-3 text-slate-500 max-w-lg mx-auto leading-6">

            There is no active validation result.
            Select a State and Jio Center from the Validation
            section and run validation first.

          </p>


          {/* Button */}

          <Link
            to="/validation"
            className="inline-flex items-center gap-2 mt-7 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition"
          >

            Go to Validation

          </Link>

        </div>

      </div>
    );
  }


  // =====================================================
  // VALIDATION DATA
  // =====================================================

  const {
    state,
    jc,
    invalidNeighbours,
    invalidCount,
    validationRules,
  } = validationResult;


  return (

    <div className="max-w-7xl mx-auto space-y-7">


      {/* ================================================= */}
      {/* HEADER                                            */}
      {/* ================================================= */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">

        <div>

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-red-50 rounded-xl">

              <AlertTriangle
                size={26}
                className="text-red-600"
              />

            </div>


            <h1 className="text-3xl font-bold text-slate-800">
              Invalid Neighbours
            </h1>

          </div>


          <p className="mt-2 text-slate-500">
            Invalid 4G → 5G neighbour relationships detected
            during the latest validation.
          </p>

        </div>


        {/* INVALID COUNT */}

        <div className="bg-red-50 border border-red-100 rounded-xl px-5 py-3">

          <p className="text-xs font-medium text-red-500">
            Invalid Count
          </p>

          <p className="text-2xl font-bold text-red-600">
            {invalidCount}
          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* CURRENT LOCATION                                  */}
      {/* ================================================= */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">

        <div className="flex flex-wrap items-center gap-6">


          {/* STATE */}

          <div className="flex items-center gap-3">

            <div className="p-2 bg-blue-50 rounded-lg">

              <MapPin
                size={18}
                className="text-blue-600"
              />

            </div>


            <div>

              <p className="text-xs text-slate-400">
                Selected State
              </p>

              <p className="font-semibold text-slate-800">
                {state}
              </p>

            </div>

          </div>


          {/* DIVIDER */}

          <div className="hidden sm:block h-9 w-px bg-slate-200" />


          {/* JC */}

          <div className="flex items-center gap-3">

            <div className="p-2 bg-indigo-50 rounded-lg">

              <Radio
                size={18}
                className="text-indigo-600"
              />

            </div>


            <div>

              <p className="text-xs text-slate-400">
                Selected Jio Center
              </p>

              <p className="font-semibold text-slate-800">
                {jc}
              </p>

            </div>

          </div>


          {/* DIVIDER */}

          <div className="hidden md:block h-9 w-px bg-slate-200" />


          {/* VALIDATION RULES */}

          <div>

            <p className="text-xs text-slate-400 mb-2">
              Rules Applied
            </p>


            <div className="flex flex-wrap gap-2">

              {validationRules?.pci && (

                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">
                  PCI
                </span>

              )}


              {validationRules?.tac && (

                <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-xs font-semibold">
                  TAC
                </span>

              )}


              {validationRules?.source && (

                <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-xs font-semibold">
                  Source
                </span>

              )}


              {validationRules?.technology && (

                <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-semibold">
                  Technology
                </span>

              )}

            </div>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* NO INVALID NEIGHBOURS                             */}
      {/* ================================================= */}

      {invalidNeighbours.length === 0 ? (

        <div className="bg-white rounded-2xl border border-green-100 shadow-sm p-10 text-center">

          <div className="mx-auto w-16 h-16 flex items-center justify-center bg-green-50 rounded-2xl">

            <Activity
              size={30}
              className="text-green-600"
            />

          </div>


          <h2 className="mt-5 text-xl font-bold text-slate-800">
            No Invalid Neighbours
          </h2>


          <p className="mt-2 text-slate-500">
            All neighbours passed the selected validation rules.
          </p>

        </div>

      ) : (

        /* ================================================= */
        /* INVALID NEIGHBOUR TABLE                          */
        /* ================================================= */

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">


          {/* TABLE HEADER */}

          <div className="px-6 py-5 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">

            <div>

              <h2 className="text-lg font-semibold text-slate-800">
                Invalid Neighbour List
              </h2>

              <p className="text-sm text-slate-500 mt-1">
                Showing {invalidNeighbours.length} invalid
                neighbour relationship(s).
              </p>

            </div>


            <div className="flex items-center gap-2 text-xs font-semibold text-red-600 bg-red-50 px-3 py-2 rounded-lg">

              <span className="w-2 h-2 bg-red-500 rounded-full" />

              Validation Failed

            </div>

          </div>


          {/* ================================================= */}
          {/* TABLE                                            */}
          {/* ================================================= */}

          <div className="overflow-x-auto">

            <table className="w-full min-w-[1200px]">

              <thead>

                <tr className="bg-slate-50 border-b border-slate-200">


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    ECell ID
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    GCell ID
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    4G PCI
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    5G PCI
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    4G TAC
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    5G TAC
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    Handover
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    Distance
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    Relation Index
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    Reason
                  </th>


                  <th className="px-5 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">
                    Status
                  </th>

                </tr>

              </thead>


              {/* ================================================= */}
              {/* TABLE BODY                                        */}
              {/* ================================================= */}

              <tbody className="divide-y divide-slate-100">

                {invalidNeighbours.map((neighbour, index) => (

                  <tr
                    key={`${neighbour.ecellId}-${neighbour.gcellId}-${index}`}
                    className="hover:bg-slate-50 transition"
                  >


                    {/* ECELL */}

                    <td className="px-5 py-4">

                      <span className="font-semibold text-slate-700">
                        {neighbour.ecellId}
                      </span>

                    </td>


                    {/* GCELL */}

                    <td className="px-5 py-4">

                      <span className="font-semibold text-slate-700">
                        {neighbour.gcellId}
                      </span>

                    </td>


                    {/* 4G PCI */}

                    <td className="px-5 py-4">

                      <span
                        className={
                          neighbour.pci4g !== neighbour.pci5g
                            ? "font-semibold text-red-600"
                            : "font-semibold text-green-600"
                        }
                      >
                        {neighbour.pci4g}
                      </span>

                    </td>


                    {/* 5G PCI */}

                    <td className="px-5 py-4">

                      <span
                        className={
                          neighbour.pci4g !== neighbour.pci5g
                            ? "font-semibold text-red-600"
                            : "font-semibold text-green-600"
                        }
                      >
                        {neighbour.pci5g}
                      </span>

                    </td>


                    {/* 4G TAC */}

                    <td className="px-5 py-4">

                      <span
                        className={
                          neighbour.tac4g !== neighbour.tac5g
                            ? "font-semibold text-red-600"
                            : "font-semibold text-green-600"
                        }
                      >
                        {neighbour.tac4g}
                      </span>

                    </td>


                    {/* 5G TAC */}

                    <td className="px-5 py-4">

                      <span
                        className={
                          neighbour.tac4g !== neighbour.tac5g
                            ? "font-semibold text-red-600"
                            : "font-semibold text-green-600"
                        }
                      >
                        {neighbour.tac5g}
                      </span>

                    </td>


                    {/* HANDOVER */}

                    <td className="px-5 py-4 text-slate-600">

                      {neighbour.handoverCount}

                    </td>


                    {/* DISTANCE */}

                    <td className="px-5 py-4 text-slate-600">

                      {neighbour.distance} km

                    </td>


                    {/* RELATION INDEX */}

                    <td className="px-5 py-4">

                      <span className="font-medium text-slate-700">
                        {neighbour.relationIndex}
                      </span>

                    </td>


                    {/* REASON */}

                    <td className="px-5 py-4">

                      <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-red-50 text-red-600 rounded-full text-xs font-semibold whitespace-nowrap">

                        <span className="w-2 h-2 bg-red-500 rounded-full" />

                        {neighbour.reason}

                      </span>

                    </td>


                    {/* STATUS */}

                    <td className="px-5 py-4">

                      <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-red-50 text-red-600 rounded-full text-xs font-semibold">

                        <span className="w-2 h-2 bg-red-500 rounded-full" />

                        INVALID

                      </span>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </div>

      )}


      {/* ================================================= */}
      {/* ACTIONS                                           */}
      {/* ================================================= */}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

        <Link
          to="/validation"
          className="inline-flex items-center gap-2 text-sm font-semibold text-blue-600 hover:text-blue-800"
        >

          <ArrowLeft size={17} />

          Run Another Validation

        </Link>


        {invalidCount > 0 && (

          <div className="flex items-center gap-2 text-sm text-slate-500">

            <Eye size={17} />

            Showing only invalid relationships

          </div>

        )}

      </div>

    </div>

  );
}


export default Neighbours;