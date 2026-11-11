import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";

import {
  Clock,
  Play,
  Pause,
  Square,
  Trash2,
  Plus,
  MapPin,
  Radio,
  ShieldCheck,
  CalendarDays,
  AlertTriangle,
  RotateCcw,
  ChevronDown,
  ArrowRightLeft,
} from "lucide-react";

import LocationMap from "../components/common/LocationMap";





// ======================================================
// STATE + JC + LOCATION DATA
// ======================================================
// Temporary frontend data.
// Later this will come from Spring Boot + MySQL.
// ======================================================

const stateData = {

  Delhi: [
    { name: "JC_Central_Delhi", latitude: 28.6139, longitude: 77.2090 },
  ],

  "Uttar Pradesh": [
    { name: "JC_Lucknow", latitude: 28.6208, longitude: 77.2185 },
  ],

  Rajasthan: [
    { name: "JC_Jaipur", latitude: 26.9124, longitude: 75.7873 },
    { name: "JC_Jaipur_North", latitude: 26.9124, longitude: 75.7873 },
  ],

  Maharashtra: [
    { name: "JC_Mumbai", latitude: 19.0760, longitude: 72.8777 },
  ],

  Gujarat: [
    { name: "JC_Ahmedabad", latitude: 23.0225, longitude: 72.5714 },
  ],

  Karnataka: [
    { name: "JC_Bangalore", latitude: 12.9716, longitude: 77.5946 },
  ],

  "Tamil Nadu": [
    { name: "JC_Chennai", latitude: 13.0827, longitude: 80.2707 },
  ],

  "West Bengal": [
    { name: "JC_Kolkata", latitude: 22.5726, longitude: 88.3639 },
  ],

  Bihar: [
    { name: "JC_Patna", latitude: 25.5941, longitude: 85.1376 },
  ],

  "Madhya Pradesh": [
    { name: "JC_Bhopal", latitude: 23.2599, longitude: 77.4126 },
  ],

  Kerala: [
    { name: "JC_Kochi", latitude: 9.9312, longitude: 76.2673 },
  ],

  Odisha: [
    { name: "JC_Bhubaneswar", latitude: 20.2961, longitude: 85.8245 },
  ],

  Punjab: [
    { name: "JC_Chandigarh", latitude: 30.7333, longitude: 76.7794 },
  ],

  Haryana: [
    { name: "JC_Gurgaon", latitude: 28.4595, longitude: 77.0266 },
  ],

  Jharkhand: [
    { name: "JC_Ranchi", latitude: 23.3441, longitude: 85.3096 },
  ],

  Assam: [
    { name: "JC_Guwahati", latitude: 26.1445, longitude: 91.7362 },
  ],

  Chandigarh: [
    { name: "JC_Chandigarh", latitude: 30.7333, longitude: 76.7794 },
  ],

  "Jammu and Kashmir": [
    { name: "JC_Srinagar", latitude: 34.0837, longitude: 74.7973 },
  ],

  Uttarakhand: [
    { name: "JC_Dehradun", latitude: 30.3165, longitude: 78.0322 },
  ],

  "Himachal Pradesh": [
    { name: "JC_Shimla", latitude: 31.1048, longitude: 77.1734 },
  ],

  Goa: [
    { name: "JC_Panaji", latitude: 15.4909, longitude: 73.8278 },
  ],

  Telangana: [
    { name: "JC_Hyderabad", latitude: 17.3850, longitude: 78.4867 },
  ],

  "Andhra Pradesh": [
    { name: "JC_Vijayawada", latitude: 16.5062, longitude: 80.6480 },
  ],

};


// ======================================================
// AUTOMATION COMPONENT
// ======================================================

