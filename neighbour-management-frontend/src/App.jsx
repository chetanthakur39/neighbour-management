import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Sidebar from "./components/layout/Sidebar";
import Navbar from "./components/layout/Navbar";
import FloatingChatbot from "./components/FloatingChatbot";

import Automation from "./pages/Automation";
import { ValidationProvider } from "./context/ValidationContext";

import Dashboard from "./pages/Dashboard";
import Neighbours from "./pages/Neighbours";
import NeighbourDetails from "./pages/NeighbourDetails";
import Validation from "./pages/Validation";

import Enodes from "./pages/Enodes";
import ECells from "./pages/ECells";

import Gnodes from "./pages/Gnodes";
import GCells from "./pages/GCells";

import FourGConfiguration from "./pages/FourGConfiguration";
import FiveGConfiguration from "./pages/FiveGConfiguration";

import Reports from "./pages/Reports";


function App() {

  return (

    <BrowserRouter>

      <ValidationProvider>

        {/* ================================================= */}
        {/* MAIN APPLICATION LAYOUT                           */}
        {/* ================================================= */}

        <div className="min-h-screen bg-slate-100 flex">


          {/* ================================================= */}
          {/* SIDEBAR                                           */}
          {/* ================================================= */}

          <Sidebar />


          {/* ================================================= */}
          {/* RIGHT SIDE                                        */}
          {/* ================================================= */}

          <div className="flex-1 flex flex-col">


            {/* ================================================= */}
            {/* NAVBAR                                            */}
            {/* ================================================= */}

            <Navbar />


            {/* ================================================= */}
            {/* PAGE CONTENT                                      */}
            {/* ================================================= */}

            <main className="flex-1 p-6 overflow-auto">

              <Routes>


                {/* ================================================= */}
                {/* DEFAULT ROUTE                                    */}
                {/* ================================================= */}

                <Route
                  path="/"
                  element={
                    <Navigate
                      to="/dashboard"
                      replace
                    />
                  }
                />


                {/* ================================================= */}
                {/* DASHBOARD                                        */}
                {/* ================================================= */}

                <Route
                  path="/dashboard"
                  element={<Dashboard />}
                />


                {/* ================================================= */}
                {/* NEIGHBOURS                                       */}
                {/* ================================================= */}

                <Route
                  path="/neighbours"
                  element={<Neighbours />}
                />


                {/* ================================================= */}
                {/* NEIGHBOUR DETAILS                                */}
                {/* ================================================= */}

                <Route
                  path="/neighbours/:id"
                  element={<NeighbourDetails />}
                />


                {/* ================================================= */}
                {/* VALIDATION                                       */}
                {/* ================================================= */}

                <Route
                  path="/validation"
                  element={<Validation />}
                />


                {/* ================================================= */}
                {/* AUTOMATION                                       */}
                {/* ================================================= */}

                <Route
                  path="/automation"
                  element={<Automation />}
                />


                {/* ================================================= */}
                {/* 4G NETWORK                                       */}
                {/* ================================================= */}

                <Route
                  path="/4g/enodes"
                  element={<Enodes />}
                />

                <Route
                  path="/4g/ecells"
                  element={<ECells />}
                />

                <Route
                  path="/4g/configuration"
                  element={<FourGConfiguration />}
                />


                {/* ================================================= */}
                {/* 5G NETWORK                                       */}
                {/* ================================================= */}

                <Route
                  path="/5g/gnodes"
                  element={<Gnodes />}
                />

                <Route
                  path="/5g/gcells"
                  element={<GCells />}
                />

                <Route
                  path="/5g/configuration"
                  element={<FiveGConfiguration />}
                />


                {/* ================================================= */}
                {/* REPORTS                                          */}
                {/* ================================================= */}

                <Route
                  path="/reports"
                  element={<Reports />}
                />


              </Routes>

            </main>

          </div>


          {/* ================================================= */}
          {/* GLOBAL FLOATING AI CHATBOT                       */}
          {/* ================================================= */}
          {/*
             This is intentionally outside <Routes>.

             Therefore the chatbot is available globally on:

             Dashboard
             Neighbours
             Validation
             Automation
             4G
             5G
             Reports
             etc.
          */}

          <FloatingChatbot />


        </div>

      </ValidationProvider>

    </BrowserRouter>

  );

}


export default App;