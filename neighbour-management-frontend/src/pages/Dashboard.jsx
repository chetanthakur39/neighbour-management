import { useEffect, useMemo, useState } from "react";
import { API_BASE_URL } from "../config";

import {
  AlertTriangle,
  MapPin,
  Activity,
  Trash2,
  CalendarDays,
  ShieldCheck,
  TrendingDown,
  Clock,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Bot,
  Send,
} from "lucide-react";


// ======================================================
// API
// ======================================================




// ======================================================
// DASHBOARD
// ======================================================

function Dashboard() {

  // ====================================================
  // DATA
  // ====================================================

  const [automations, setAutomations] =
    useState([]);

  const [executions, setExecutions] =
    useState([]);

  const [deletionHistory, setDeletionHistory] =
    useState([]);

  const [dailyDeletionTotal, setDailyDeletionTotal] =
    useState(0);

  const [loading, setLoading] =
    useState(true);

  const [refreshing, setRefreshing] =
    useState(false);

  const [error, setError] =
    useState("");


  // ====================================================
  // CHATBOT STATE
  // ====================================================

  const [chatMessage, setChatMessage] =
    useState("");

  const [chatMessages, setChatMessages] =
    useState([
      {
        role: "assistant",
        text:
          "Hello! I am the Neighbour Management AI. You can enter commands such as: Validate neighbours in Odisha JC_Bhubaneswar",
      },
    ]);

  const [chatLoading, setChatLoading] =
    useState(false);

  const [chatError, setChatError] =
    useState("");


  // ====================================================
  // LOAD DASHBOARD DATA
  // ====================================================

  useEffect(() => {

    loadDashboardData();

  }, []);


  const loadDashboardData = async () => {

    try {

      setLoading(true);
      setError("");


      // ==================================================
      // 1. GET ALL AUTOMATIONS
      // ==================================================

      const automationResponse =
        await fetch(
          `${API_BASE_URL}/automations`
        );


      if (!automationResponse.ok) {

        throw new Error(
          `Failed to load automations (${automationResponse.status})`
        );

      }


      const automationData =
        await automationResponse.json();


      const automationList =
        Array.isArray(automationData)
          ? automationData
          : [];


      setAutomations(
        automationList
      );


      // ==================================================
      // 2. GET EXECUTIONS FOR EVERY AUTOMATION
      // ==================================================

      const executionResults =
        await Promise.all(

          automationList.map(
            async (automation) => {

              const automationId =
                automation.automationId;


              if (!automationId) {

                return [];

              }


              try {

                const response =
                  await fetch(
                    `${API_BASE_URL}/automation-executions/automation/${automationId}`
                  );


                if (!response.ok) {

                  console.error(
                    `Failed to load executions for automation ${automationId}`
                  );

                  return [];

                }


                const data =
                  await response.json();


                return Array.isArray(data)
                  ? data
                  : [];

              } catch (error) {

                console.error(
                  `Execution loading failed for automation ${automationId}:`,
                  error
                );

                return [];

              }

            }
          )

        );


      // ==================================================
      // 3. FLATTEN EXECUTIONS
      // ==================================================

      const allExecutions =
        executionResults.flat();


      // ==================================================
      // 4. REMOVE DUPLICATE EXECUTIONS
      // ==================================================

      const uniqueExecutions =
        Array.from(
          new Map(
            allExecutions.map(
              (execution, index) => [

                execution.executionId ??
                  `execution-${index}`,

                execution,

              ]
            )
          ).values()
        );


      // ==================================================
      // 5. SORT NEWEST FIRST
      // ==================================================

      uniqueExecutions.sort(
        (a, b) => {

          const dateA =
            parseDate(a.startedAt);

          const dateB =
            parseDate(b.startedAt);

          return dateB - dateA;

        }
      );


      setExecutions(
        uniqueExecutions
      );


      // ==================================================
      // 6. GET DELETION HISTORY
      //
      // This contains BOTH:
      //
      // CHATBOT
      // AUTOMATION
      //
      // deletions.
      // ==================================================

      const deletionHistoryResponse =
        await fetch(
          `${API_BASE_URL}/deletion/history`
        );


      if (!deletionHistoryResponse.ok) {

        throw new Error(
          `Failed to load deletion history (${deletionHistoryResponse.status})`
        );

      }


      const deletionHistoryData =
        await deletionHistoryResponse.json();


      const historyList =
        Array.isArray(deletionHistoryData)
          ? deletionHistoryData
          : [];


      setDeletionHistory(
        historyList
      );


      // ==================================================
      // 7. GET TODAY'S REAL DELETION TOTAL
      // ==================================================

      const dailyTotalResponse =
        await fetch(
          `${API_BASE_URL}/deletion/history/daily-total`
        );


      if (!dailyTotalResponse.ok) {

        throw new Error(
          `Failed to load daily deletion total (${dailyTotalResponse.status})`
        );

      }


      const dailyTotalData =
        await dailyTotalResponse.json();


      setDailyDeletionTotal(
        toNumber(
          dailyTotalData.deletedCount
        )
      );


    } catch (error) {

      console.error(
        "Dashboard loading failed:",
        error
      );


      setError(
        error.message ||
        "Unable to load dashboard data."
      );


    } finally {

      setLoading(false);
      setRefreshing(false);

    }

  };


  // ====================================================
  // REFRESH
  // ====================================================

  const handleRefresh = async () => {

    setRefreshing(true);

    await loadDashboardData();

  };


  // ====================================================
  // TODAY
  // ====================================================

  const today = new Date();

  const todayLabel =
    today.toLocaleDateString(
      "en-IN",
      {
        weekday: "long",
        day: "2-digit",
        month: "short",
        year: "numeric",
      }
    );


  // ====================================================
  // TODAY EXECUTIONS
  // ====================================================

  const todayExecutions =
    useMemo(
      () => {

        return executions.filter(
          (execution) =>
            isSameDay(
              execution.startedAt,
              today
            )
        );

      },
      [executions]
    );


  // ====================================================
  // SUMMARY
  // ====================================================

  const summaryData =
    useMemo(
      () => {

        // ---------------------------------------------
        // Invalid neighbours found
        // ---------------------------------------------

        const totalInvalidNeighbours =
          executions.reduce(
            (
              total,
              execution
            ) =>
              total +
              toNumber(
                execution.invalidCount
              ),
            0
          );


        // ---------------------------------------------
        // Affected states
        // ---------------------------------------------

        const affectedStates =
          new Set(
            executions
              .filter(
                (execution) =>
                  toNumber(
                    execution.invalidCount
                  ) > 0
              )
              .map(
                (execution) =>
                  execution.state
              )
              .filter(Boolean)
          ).size;


        // ---------------------------------------------
        // Affected JCs
        // ---------------------------------------------

        const affectedJCs =
          new Set(
            executions
              .filter(
                (execution) =>
                  toNumber(
                    execution.invalidCount
                  ) > 0
              )
              .map(
                (execution) =>
                  execution.jc
              )
              .filter(Boolean)
          ).size;


        return {

          totalInvalidNeighbours,

          affectedStates,

          affectedJCs,

        };

      },
      [executions]
    );


  // ====================================================
  // INVALID NEIGHBOURS BY LOCATION
  // ====================================================

  const invalidLocations =
    useMemo(
      () => {

        const locationMap =
          new Map();


        executions.forEach(
          (execution) => {

            const invalid =
              toNumber(
                execution.invalidCount
              );


            if (
              invalid <= 0
            ) {

              return;

            }


            const state =
              execution.state ||
              "Unknown State";


            const jc =
              execution.jc ||
              "Unknown JC";


            const key =
              `${state}|||${jc}`;


            if (
              !locationMap.has(key)
            ) {

              locationMap.set(
                key,
                {

                  state,

                  jc,

                  invalidCount: 0,

                  runs: 0,

                }
              );

            }


            const location =
              locationMap.get(key);


            location.invalidCount +=
              invalid;


            location.runs += 1;

          }
        );


        return Array.from(
          locationMap.values()
        ).sort(
          (
            a,
            b
          ) =>
            b.invalidCount -
            a.invalidCount
        );

      },
      [executions]
    );


  // ====================================================
  // DAILY DELETION HISTORY
  //
  // IMPORTANT:
  //
  // This now uses deletion_history.
  //
  // Therefore:
  //
  // CHATBOT deletions
  // +
  // AUTOMATION deletions
  //
  // are both included.
  // ====================================================

  const dailyDeletionHistory =
    useMemo(
      () => {

        const dayMap =
          new Map();


        deletionHistory.forEach(
          (history) => {

            if (
              !history.deletedAt
            ) {

              return;

            }


            const date =
              parseDate(
                history.deletedAt
              );


            if (
              Number.isNaN(
                date.getTime()
              )
            ) {

              return;

            }


            const key =
              getDateKey(date);


            if (
              !dayMap.has(key)
            ) {

              dayMap.set(
                key,
                {

                  date,

                  deleted: 0,

                  records: 0,

                  chatbotDeleted: 0,

                  automationDeleted: 0,

                }
              );

            }


            const item =
              dayMap.get(key);


            const deletedCount =
              toNumber(
                history.deletedCount
              );


            item.deleted +=
              deletedCount;


            item.records += 1;


            if (
              String(
                history.source
              ).toUpperCase() ===
              "CHATBOT"
            ) {

              item.chatbotDeleted +=
                deletedCount;

            }


            if (
              String(
                history.source
              ).toUpperCase() ===
              "AUTOMATION"
            ) {

              item.automationDeleted +=
                deletedCount;

            }

          }
        );


        return Array.from(
          dayMap.values()
        )
          .sort(
            (
              a,
              b
            ) =>
              b.date - a.date
          )
          .slice(
            0,
            7
          )
          .map(
            (item) => ({

              day:
                item.date.toLocaleDateString(
                  "en-IN",
                  {
                    weekday: "long",
                  }
                ),

              date:
                formatDisplayDate(
                  item.date
                ),

              deleted:
                item.deleted,

              runs:
                item.records,

              chatbotDeleted:
                item.chatbotDeleted,

              automationDeleted:
                item.automationDeleted,

            })
          );

      },
      [deletionHistory]
    );


  // ====================================================
  // RECENT AUTOMATION ACTIVITY
  // ====================================================

  const recentActivity =
    useMemo(
      () => {

        return executions
          .slice(
            0,
            10
          )
          .map(
            (execution) => {

              const date =
                parseDate(
                  execution.startedAt
                );


              return {

                executionId:
                  execution.executionId,

                time:
                  formatTimeFromDate(
                    date
                  ),

                date:
                  formatDisplayDate(
                    date
                  ),

                state:
                  execution.state ||
                  "Unknown",

                jc:
                  execution.jc ||
                  "Unknown",

                checked:
                  toNumber(
                    execution.totalChecked
                  ),

                valid:
                  toNumber(
                    execution.validCount
                  ),

                invalid:
                  toNumber(
                    execution.invalidCount
                  ),

                deleted:
                  toNumber(
                    execution.deletedCount
                  ),

                retained:
                  toNumber(
                    execution.retainedCount
                  ),

                status:
                  execution.status ||
                  "UNKNOWN",

              };

            }
          );

      },
      [executions]
    );


  // ====================================================
  // SEND CHATBOT COMMAND
  //
  // IMPORTANT:
  //
  // Your current Python AI is a terminal application.
  // It does not currently expose an HTTP endpoint.
  //
  // Therefore this function does NOT pretend there is
  // an AI API.
  //
  // Once we create the Python HTTP endpoint, only this
  // function needs to be connected.
  // ====================================================

  const handleChatSubmit = async (event) => {

    event.preventDefault();


    const command =
      chatMessage.trim();


    if (!command) {

      return;

    }


    setChatMessages(
      (previous) => [

        ...previous,

        {
          role: "user",
          text: command,
        },

      ]
    );


    setChatMessage("");

    setChatError("");

    setChatLoading(true);


    try {

      // ------------------------------------------------
      // AI HTTP ENDPOINT WILL BE CONNECTED HERE.
      //
      // Example future endpoint:
      //
      // POST http://localhost:8000/chat
      //
      // Do NOT uncomment until the Python AI exposes
      // this endpoint.
      // ------------------------------------------------

      throw new Error(
        "AI chatbot API is not connected yet. The current Python AI runs in the terminal. We will connect the dashboard to the AI HTTP API in the next step."
      );


    } catch (error) {

      console.error(
        "Chatbot request failed:",
        error
      );


      const message =
        error.message ||
        "Unable to process chatbot command.";


      setChatError(
        message
      );


      setChatMessages(
        (previous) => [

          ...previous,

          {
            role: "assistant",
            text: message,
            error: true,
          },

        ]
      );


    } finally {

      setChatLoading(false);

    }

  };


  // ====================================================
  // LOADING
  // ====================================================

  if (loading) {

    return (

      <div className="max-w-7xl mx-auto">

        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center">

          <div className="mx-auto w-9 h-9 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />

          <p className="mt-4 text-sm font-semibold text-slate-600">

            Loading dashboard data...

          </p>

          <p className="mt-1 text-xs text-slate-400">

            Reading automations, execution results and
            deletion history from Spring Boot.

          </p>

        </div>

      </div>

    );

  }


  // ====================================================
  // PAGE
  // ====================================================

  return (

    <div className="max-w-7xl mx-auto space-y-7">


      {/* ================================================= */}
      {/* ERROR                                            */}
      {/* ================================================= */}

      {error && (

        <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-xl">

          <AlertTriangle
            size={20}
            className="text-red-600 mt-0.5"
          />


          <div className="flex-1">

            <p className="text-sm font-semibold text-red-800">

              Dashboard Error

            </p>


            <p className="text-sm text-red-700 mt-1">

              {error}

            </p>

          </div>


          <button
            type="button"
            onClick={
              handleRefresh
            }
            className="inline-flex items-center gap-2 px-3 py-2 bg-white border border-red-200 text-red-700 rounded-lg text-xs font-semibold hover:bg-red-50"
          >

            <RefreshCw
              size={14}
            />

            Retry

          </button>

        </div>

      )}


      {/* ================================================= */}
      {/* HEADER                                           */}
      {/* ================================================= */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <div>

          <div className="flex items-center gap-3">

            <div className="p-3 bg-blue-50 rounded-xl">

              <Activity
                size={27}
                className="text-blue-600"
              />

            </div>


            <div>

              <h1 className="text-3xl font-bold text-slate-800">

                Dashboard

              </h1>


              <p className="text-slate-500 mt-1">

                Monitor neighbour validation,
                automation and deletion activity.

              </p>

            </div>

          </div>

        </div>


        {/* TODAY + REFRESH */}

        <div className="flex items-center gap-3">

          <button
            type="button"
            onClick={
              handleRefresh
            }
            disabled={refreshing}
            className="inline-flex items-center gap-2 px-3 py-2.5 bg-white border border-slate-200 rounded-xl shadow-sm text-sm font-semibold text-slate-600 hover:bg-slate-50 disabled:opacity-50"
          >

            <RefreshCw
              size={16}
              className={
                refreshing
                  ? "animate-spin"
                  : ""
              }
            />

            Refresh

          </button>


          <div className="flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-200 rounded-xl shadow-sm">

            <CalendarDays
              size={18}
              className="text-blue-600"
            />


            <div>

              <p className="text-xs text-slate-400">
                Today
              </p>


              <p className="text-sm font-semibold text-slate-700">

                {todayLabel}

              </p>

            </div>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* SUMMARY CARDS                                    */}
      {/* ================================================= */}

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">


        {/* INVALID */}

        <div className="bg-white border border-red-100 rounded-2xl p-5 shadow-sm">

          <div className="flex items-start justify-between">

            <div>

              <p className="text-sm font-medium text-slate-500">

                Invalid Neighbours Found

              </p>


              <p className="text-3xl font-bold text-slate-800 mt-2">

                {summaryData.totalInvalidNeighbours}

              </p>


              <p className="text-xs text-red-600 mt-2 flex items-center gap-1">

                <AlertTriangle size={13} />

                From recorded executions

              </p>

            </div>


            <div className="p-3 bg-red-50 rounded-xl">

              <AlertTriangle
                size={23}
                className="text-red-600"
              />

            </div>

          </div>

        </div>


        {/* STATES */}

        <div className="bg-white border border-blue-100 rounded-2xl p-5 shadow-sm">

          <div className="flex items-start justify-between">

            <div>

              <p className="text-sm font-medium text-slate-500">

                Affected States

              </p>


              <p className="text-3xl font-bold text-slate-800 mt-2">

                {summaryData.affectedStates}

              </p>


              <p className="text-xs text-blue-600 mt-2 flex items-center gap-1">

                <MapPin size={13} />

                States with invalid results

              </p>

            </div>


            <div className="p-3 bg-blue-50 rounded-xl">

              <MapPin
                size={23}
                className="text-blue-600"
              />

            </div>

          </div>

        </div>


        {/* JCs */}

        <div className="bg-white border border-purple-100 rounded-2xl p-5 shadow-sm">

          <div className="flex items-start justify-between">

            <div>

              <p className="text-sm font-medium text-slate-500">

                Affected Jio Centers

              </p>


              <p className="text-3xl font-bold text-slate-800 mt-2">

                {summaryData.affectedJCs}

              </p>


              <p className="text-xs text-purple-600 mt-2 flex items-center gap-1">

                <Activity size={13} />

                JCs with invalid results

              </p>

            </div>


            <div className="p-3 bg-purple-50 rounded-xl">

              <Activity
                size={23}
                className="text-purple-600"
              />

            </div>

          </div>

        </div>


        {/* DELETED TODAY */}

        <div className="bg-white border border-green-100 rounded-2xl p-5 shadow-sm">

          <div className="flex items-start justify-between">

            <div>

              <p className="text-sm font-medium text-slate-500">

                Deleted Today

              </p>


              <p className="text-3xl font-bold text-slate-800 mt-2">

                {dailyDeletionTotal}

              </p>


              <p className="text-xs text-green-600 mt-2 flex items-center gap-1">

                <TrendingDown size={13} />

                Chatbot + automation deletions

              </p>

            </div>


            <div className="p-3 bg-green-50 rounded-xl">

              <Trash2
                size={23}
                className="text-green-600"
              />

            </div>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* INVALID NEIGHBOURS BY LOCATION                   */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

        <div className="p-6 border-b border-slate-100">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-red-50 rounded-xl">

              <AlertTriangle
                size={21}
                className="text-red-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">

                Invalid Neighbours by Location

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Invalid neighbours recorded by automation
                executions.

              </p>

            </div>

          </div>

        </div>


        <div className="overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="bg-slate-50 border-b border-slate-200">

                <th className="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  State
                </th>


                <th className="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Jio Center
                </th>


                <th className="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Invalid Neighbours
                </th>


                <th className="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Executions
                </th>


                <th className="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Status
                </th>

              </tr>

            </thead>


            <tbody>

              {invalidLocations.length ===
              0 ? (

                <tr>

                  <td
                    colSpan="5"
                    className="px-6 py-10 text-center text-sm text-slate-500"
                  >

                    No invalid neighbours have been
                    recorded by an automation execution.

                  </td>

                </tr>

              ) : (

                invalidLocations.map(
                  (
                    location,
                    index
                  ) => (

                    <tr
                      key={`${location.state}-${location.jc}-${index}`}
                      className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition"
                    >

                      <td className="px-6 py-4">

                        <div className="flex items-center gap-2">

                          <MapPin
                            size={16}
                            className="text-blue-500"
                          />

                          <span className="font-medium text-slate-700">

                            {location.state}

                          </span>

                        </div>

                      </td>


                      <td className="px-6 py-4">

                        <span className="font-semibold text-indigo-600">

                          {location.jc}

                        </span>

                      </td>


                      <td className="px-6 py-4 text-right">

                        <span className="text-lg font-bold text-red-600">

                          {location.invalidCount}

                        </span>

                      </td>


                      <td className="px-6 py-4 text-right">

                        <span className="text-sm font-semibold text-slate-600">

                          {location.runs}

                        </span>

                      </td>


                      <td className="px-6 py-4 text-right">

                        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-50 text-red-700 rounded-full text-xs font-semibold">

                          <span className="w-1.5 h-1.5 bg-red-500 rounded-full" />

                          Invalid Found

                        </span>

                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>


      {/* ================================================= */}
      {/* DAILY DELETION HISTORY                           */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-green-50 rounded-xl">

              <Trash2
                size={21}
                className="text-green-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">

                Daily Deletion History

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Total neighbours permanently deleted
                day and date wise.

              </p>

            </div>

          </div>


          <div className="flex items-center gap-2 px-3 py-2 bg-green-50 text-green-700 rounded-lg text-xs font-semibold">

            <ShieldCheck size={15} />

            Permanent deletion activity

          </div>

        </div>


        <div className="overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="bg-slate-50 border-b border-slate-200">

                <th className="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Day
                </th>


                <th className="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Date
                </th>


                <th className="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Neighbours Deleted
                </th>


                <th className="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Automation Runs
                </th>

              </tr>

            </thead>


            <tbody>

              {dailyDeletionHistory.length ===
              0 ? (

                <tr>

                  <td
                    colSpan="4"
                    className="px-6 py-10 text-center text-sm text-slate-500"
                  >

                    No deletion history available.

                  </td>

                </tr>

              ) : (

                dailyDeletionHistory.map(
                  (
                    item,
                    index
                  ) => (

                    <tr
                      key={`${item.date}-${index}`}
                      className={`border-b border-slate-100 last:border-0 hover:bg-slate-50 transition ${
                        index === 0
                          ? "bg-green-50/30"
                          : ""
                      }`}
                    >

                      <td className="px-6 py-4">

                        <div className="flex items-center gap-3">

                          <div className="p-2 bg-slate-100 rounded-lg">

                            <CalendarDays
                              size={16}
                              className="text-slate-500"
                            />

                          </div>


                          <span className="font-semibold text-slate-700">

                            {item.day}

                          </span>

                        </div>

                      </td>


                      <td className="px-6 py-4">

                        <span className="text-sm text-slate-600">

                          {item.date}

                        </span>

                      </td>


                      <td className="px-6 py-4 text-right">

                        <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 rounded-lg font-bold">

                          <Trash2 size={15} />

                          {item.deleted}

                        </span>

                      </td>


                      <td className="px-6 py-4 text-right">

                        <span className="inline-flex items-center gap-2 text-sm text-slate-600">

                          <Clock size={15} />

                          {item.runs}

                        </span>

                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>


      {/* ================================================= */}
      {/* DELETION SOURCE SUMMARY                          */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

        <div className="p-6 border-b border-slate-100">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-purple-50 rounded-xl">

              <Trash2
                size={21}
                className="text-purple-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">

                Deletion Source Summary

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Direct chatbot and automation deletions
                are included in the same deletion history.

              </p>

            </div>

          </div>

        </div>


        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-5">

          <div className="border border-blue-100 bg-blue-50/40 rounded-xl p-5">

            <div className="flex items-center justify-between">

              <div>

                <p className="text-sm font-medium text-slate-500">

                  Chatbot Deletions

                </p>


                <p className="text-3xl font-bold text-slate-800 mt-2">

                  {deletionHistory
                    .filter(
                      (item) =>
                        String(
                          item.source
                        ).toUpperCase() ===
                        "CHATBOT"
                    )
                    .reduce(
                      (
                        total,
                        item
                      ) =>
                        total +
                        toNumber(
                          item.deletedCount
                        ),
                      0
                    )}

                </p>

              </div>


              <div className="p-3 bg-blue-50 rounded-xl">

                <Bot
                  size={23}
                  className="text-blue-600"
                />

              </div>

            </div>

          </div>


          <div className="border border-purple-100 bg-purple-50/40 rounded-xl p-5">

            <div className="flex items-center justify-between">

              <div>

                <p className="text-sm font-medium text-slate-500">

                  Automation Deletions

                </p>


                <p className="text-3xl font-bold text-slate-800 mt-2">

                  {deletionHistory
                    .filter(
                      (item) =>
                        String(
                          item.source
                        ).toUpperCase() ===
                        "AUTOMATION"
                    )
                    .reduce(
                      (
                        total,
                        item
                      ) =>
                        total +
                        toNumber(
                          item.deletedCount
                        ),
                      0
                    )}

                </p>

              </div>


              <div className="p-3 bg-purple-50 rounded-xl">

                <Activity
                  size={23}
                  className="text-purple-600"
                />

              </div>

            </div>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* RECENT AUTOMATION ACTIVITY                       */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

        <div className="p-6 border-b border-slate-100">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-blue-50 rounded-xl">

              <Activity
                size={21}
                className="text-blue-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">

                Recent Automation Activity

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Latest validation and permanent deletion
                executions from the database.

              </p>

            </div>

          </div>

        </div>


        <div className="divide-y divide-slate-100">

          {recentActivity.length ===
          0 ? (

            <div className="p-10 text-center">

              <Activity
                size={35}
                className="mx-auto text-slate-300"
              />

              <p className="mt-4 text-sm font-semibold text-slate-600">

                No automation executions yet.

              </p>

              <p className="mt-1 text-xs text-slate-400">

                Execution results will appear here after
                an automation runs.

              </p>

            </div>

          ) : (

            recentActivity.map(
              (
                activity,
                index
              ) => (

                <div
                  key={
                    activity.executionId ??
                    `${activity.jc}-${activity.date}-${index}`
                  }
                  className="p-5 hover:bg-slate-50 transition"
                >

                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">


                    {/* LOCATION */}

                    <div className="flex items-start gap-3">

                      <div className="p-2.5 bg-blue-50 rounded-xl">

                        <MapPin
                          size={19}
                          className="text-blue-600"
                        />

                      </div>


                      <div>

                        <div className="flex items-center gap-2 flex-wrap">

                          <span className="font-bold text-slate-800">

                            {activity.jc}

                          </span>


                          <span className="text-slate-300">
                            •
                          </span>


                          <span className="text-sm text-slate-500">

                            {activity.state}

                          </span>

                        </div>


                        <div className="flex items-center gap-2 mt-1">

                          <Clock
                            size={13}
                            className="text-slate-400"
                          />


                          <span className="text-xs text-slate-500">

                            {activity.date}

                            {" • "}

                            {activity.time}

                          </span>

                        </div>

                      </div>

                    </div>


                    {/* STATS */}

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">

                      <div className="px-4 py-2.5 bg-slate-50 rounded-lg text-center">

                        <p className="text-xs text-slate-400">
                          Checked
                        </p>

                        <p className="font-bold text-slate-700 mt-1">

                          {activity.checked}

                        </p>

                      </div>


                      <div className="px-4 py-2.5 bg-blue-50 rounded-lg text-center">

                        <p className="text-xs text-blue-500">
                          Valid
                        </p>

                        <p className="font-bold text-blue-700 mt-1">

                          {activity.valid}

                        </p>

                      </div>


                      <div className="px-4 py-2.5 bg-red-50 rounded-lg text-center">

                        <p className="text-xs text-red-500">
                          Invalid
                        </p>

                        <p className="font-bold text-red-700 mt-1">

                          {activity.invalid}

                        </p>

                      </div>


                      <div className="px-4 py-2.5 bg-green-50 rounded-lg text-center">

                        <p className="text-xs text-green-600">
                          Deleted
                        </p>

                        <p className="font-bold text-green-700 mt-1">

                          {activity.deleted}

                        </p>

                      </div>

                    </div>


                    {/* STATUS */}

                    <div>

                      {activity.status ===
                        "SUCCESS" ? (

                        <span className="inline-flex items-center gap-2 px-3 py-2 bg-green-50 text-green-700 rounded-full text-xs font-semibold">

                          <CheckCircle2
                            size={15}
                          />

                          SUCCESS

                        </span>

                      ) : (

                        <span className="inline-flex items-center gap-2 px-3 py-2 bg-red-50 text-red-700 rounded-full text-xs font-semibold">

                          <XCircle
                            size={15}
                          />

                          {activity.status}

                        </span>

                      )}

                    </div>

                  </div>


                  {/* RETAINED */}

                  <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">

                    <ShieldCheck
                      size={14}
                      className="text-green-600"
                    />

                    Retained:

                    <span className="font-semibold text-slate-700">

                      {activity.retained}

                    </span>

                    neighbours

                  </div>

                </div>

              )
            )

          )}

        </div>

      </div>


      {/* ================================================= */}
      {/* CHATBOT                                          */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

        <div className="p-6 border-b border-slate-100">

          <div className="flex items-center gap-3">

            <div className="p-2.5 bg-blue-50 rounded-xl">

              <Bot
                size={21}
                className="text-blue-600"
              />

            </div>


            <div>

              <h2 className="text-xl font-semibold text-slate-800">

                Neighbour Management AI

              </h2>


              <p className="text-sm text-slate-500 mt-1">

                Validate neighbours, preview cleanup and
                start cleanup using natural language.

              </p>

            </div>

          </div>

        </div>


        {/* CHAT MESSAGES */}

        <div className="p-6 space-y-4 max-h-96 overflow-y-auto">

          {chatMessages.map(
            (
              message,
              index
            ) => (

              <div
                key={index}
                className={
                  message.role === "user"
                    ? "flex justify-end"
                    : "flex justify-start"
                }
              >

                <div
                  className={
                    message.role === "user"
                      ? "max-w-[80%] px-4 py-3 bg-blue-600 text-white rounded-2xl rounded-br-md text-sm"
                      : "max-w-[80%] px-4 py-3 bg-slate-50 border border-slate-200 text-slate-700 rounded-2xl rounded-bl-md text-sm"
                  }
                >

                  {message.text}

                </div>

              </div>

            )
          )}

          {chatLoading && (

            <div className="flex justify-start">

              <div className="px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl">

                <div className="flex gap-1">

                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />

                  <span
                    className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                    style={{
                      animationDelay: "150ms",
                    }}
                  />

                  <span
                    className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                    style={{
                      animationDelay: "300ms",
                    }}
                  />

                </div>

              </div>

            </div>

          )}

        </div>


        {/* CHAT ERROR */}

        {chatError && (

          <div className="mx-6 mb-4 p-3 bg-amber-50 border border-amber-200 rounded-xl">

            <p className="text-xs text-amber-700">

              {chatError}

            </p>

          </div>

        )}


        {/* CHAT INPUT */}

        <form
          onSubmit={
            handleChatSubmit
          }
          className="p-5 border-t border-slate-100"
        >

          <div className="flex gap-3">

            <input
              type="text"
              value={chatMessage}
              onChange={
                (event) =>
                  setChatMessage(
                    event.target.value
                  )
              }
              placeholder="Example: Validate neighbours in Odisha JC_Bhubaneswar"
              className="flex-1 px-4 py-3 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-400 text-sm text-slate-700"
              disabled={
                chatLoading
              }
            />


            <button
              type="submit"
              disabled={
                chatLoading ||
                !chatMessage.trim()
              }
              className="inline-flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl text-sm font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >

              <Send
                size={16}
              />

              Send

            </button>

          </div>


          <p className="mt-2 text-xs text-slate-400">

            Example: Start cleanup for Maharashtra
            JC_Mumbai with minimum retention of 2 neighbours

          </p>

        </form>

      </div>


      {/* ================================================= */}
      {/* AUTOMATION DATABASE INFO                         */}
      {/* ================================================= */}

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">

        <div className="flex items-start gap-3">

          <div className="p-2.5 bg-blue-50 rounded-xl">

            <Activity
              size={21}
              className="text-blue-600"
            />

          </div>


          <div>

            <p className="text-sm font-semibold text-slate-800">

              Database Monitoring

            </p>


            <p className="text-sm text-slate-500 mt-1">

              {automations.length} automation
              {automations.length === 1
                ? ""
                : "s"} registered and{" "}

              {executions.length} execution
              {executions.length === 1
                ? ""
                : "s"} recorded.

              {" "}

              {deletionHistory.length} deletion
              {deletionHistory.length === 1
                ? ""
                : "s"} recorded.

            </p>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* SAFETY INFORMATION                               */}
      {/* ================================================= */}

      <div className="flex items-start gap-3 p-5 bg-amber-50 border border-amber-200 rounded-2xl">

        <ShieldCheck
          size={21}
          className="text-amber-600 mt-0.5 flex-shrink-0"
        />


        <div>

          <p className="text-sm font-semibold text-amber-800">

            Neighbour Deletion Safety

          </p>


          <p className="text-sm text-amber-700 mt-1 leading-6">

            Invalid neighbours are permanently deleted only
            according to the configured validation rules.
            If all neighbours for a JC are invalid, the
            automation will retain the configured minimum
            number of neighbours and will never remove the
            entire neighbour set.

          </p>

        </div>

      </div>


    </div>

  );

}


// ======================================================
// HELPERS
// ======================================================

function toNumber(value) {

  const number =
    Number(value);

  return Number.isFinite(number)
    ? number
    : 0;

}


// ======================================================
// PARSE DATE
// ======================================================

function parseDate(value) {

  if (!value) {

    return new Date(
      "Invalid"
    );

  }


  const date =
    new Date(value);


  return date;

}


// ======================================================
// SAME DAY
// ======================================================

function isSameDay(
  value,
  targetDate
) {

  const date =
    parseDate(value);


  if (
    Number.isNaN(
      date.getTime()
    )
  ) {

    return false;

  }


  return (

    date.getFullYear() ===
      targetDate.getFullYear()

    &&

    date.getMonth() ===
      targetDate.getMonth()

    &&

    date.getDate() ===
      targetDate.getDate()

  );

}


// ======================================================
// DATE KEY
// ======================================================

function getDateKey(
  date
) {

  return [

    date.getFullYear(),

    String(
      date.getMonth() + 1
    ).padStart(2, "0"),

    String(
      date.getDate()
    ).padStart(2, "0"),

  ].join("-");

}


// ======================================================
// DISPLAY DATE
// ======================================================

function formatDisplayDate(
  value
) {

  const date =
    value instanceof Date
      ? value
      : parseDate(value);


  if (
    Number.isNaN(
      date.getTime()
    )
  ) {

    return "-";

  }


  return date.toLocaleDateString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }
  );

}


// ======================================================
// DISPLAY TIME
// ======================================================

function formatTimeFromDate(
  date
) {

  if (
    !date ||
    Number.isNaN(
      date.getTime()
    )
  ) {

    return "-";

  }


  return date.toLocaleTimeString(
    "en-IN",
    {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    }
  );

}


export default Dashboard;