function Automation() {


  // ====================================================
  // AUTOMATIONS
  // ====================================================

  const [automations, setAutomations] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  // ====================================================
  // CREATE FORM
  // ====================================================

  const [showCreateForm, setShowCreateForm] =
    useState(false);


  // ====================================================
  // STATE
  // ====================================================

  const [state, setState] =
    useState("");


  // ====================================================
  // JC
  // ====================================================

  const [jc, setJc] =
    useState("");


  // ====================================================
  // SELECTED LOCATION
  // ====================================================

  const [selectedLocation, setSelectedLocation] =
    useState(null);


  // ====================================================
  // TIME
  // ====================================================

  const [time, setTime] =
    useState("10:00");


  // ====================================================
  // MINIMUM NEIGHBOURS
  // ====================================================

  const [minimumNeighbours, setMinimumNeighbours] =
    useState(5);


  // ====================================================
  // TECHNOLOGY FLOW
  // ====================================================

  const [technologyFlow, setTechnologyFlow] =
    useState("4G_TO_5G");


  // ====================================================
  // VALIDATION RULES
  // ====================================================

  const [selectedRules, setSelectedRules] =
    useState([
      "PCI",
      "TAC",
    ]);


  // ====================================================
  // RULE DROPDOWN
  // ====================================================

  const [showRulesDropdown, setShowRulesDropdown] =
    useState(false);


  // ====================================================
  // DELETE MODAL
  // ====================================================

  const [deleteId, setDeleteId] =
    useState(null);


  // ====================================================
  // AVAILABLE JCs
  // ====================================================

  const availableJCs =
    state
      ? stateData[state]
      : [];


  // ====================================================
  // LOAD AUTOMATIONS FROM BACKEND
  // ====================================================

  useEffect(() => {

    loadAutomations();

  }, []);


  const loadAutomations = async () => {

    try {

      setLoading(true);

      setError("");

      const response =
        await fetch(
          `${API_BASE_URL}/automations`
        );

      if (!response.ok) {

        throw new Error(
          `Failed to load automations (${response.status})`
        );

      }

      const data =
        await response.json();

      setAutomations(
        Array.isArray(data)
          ? data.map(mapAutomationFromApi)
          : []
      );

    } catch (error) {

      console.error(
        "Failed to load automations:",
        error
      );

      setError(
        error.message ||
        "Unable to load automations."
      );

    } finally {

      setLoading(false);

    }

  };


  // ====================================================
  // MAP BACKEND RESPONSE TO UI MODEL
  // ====================================================

  const mapAutomationFromApi = (item) => ({

    id: item.automationId,

    name:
      item.name ||
      `${item.jc || "JC"} Daily Validation`,

    state:
      item.state || "",

    jc:
      item.jc || "",

    time:
      normalizeTime(item.executionTime),

    frequency:
      item.frequency || "DAILY",

    technologyFlow:
      normalizeTechnologyFlow(
        item.technologyFlow
      ),

    minimumNeighbours:
      item.minimumNeighbours ?? 5,

    rules:
      Array.isArray(item.rules)
        ? item.rules.filter(
            (rule) =>
              rule === "PCI" ||
              rule === "TAC"
          )
        : [],

    status:
      item.status || "RUNNING",

    lastRun:
      item.lastRunAt
        ? formatDateTime(item.lastRunAt)
        : "Not executed yet",

    nextRun:
      item.nextRunAt
        ? formatDateTime(item.nextRunAt)
        : item.status === "PAUSED"
        ? "Paused"
        : item.status === "ENDED"
        ? "Never"
        : "Not scheduled",

    createdAt:
      item.createdAt
        ? formatDateTime(item.createdAt)
        : "",

  });


  // ====================================================
  // CREATE BACKEND AUTOMATION
  // ====================================================

  const createAutomationApi = async () => {

    const requestBody = {

      name:
        `${jc} Daily Validation`,

      state,

      jc,

      technologyFlow:
        toBackendTechnologyFlow(
          technologyFlow
        ),

      executionTime:
        time,

      minimumNeighbours,

      rules:
        selectedRules,

    };


    const response =
      await fetch(
        `${API_BASE_URL}/automations`,
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


    if (!response.ok) {

      let message =
        `Failed to create automation (${response.status})`;

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

      throw new Error(message);

    }


    return response.json();

  };


  // ====================================================
  // TOGGLE RULE
  // ====================================================

  const toggleRule = (rule) => {

    setSelectedRules((previous) => {

      if (
        previous.includes(rule)
      ) {

        return previous.filter(
          (item) =>
            item !== rule
        );

      }


      return [
        ...previous,
        rule,
      ];

    });

  };


  // ====================================================
  // SELECT ALL / CLEAR ALL
  // ====================================================

  const toggleAllRules = () => {

    if (
      selectedRules.length === 2
    ) {

      setSelectedRules([]);

    } else {

      setSelectedRules([
        "PCI",
        "TAC",
      ]);

    }

  };


  // ====================================================
  // CREATE AUTOMATION
  // ====================================================

  const handleCreateAutomation = async () => {

    if (!state) {

      alert(
        "Please select a State."
      );

      return;

    }


    if (!jc) {

      alert(
        "Please select a Jio Center."
      );

      return;

    }


    if (!time) {

      alert(
        "Please select execution time."
      );

      return;

    }


    if (
      !minimumNeighbours ||
      minimumNeighbours < 1
    ) {

      alert(
        "Please select minimum neighbours."
      );

      return;

    }


    if (
      selectedRules.length === 0
    ) {

      alert(
        "Please select at least one validation rule."
      );

      return;

    }


    try {

      setSaving(true);

      setError("");

      const created =
        await createAutomationApi();


      setAutomations(
        (previous) => [
          mapAutomationFromApi(
            created
          ),
          ...previous,
        ]
      );


      setState("");

      setJc("");

      setSelectedLocation(
        null
      );

      setTime("10:00");

      setMinimumNeighbours(5);

      setTechnologyFlow(
        "4G_TO_5G"
      );

      setSelectedRules([
        "PCI",
        "TAC",
      ]);

      setShowRulesDropdown(
        false
      );

      setShowCreateForm(
        false
      );

    } catch (error) {

      console.error(
        "Create automation failed:",
        error
      );

      setError(
        error.message ||
        "Unable to create automation."
      );

      alert(
        error.message ||
        "Unable to create automation."
      );

    } finally {

      setSaving(false);

    }

  };

  // ====================================================
  // PAUSE
  // ====================================================

  const handlePause = async (id) => {

    try {

      setError("");

      const response =
        await fetch(
          `${API_BASE_URL}/automations/${id}/pause`,
          {
            method: "PUT",
          }
        );


      if (!response.ok) {

        throw new Error(
          `Failed to pause automation (${response.status})`
        );

      }


      const updated =
        await response.json();


      setAutomations(
        (previous) =>
          previous.map(
            (automation) =>
              automation.id === id
                ? mapAutomationFromApi(
                    updated
                  )
                : automation
          )
      );

    } catch (error) {

      console.error(
        "Pause automation failed:",
        error
      );

      setError(
        error.message ||
        "Unable to pause automation."
      );

      alert(
        error.message ||
        "Unable to pause automation."
      );

    }

  };

  // ====================================================
  // RESUME
  // ====================================================

  const handleResume = async (id) => {

    try {

      setError("");

      const response =
        await fetch(
          `${API_BASE_URL}/automations/${id}/resume`,
          {
            method: "PUT",
          }
        );


      if (!response.ok) {

        throw new Error(
          `Failed to resume automation (${response.status})`
        );

      }


      const updated =
        await response.json();


      setAutomations(
        (previous) =>
          previous.map(
            (automation) =>
              automation.id === id
                ? mapAutomationFromApi(
                    updated
                  )
                : automation
          )
      );

    } catch (error) {

      console.error(
        "Resume automation failed:",
        error
      );

      setError(
        error.message ||
        "Unable to resume automation."
      );

      alert(
        error.message ||
        "Unable to resume automation."
      );

    }

  };

  // ====================================================
  // END AUTOMATION
  // ====================================================

  const handleEnd = async (id) => {

    const confirmed =
      window.confirm(
        "Are you sure you want to end this automation? It will no longer run."
      );


    if (!confirmed) {

      return;

    }


    try {

      setError("");

      const response =
        await fetch(
          `${API_BASE_URL}/automations/${id}/end`,
          {
            method: "PUT",
          }
        );


      if (!response.ok) {

        throw new Error(
          `Failed to end automation (${response.status})`
        );

      }


      const updated =
        await response.json();


      setAutomations(
        (previous) =>
          previous.map(
            (automation) =>
              automation.id === id
                ? mapAutomationFromApi(
                    updated
                  )
                : automation
          )
      );

    } catch (error) {

      console.error(
        "End automation failed:",
        error
      );

      setError(
        error.message ||
        "Unable to end automation."
      );

      alert(
        error.message ||
        "Unable to end automation."
      );

    }

  };

  // ====================================================
  // DELETE AUTOMATION
  // ====================================================

  const handleDelete = async () => {

    if (!deleteId) {

      return;

    }


    try {

      setError("");

      const response =
        await fetch(
          `${API_BASE_URL}/automations/${deleteId}`,
          {
            method: "DELETE",
          }
        );


      if (!response.ok) {

        throw new Error(
          `Failed to delete automation (${response.status})`
        );

      }


      setAutomations(
        (previous) =>
          previous.filter(
            (automation) =>
              automation.id !== deleteId
          )
      );


      setDeleteId(null);

    } catch (error) {

      console.error(
        "Delete automation failed:",
        error
      );

      setError(
        error.message ||
        "Unable to delete automation."
      );

      alert(
        error.message ||
        "Unable to delete automation."
      );

    }

  };

  // ====================================================
  // PAGE
  // ====================================================

  return (

    <div className="max-w-7xl mx-auto space-y-7">


      {error && (

        <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-xl">

          <AlertTriangle
            size={20}
            className="text-red-600 mt-0.5"
          />

          <div className="flex-1">

            <p className="text-sm font-semibold text-red-800">
              Backend Error
            </p>

            <p className="text-sm text-red-700 mt-1">
              {error}
            </p>

          </div>

          <button
            type="button"
            onClick={() => setError("")}
            className="text-red-500 hover:text-red-700 text-sm font-semibold"
          >
            Dismiss
          </button>

        </div>

      )}


      {/* ================================================= */}
      {/* HEADER                                           */}
      {/* ================================================= */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">


        {/* TITLE */}

        <div>

          <div className="flex items-center gap-3">

            <div className="p-3 bg-blue-50 rounded-xl">

              <RotateCcw
                size={27}
                className="text-blue-600"
              />

            </div>


            <div>

              <h1 className="text-3xl font-bold text-slate-800">
                Automation
              </h1>

              <p className="mt-1 text-slate-500">
                Schedule automatic neighbour validation
                for a State and Jio Center.
              </p>

            </div>

          </div>

        </div>


        {/* ================================================= */}
        {/* TECHNOLOGY FLOW + NEW AUTOMATION                */}
        {/* ================================================= */}

        <div className="flex items-center gap-3">


          {/* TECHNOLOGY FLOW */}

          <div className="relative">

            <ArrowRightLeft
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-600 pointer-events-none z-10"
            />


            <select
              value={technologyFlow}
              onChange={(event) => {

                const value =
                  event.target.value;


                if (
                  value === "5G_TO_4G"
                ) {

                  alert(
                    "5G → 4G automation will be available in a future version."
                  );

                  return;

                }


                setTechnologyFlow(
                  value
                );

              }}
              className="appearance-none pl-10 pr-10 py-3 bg-white border border-slate-200 rounded-xl shadow-sm text-sm font-semibold text-slate-700 cursor-pointer hover:border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="4G_TO_5G">
                4G → 5G
              </option>


              <option
                value="5G_TO_4G"
                disabled
              >
                5G → 4G (Coming Soon)
              </option>

            </select>


            <ChevronDown
              size={17}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
            />

          </div>


          {/* NEW AUTOMATION */}

          <button
            type="button"
            onClick={() =>
              setShowCreateForm(
                !showCreateForm
              )
            }
            className="inline-flex items-center justify-center gap-2 px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition"
          >

            <Plus size={19} />

            New Automation

          </button>

        </div>

      </div>


      {/* ================================================= */}
      {/* CREATE FORM                                      */}
      {/* ================================================= */}

      {showCreateForm && (

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">


          {/* FORM HEADER */}

          <div className="flex items-start gap-3 mb-7">

            <div className="p-2.5 bg-blue-50 rounded-xl">

              <CalendarDays
                size={23}
                className="text-blue-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">
                Create Daily Automation
              </h2>

              <p className="text-sm text-slate-500 mt-1">
                This automation will run every day at
                the selected time until it is paused or ended.
              </p>

            </div>

          </div>


          {/* ================================================= */}
          {/* STATE + JC                                      */}
          {/* ================================================= */}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">


            {/* STATE */}

            <div>

              <label
                htmlFor="automation-state"
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
                id="automation-state"
                value={state}
                onChange={(event) => {

                  setState(
                    event.target.value
                  );

                  setJc("");

                  setSelectedLocation(
                    null
                  );

                }}
                className="w-full px-4 py-3 border border-slate-300 rounded-xl bg-white text-slate-700 outline-none focus:ring-2 focus:ring-blue-500"
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
                htmlFor="automation-jc"
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
                id="automation-jc"
                value={jc}
                disabled={!state}
                onChange={(event) => {

                  const selectedJC =
                    event.target.value;


                  setJc(
                    selectedJC
                  );


                  const location =
                    availableJCs.find(
                      (item) =>
                        item.name ===
                        selectedJC
                    );


                  setSelectedLocation(

                    location

                      ? {

                          jc:
                            location.name,

                          state,

                          latitude:
                            location.latitude,

                          longitude:
                            location.longitude,

                        }

                      : null

                  );

                }}
                className="w-full px-4 py-3 border border-slate-300 rounded-xl bg-white text-slate-700 outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100 disabled:text-slate-400"
              >

                <option value="">

                  {state
                    ? "Select Jio Center"
                    : "Select State First"}

                </option>


                {availableJCs.map(
                  (item) => (

                    <option
                      key={item.name}
                      value={item.name}
                    >
                      {item.name}
                    </option>

                  )
                )}

              </select>

            </div>

          </div>


          {/* ================================================= */}
          {/* JC LOCATION MAP                                 */}
          {/* ================================================= */}

          <div className="mt-6">

            <div className="flex items-center justify-between mb-3">

              <div>

                <h3 className="text-sm font-semibold text-slate-700">
                  Jio Center Location
                </h3>

                <p className="text-xs text-slate-500 mt-1">
                  Map preview for the selected Jio Center.
                </p>

              </div>


              {selectedLocation && (

                <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-xs font-semibold">

                  <MapPin size={14} />

                  {selectedLocation.jc}

                </div>

              )}

            </div>


            <LocationMap
              location={
                selectedLocation
              }
            />

          </div>


          {/* ================================================= */}
          {/* TECHNOLOGY FLOW                                 */}
          {/* ================================================= */}

          <div className="mt-6">

            <label className="block text-sm font-medium text-slate-700 mb-2">

              Technology Flow

            </label>


            <div className="flex items-center gap-4 p-4 bg-blue-50 border border-blue-100 rounded-xl">

              <div className="p-2.5 bg-white rounded-lg">

                <ArrowRightLeft
                  size={21}
                  className="text-blue-600"
                />

              </div>


              <div>

                <p className="text-sm font-semibold text-blue-800">
                  4G → 5G
                </p>

                <p className="text-xs text-blue-600 mt-1">
                  Current automation flow
                </p>

              </div>


              <span className="ml-auto px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                ACTIVE
              </span>

            </div>


            <p className="text-xs text-slate-500 mt-2">

              The selected technology flow determines which
              validation direction the backend will execute.

            </p>

          </div>


          {/* ================================================= */}
          {/* TIME                                            */}
          {/* ================================================= */}

          <div className="mt-6">

            <label
              htmlFor="automation-time"
              className="block text-sm font-medium text-slate-700 mb-2"
            >

              <span className="flex items-center gap-2">

                <Clock
                  size={17}
                  className="text-blue-600"
                />

                Daily Execution Time

              </span>

            </label>


            <div className="w-full md:w-1/2 flex rounded-xl border border-slate-300 px-3 py-2 bg-white">

              <input
                id="automation-time"
                type="time"
                value={time}
                onChange={(event) =>
                  setTime(
                    event.target.value
                  )
                }
                className="block w-full min-w-0 border-0 bg-transparent p-0 text-base text-slate-700 outline-none"
              />

            </div>


            <p className="text-xs text-slate-500 mt-2">
              The validation will run automatically every
              day at this time.
            </p>

          </div>


          {/* ================================================= */}
          {/* MINIMUM NEIGHBOURS                               */}
          {/* ================================================= */}

          <div className="mt-6">

            <label
              htmlFor="minimum-neighbours"
              className="block text-sm font-medium text-slate-700 mb-2"
            >

              <span className="flex items-center gap-2">

                <ShieldCheck
                  size={17}
                  className="text-green-600"
                />

                Minimum Neighbours

              </span>

            </label>


            <select
              id="minimum-neighbours"
              value={minimumNeighbours}
              onChange={(event) =>
                setMinimumNeighbours(
                  Number(event.target.value)
                )
              }
              className="w-full md:w-1/2 px-4 py-3 border border-slate-300 rounded-xl bg-white text-slate-700 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value={5}>
                5
              </option>

              <option value={10}>
                10
              </option>

              <option value={15}>
                15
              </option>

              <option value={20}>
                20
              </option>

              <option value={25}>
                25
              </option>

              <option value={50}>
                50
              </option>

            </select>


            <p className="text-xs text-slate-500 mt-2">
              Minimum number of neighbours that must be
              retained by the safety engine.
            </p>

          </div>


          {/* ================================================= */}
          {/* FREQUENCY                                       */}
          {/* ================================================= */}

          <div className="mt-6">

            <label className="block text-sm font-medium text-slate-700 mb-2">
              Frequency
            </label>


            <div className="flex items-center gap-3 p-4 bg-blue-50 border border-blue-100 rounded-xl">

              <CalendarDays
                size={20}
                className="text-blue-600"
              />


              <div>

                <p className="font-semibold text-blue-800">
                  Daily
                </p>

                <p className="text-xs text-blue-600 mt-1">
                  Runs every day until paused or ended.
                </p>

              </div>

            </div>

          </div>


          {/* ================================================= */}
          {/* VALIDATION RULES                                */}
          {/* ================================================= */}

          <div className="mt-6">

            <label className="block text-sm font-medium text-slate-700 mb-2">
              Validation Rules
            </label>


            <div className="relative">


              {/* DROPDOWN BUTTON */}

              <button
                type="button"
                onClick={() =>
                  setShowRulesDropdown(
                    (previous) =>
                      !previous
                  )
                }
                className="w-full min-h-[52px] px-4 py-3 border border-slate-300 rounded-xl bg-white flex items-center justify-between text-left hover:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100 transition"
              >

                <div className="flex flex-wrap gap-2 pr-3">

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

                              : rule ===
                                "TAC"

                              ? "px-3 py-1 bg-purple-50 text-purple-700 rounded-lg text-xs font-semibold"

                              : rule ===
                                "Source"

                              ? "px-3 py-1 bg-orange-50 text-orange-700 rounded-lg text-xs font-semibold"

                              : "px-3 py-1 bg-green-50 text-green-700 rounded-lg text-xs font-semibold"
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
                  className={`text-slate-500 flex-shrink-0 transition-transform ${
                    showRulesDropdown
                      ? "rotate-180"
                      : ""
                  }`}
                />

              </button>


              {/* DROPDOWN */}

              {showRulesDropdown && (

                <div className="absolute z-50 mt-2 w-full bg-white border border-slate-200 rounded-xl shadow-xl overflow-hidden">


                  {/* PCI */}

                  <label className="flex items-center gap-3 px-4 py-3 hover:bg-blue-50 cursor-pointer transition">

                    <input
                      type="checkbox"
                      checked={
                        selectedRules.includes(
                          "PCI"
                        )
                      }
                      onChange={() =>
                        toggleRule(
                          "PCI"
                        )
                      }
                      className="w-4 h-4 accent-blue-600"
                    />


                    <div className="flex-1">

                      <p className="text-sm font-semibold text-slate-700">
                        PCI
                      </p>

                      <p className="text-xs text-slate-400">
                        Source PCI must match the configured PCI
                      </p>

                    </div>

                  </label>


                  {/* TAC */}

                  <label className="flex items-center gap-3 px-4 py-3 hover:bg-purple-50 cursor-pointer transition">

                    <input
                      type="checkbox"
                      checked={
                        selectedRules.includes(
                          "TAC"
                        )
                      }
                      onChange={() =>
                        toggleRule(
                          "TAC"
                        )
                      }
                      className="w-4 h-4 accent-purple-600"
                    />


                    <div className="flex-1">

                      <p className="text-sm font-semibold text-slate-700">
                        TAC
                      </p>

                      <p className="text-xs text-slate-400">
                        Target TAC must match the configured TAC
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
                      className="text-sm font-semibold text-blue-600 hover:text-blue-800 transition"
                    >

                      {
                        selectedRules.length ===
                        2
                          ? "Clear All"
                          : "Select All"
                      }

                    </button>

                  </div>

                </div>

              )}

            </div>


            <p className="text-xs text-slate-500 mt-2">

              {selectedRules.length ===
              0

                ? "Select at least one validation rule."

                : `${selectedRules.length} validation ${
                    selectedRules.length ===
                    1
                      ? "rule"
                      : "rules"
                  } selected. PCI and TAC are the supported validation rules.`}

            </p>

          </div>


          {/* ================================================= */}
          {/* SAFETY                                          */}
          {/* ================================================= */}

          <div className="mt-6 flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-xl">

            <AlertTriangle
              size={20}
              className="text-amber-600 mt-0.5"
            />


            <div>

              <p className="text-sm font-semibold text-amber-800">
                Automation Safety
              </p>

              <p className="text-xs text-amber-700 mt-1 leading-5">

                Invalid neighbours are determined using
                PCI and TAC matching. The backend will enforce
                safety restrictions before changing neighbour status.

              </p>

            </div>

          </div>


          {/* ================================================= */}
          {/* FORM BUTTONS                                    */}
          {/* ================================================= */}

          <div className="flex justify-end gap-3 mt-7">

            <button
              type="button"
              onClick={() => {

                setShowCreateForm(
                  false
                );

                setShowRulesDropdown(
                  false
                );

              }}
              className="px-5 py-3 border border-slate-300 text-slate-700 font-semibold rounded-xl hover:bg-slate-50 transition"
            >

              Cancel

            </button>


            <button
              type="button"
              onClick={
                handleCreateAutomation
              }
              disabled={saving}
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition"
            >

              <Play size={18} />

              {saving
                ? "Creating..."
                : "Start Automation"}

            </button>

          </div>

        </div>

      )}


      {/* ================================================= */}
      {/* SUMMARY CARDS                                    */}
      {/* ================================================= */}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">


        {/* TOTAL */}

        <div className="bg-white border border-slate-200 rounded-2xl p-5">

          <p className="text-sm text-slate-500">
            Total Automations
          </p>

          <p className="text-3xl font-bold text-slate-800 mt-2">
            {automations.length}
          </p>

        </div>


        {/* RUNNING */}

        <div className="bg-white border border-green-100 rounded-2xl p-5">

          <p className="text-sm text-slate-500">
            Running
          </p>

          <p className="text-3xl font-bold text-green-600 mt-2">

            {
              automations.filter(
                (item) =>
                  item.status ===
                  "RUNNING"
              ).length
            }

          </p>

        </div>


        {/* PAUSED */}

        <div className="bg-white border border-amber-100 rounded-2xl p-5">

          <p className="text-sm text-slate-500">
            Paused
          </p>

          <p className="text-3xl font-bold text-amber-600 mt-2">

            {
              automations.filter(
                (item) =>
                  item.status ===
                  "PAUSED"
              ).length
            }

          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* SCHEDULED AUTOMATIONS                            */}
      {/* ================================================= */}

      <div className="space-y-5">

        <div>

          <h2 className="text-xl font-semibold text-slate-800">
            Scheduled Automations
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            Manage your daily neighbour validation schedules.
          </p>

        </div>


        {/* ================================================= */}
        {/* LOADING STATE                                    */}
        {/* ================================================= */}

        {loading ? (

          <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center">

            <div className="mx-auto w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />

            <p className="mt-4 text-sm font-medium text-slate-600">
              Loading automations...
            </p>

          </div>

        ) : automations.length ===
        0 ? (

          <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center">

            <CalendarDays
              size={35}
              className="mx-auto text-slate-400"
            />

            <h3 className="mt-4 font-semibold text-slate-700">
              No Automations
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              Create your first daily validation automation.
            </p>

          </div>

        ) : (

          automations.map(
            (automation) => (

              <div
                key={
                  automation.id
                }
                className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6"
              >


                {/* ================================================= */}
                {/* LOCATION + STATUS                               */}
                {/* ================================================= */}

                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">


                  {/* LOCATION */}

                  <div>

                    <div className="flex items-center gap-3">

                      <div className="p-2.5 bg-blue-50 rounded-xl">

                        <MapPin
                          size={21}
                          className="text-blue-600"
                        />

                      </div>


                      <div>

                        <div className="flex items-center gap-2">

                          <h3 className="text-lg font-bold text-slate-800">
                            {automation.state}
                          </h3>

                          <span className="text-slate-400">
                            →
                          </span>

                          <span className="font-semibold text-indigo-600">
                            {automation.jc}
                          </span>

                        </div>


                        <div className="flex items-center gap-2 mt-1">

                          <p className="text-sm text-slate-500">
                            Daily neighbour validation
                          </p>

                          <span className="text-slate-300">
                            •
                          </span>

                          <span className="text-xs font-semibold text-blue-600">

                            {
                              automation.technologyFlow ===
                              "4G_TO_5G"
                                ? "4G → 5G"
                                : "5G → 4G"
                            }

                          </span>

                        </div>

                      </div>

                    </div>

                  </div>


                  {/* STATUS */}

                  <div>

                    {automation.status ===
                      "RUNNING" && (

                      <span className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 border border-green-100 rounded-full text-sm font-semibold">

                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />

                        RUNNING

                      </span>

                    )}


                    {automation.status ===
                      "PAUSED" && (

                      <span className="inline-flex items-center gap-2 px-4 py-2 bg-amber-50 text-amber-700 border border-amber-100 rounded-full text-sm font-semibold">

                        <span className="w-2 h-2 bg-amber-500 rounded-full" />

                        PAUSED

                      </span>

                    )}


                    {automation.status ===
                      "ENDED" && (

                      <span className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-600 border border-slate-200 rounded-full text-sm font-semibold">

                        <span className="w-2 h-2 bg-slate-400 rounded-full" />

                        ENDED

                      </span>

                    )}

                  </div>

                </div>


                {/* ================================================= */}
                {/* DETAILS                                         */}
                {/* ================================================= */}

                <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">


                  {/* TECHNOLOGY FLOW */}

                  <div className="p-4 bg-blue-50 rounded-xl">

                    <div className="flex items-center gap-2 text-blue-600">

                      <ArrowRightLeft
                        size={16}
                      />

                      <span className="text-xs font-medium">
                        Technology Flow
                      </span>

                    </div>


                    <p className="text-lg font-bold text-slate-800 mt-2">

                      {
                        automation.technologyFlow ===
                        "4G_TO_5G"
                          ? "4G → 5G"
                          : "5G → 4G"
                      }

                    </p>

                  </div>


                  {/* TIME */}

                  <div className="p-4 bg-slate-50 rounded-xl">

                    <div className="flex items-center gap-2 text-slate-500">

                      <Clock size={16} />

                      <span className="text-xs font-medium">
                        Execution Time
                      </span>

                    </div>


                    <p className="text-lg font-bold text-slate-800 mt-2">

                      {formatTime(
                        automation.time
                      )}

                    </p>

                  </div>


                  {/* FREQUENCY */}

                  <div className="p-4 bg-slate-50 rounded-xl">

                    <div className="flex items-center gap-2 text-slate-500">

                      <CalendarDays
                        size={16}
                      />

                      <span className="text-xs font-medium">
                        Frequency
                      </span>

                    </div>


                    <p className="text-lg font-bold text-slate-800 mt-2">
                      {formatFrequency(
                        automation.frequency
                      )}
                    </p>

                  </div>


                  {/* MINIMUM NEIGHBOURS */}

                  <div className="p-4 bg-green-50 rounded-xl">

                    <div className="flex items-center gap-2 text-green-600">

                      <ShieldCheck
                        size={16}
                      />

                      <span className="text-xs font-medium">
                        Minimum Neighbours
                      </span>

                    </div>


                    <p className="text-lg font-bold text-slate-800 mt-2">
                      {automation.minimumNeighbours}
                    </p>

                  </div>


                  {/* LAST RUN */}

                  <div className="p-4 bg-slate-50 rounded-xl">

                    <p className="text-xs font-medium text-slate-500">
                      Last Run
                    </p>


                    <p className="text-sm font-semibold text-slate-800 mt-2">
                      {automation.lastRun}
                    </p>

                  </div>


                  {/* NEXT RUN */}

                  <div className="p-4 bg-slate-50 rounded-xl">

                    <p className="text-xs font-medium text-slate-500">
                      Next Run
                    </p>


                    <p className="text-sm font-semibold text-slate-800 mt-2">
                      {automation.nextRun}
                    </p>

                  </div>

                </div>


                {/* ================================================= */}
                {/* RULES                                            */}
                {/* ================================================= */}

                <div className="mt-5 flex flex-wrap items-center gap-2">

                  <span className="text-xs font-semibold text-slate-500 mr-2">
                    Rules:
                  </span>


                  {(automation.rules || []).map(
                    (rule) => (

                      <span
                        key={rule}
                        className={
                          rule ===
                          "PCI"

                            ? "px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold"

                            : rule ===
                              "TAC"

                            ? "px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-xs font-semibold"

                            : rule ===
                              "Source"

                            ? "px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-xs font-semibold"

                            : "px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-semibold"
                        }
                      >

                        {rule}

                      </span>

                    )
                  )}

                </div>


                {/* ================================================= */}
                {/* ACTIONS                                          */}
                {/* ================================================= */}

                <div className="mt-6 pt-5 border-t border-slate-100 flex flex-wrap gap-3">


                  {/* PAUSE */}

                  {automation.status ===
                    "RUNNING" && (

                    <button
                      type="button"
                      onClick={() =>
                        handlePause(
                          automation.id
                        )
                      }
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-amber-50 hover:bg-amber-100 text-amber-700 font-semibold rounded-xl transition"
                    >

                      <Pause size={17} />

                      Pause

                    </button>

                  )}


                  {/* RESUME */}

                  {automation.status ===
                    "PAUSED" && (

                    <button
                      type="button"
                      onClick={() =>
                        handleResume(
                          automation.id
                        )
                      }
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-green-50 hover:bg-green-100 text-green-700 font-semibold rounded-xl transition"
                    >

                      <Play size={17} />

                      Resume

                    </button>

                  )}


                  {/* END */}

                  {automation.status !==
                    "ENDED" && (

                    <button
                      type="button"
                      onClick={() =>
                        handleEnd(
                          automation.id
                        )
                      }
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-red-50 hover:bg-red-100 text-red-700 font-semibold rounded-xl transition"
                    >

                      <Square size={16} />

                      End Automation

                    </button>

                  )}


                  {/* DELETE */}

                  <button
                    type="button"
                    onClick={() =>
                      setDeleteId(
                        automation.id
                      )
                    }
                    className="inline-flex items-center gap-2 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-xl transition"
                  >

                    <Trash2 size={16} />

                    Delete Permanently

                  </button>

                </div>


                {/* ================================================= */}
                {/* ACTIVE MESSAGE                                   */}
                {/* ================================================= */}

                {automation.status ===
                  "RUNNING" && (

                  <div className="mt-5 flex items-center gap-2 text-xs text-slate-500">

                    <ShieldCheck
                      size={15}
                      className="text-green-600"
                    />

                    Automation is active and scheduled
                    to run daily.

                  </div>

                )}

              </div>

            )
          )

        )}

      </div>


      {/* ================================================= */}
      {/* DELETE MODAL                                     */}
      {/* ================================================= */}

      {deleteId && (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-5">

          <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">


            <div className="flex items-start gap-4">

              <div className="p-3 bg-red-50 rounded-xl">

                <Trash2
                  size={23}
                  className="text-red-600"
                />

              </div>


              <div>

                <h2 className="text-xl font-bold text-slate-800">
                  Delete Automation?
                </h2>

                <p className="text-sm text-slate-500 mt-2 leading-6">

                  This will permanently remove the automation
                  schedule. It will no longer run and its
                  configuration will be deleted.

                </p>

              </div>

            </div>


            <div className="flex justify-end gap-3 mt-7">

              <button
                type="button"
                onClick={() =>
                  setDeleteId(
                    null
                  )
                }
                className="px-5 py-2.5 border border-slate-300 text-slate-700 font-semibold rounded-xl hover:bg-slate-50"
              >

                Cancel

              </button>


              <button
                type="button"
                onClick={
                  handleDelete
                }
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl"
              >

                <Trash2 size={16} />

                Delete Permanently

              </button>

            </div>

          </div>

        </div>

      )}

    </div>

  );

}


// ======================================================
// TECHNOLOGY FLOW CONVERSION
// ======================================================

function normalizeTechnologyFlow(
  value
) {

  if (
    value === "FOUR_G_TO_FIVE_G" ||
    value === "4G_TO_5G"
  ) {

    return "4G_TO_5G";

  }


  if (
    value === "FIVE_G_TO_FOUR_G" ||
    value === "5G_TO_4G"
  ) {

    return "5G_TO_4G";

  }


  return "4G_TO_5G";

}


function toBackendTechnologyFlow(
  value
) {

  if (value === "5G_TO_4G") {

    return "FIVE_G_TO_FOUR_G";

  }


  return "FOUR_G_TO_FIVE_G";

}


// ======================================================
// NORMALIZE BACKEND TIME
// ======================================================

function normalizeTime(time) {

  if (!time) {

    return "";

  }

  return String(time)
    .substring(0, 5);

}


// ======================================================
// FORMAT BACKEND DATE/TIME
// ======================================================

function formatDateTime(value) {

  if (!value) {

    return "";

  }


  const date =
    new Date(value);


  if (Number.isNaN(
    date.getTime()
  )) {

    return String(value);

  }


  return date.toLocaleString(
    "en-IN",
    {
      dateStyle: "medium",
      timeStyle: "short",
    }
  );

}


// ======================================================
// FORMAT FREQUENCY
// ======================================================

function formatFrequency(
  frequency
) {

  if (!frequency) {

    return "Daily";

  }


  return String(frequency)
    .toLowerCase()
    .replace(
      /^./,
      (character) =>
        character.toUpperCase()
    );

}


// ======================================================
// FORMAT TIME
// ======================================================

function formatTime(time) {

  if (!time) {

    return "";

  }


  const [hour, minute] =
    time.split(":");


  const date = new Date();

  date.setHours(
    Number(hour),
    Number(minute)
  );


  return date.toLocaleTimeString(
    "en-IN",
    {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    }
  );

}


export default Automation;
