import { useRef, useState } from "react";
import { AI_CHAT_URL } from "../config";

import {
  Bot,
  X,
  Send,
  Minimize2,
} from "lucide-react";


// ======================================================
// FLOATING CHATBOT
// ======================================================

function FloatingChatbot() {

  const [isOpen, setIsOpen] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const sessionIdRef = useRef(
  `nm-ai-${Date.now()}-${Math.random().toString(36).slice(2)}`
);


  const [messages, setMessages] =
    useState([
      {
        role: "assistant",
        text:
          "Hello! I am the Neighbour Management AI. You can ask me to validate neighbours, preview cleanup, or start cleanup.",
      },
    ]);


  // ====================================================
  // SEND MESSAGE
  // ====================================================

  const handleSubmit = async (event) => {

    event.preventDefault();

    const command =
      message.trim();

    if (!command) {
      return;
    }


    // -----------------------------------------------
    // ADD USER MESSAGE
    // -----------------------------------------------

    setMessages(
      (previous) => [
        ...previous,

        {
          role: "user",
          text: command,
        },
      ]
    );


    setMessage("");

    setLoading(true);


    try {

      /*
       * =================================================
       * AI API CONNECTION
       * =================================================
       *
       * Your Python AI currently runs as:
       *
       *     python -m model.predict
       *
       * Once the Python AI HTTP endpoint is exposed,
       * replace the URL below with that endpoint.
       *
       * Example:
       *
       * POST http://localhost:8000/chat
       *
       * =================================================
       */

      const response =
        await fetch(
          AI_CHAT_URL,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              command: command,
               session_id: sessionIdRef.current,
            }),
          }
        );


      if (!response.ok) {

        throw new Error(
          `AI server returned ${response.status}`
        );

      }


      const data =
        await response.json();


      // -----------------------------------------------
      // AI RESPONSE
      // -----------------------------------------------

      const aiMessage =
        data.message ||
        data.response ||
        data.result ||
        "Command processed successfully.";


      setMessages(
        (previous) => [
          ...previous,

          {
            role: "assistant",
            text: aiMessage,
          },
        ]
      );


    } catch (error) {

      console.error(
        "Chatbot error:",
        error
      );


      setMessages(
        (previous) => [
          ...previous,

          {
            role: "assistant",
            text:
              "I could not connect to the AI server. Please make sure the Neighbour Management AI service is running.",
          },
        ]
      );


    } finally {

      setLoading(false);

    }

  };


  // ====================================================
  // FLOATING BUTTON
  // ====================================================

  return (

    <>

      {/* =================================================
          FLOATING AI BUTTON
      ================================================= */}

      {!isOpen && (

        <button
          type="button"
          onClick={() =>
            setIsOpen(true)
          }
          aria-label="Open Neighbour Management AI"
          className="
            fixed
            right-6
            bottom-6
            z-[9999]
            w-16
            h-16
            rounded-full
            bg-blue-600
            hover:bg-blue-700
            text-white
            shadow-xl
            flex
            items-center
            justify-center
            transition-all
            duration-200
            hover:scale-105
          "
        >

          <Bot
            size={28}
          />

        </button>

      )}


      {/* =================================================
          CHAT POPUP
      ================================================= */}

      {isOpen && (

        <div
          className="
            fixed
            right-6
            bottom-6
            z-[9999]
            w-[380px]
            max-w-[calc(100vw-32px)]
            h-[560px]
            max-h-[calc(100vh-32px)]
            bg-white
            border
            border-slate-200
            rounded-2xl
            shadow-2xl
            flex
            flex-col
            overflow-hidden
          "
        >

          {/* =============================================
              HEADER
          ============================================= */}

          <div
            className="
              px-5
              py-4
              bg-white
              border-b
              border-slate-200
              flex
              items-center
              justify-between
            "
          >

            <div className="flex items-center gap-3">

              <div
                className="
                  w-10
                  h-10
                  bg-blue-50
                  rounded-xl
                  flex
                  items-center
                  justify-center
                "
              >

                <Bot
                  size={21}
                  className="text-blue-600"
                />

              </div>


              <div>

                <h3
                  className="
                    text-sm
                    font-bold
                    text-slate-800
                  "
                >
                  Neighbour Management AI
                </h3>


                <p
                  className="
                    text-xs
                    text-slate-400
                    mt-0.5
                  "
                >
                  AI Assistant
                </p>

              </div>

            </div>


            <div className="flex items-center gap-1">

              <button
                type="button"
                onClick={() =>
                  setIsOpen(false)
                }
                aria-label="Minimize chatbot"
                className="
                  w-9
                  h-9
                  rounded-lg
                  flex
                  items-center
                  justify-center
                  text-slate-400
                  hover:text-slate-700
                  hover:bg-slate-100
                  transition
                "
              >

                <Minimize2
                  size={17}
                />

              </button>


              <button
                type="button"
                onClick={() =>
                  setIsOpen(false)
                }
                aria-label="Close chatbot"
                className="
                  w-9
                  h-9
                  rounded-lg
                  flex
                  items-center
                  justify-center
                  text-slate-400
                  hover:text-red-600
                  hover:bg-red-50
                  transition
                "
              >

                <X
                  size={18}
                />

              </button>

            </div>

          </div>


          {/* =============================================
              MESSAGES
          ============================================= */}

          <div
            className="
              flex-1
              overflow-y-auto
              p-4
              space-y-3
              bg-slate-50
            "
          >

            {messages.map(
              (
                item,
                index
              ) => (

                <div
                  key={index}
                  className={
                    item.role === "user"
                      ? "flex justify-end"
                      : "flex justify-start"
                  }
                >

                  <div
                    className={
                      item.role === "user"
                        ? `
                          max-w-[82%]
                          px-4
                          py-3
                          bg-blue-600
                          text-white
                          rounded-2xl
                          rounded-br-md
                          text-sm
                          leading-5
                        `
                        : `
                          max-w-[82%]
                          px-4
                          py-3
                          bg-white
                          border
                          border-slate-200
                          text-slate-700
                          rounded-2xl
                          rounded-bl-md
                          text-sm
                          leading-5
                        `
                    }
                  >

                    {item.text}

                  </div>

                </div>

              )
            )}


            {/* =========================================
                LOADING
            ========================================= */}

            {loading && (

              <div className="flex justify-start">

                <div
                  className="
                    px-4
                    py-3
                    bg-white
                    border
                    border-slate-200
                    rounded-2xl
                    rounded-bl-md
                  "
                >

                  <div className="flex gap-1">

                    <span
                      className="
                        w-2
                        h-2
                        bg-slate-400
                        rounded-full
                        animate-bounce
                      "
                    />

                    <span
                      className="
                        w-2
                        h-2
                        bg-slate-400
                        rounded-full
                        animate-bounce
                      "
                      style={{
                        animationDelay:
                          "150ms",
                      }}
                    />

                    <span
                      className="
                        w-2
                        h-2
                        bg-slate-400
                        rounded-full
                        animate-bounce
                      "
                      style={{
                        animationDelay:
                          "300ms",
                      }}
                    />

                  </div>

                </div>

              </div>

            )}

          </div>


          {/* =============================================
              QUICK COMMANDS
          ============================================= */}

          <div
            className="
              px-4
              pt-3
              bg-white
              border-t
              border-slate-100
            "
          >

            <div className="flex gap-2 overflow-x-auto pb-2">

              <button
                type="button"
                onClick={() =>
                  setMessage(
                    "Validate neighbours in Odisha JC_Bhubaneswar"
                  )
                }
                className="
                  whitespace-nowrap
                  px-3
                  py-1.5
                  bg-slate-50
                  border
                  border-slate-200
                  rounded-lg
                  text-xs
                  text-slate-600
                  hover:bg-blue-50
                  hover:text-blue-600
                  transition
                "
              >

                Validate

              </button>


              <button
                type="button"
                onClick={() =>
                  setMessage(
                    "Preview cleanup for Maharashtra JC_Mumbai with minimum retention of 2 neighbours"
                  )
                }
                className="
                  whitespace-nowrap
                  px-3
                  py-1.5
                  bg-slate-50
                  border
                  border-slate-200
                  rounded-lg
                  text-xs
                  text-slate-600
                  hover:bg-blue-50
                  hover:text-blue-600
                  transition
                "
              >

                Preview Cleanup

              </button>


              <button
                type="button"
                onClick={() =>
                  setMessage(
                    "Start cleanup for Maharashtra JC_Mumbai with minimum retention of 2 neighbours"
                  )
                }
                className="
                  whitespace-nowrap
                  px-3
                  py-1.5
                  bg-slate-50
                  border
                  border-slate-200
                  rounded-lg
                  text-xs
                  text-slate-600
                  hover:bg-blue-50
                  hover:text-blue-600
                  transition
                "
              >

                Start Cleanup

              </button>

            </div>

          </div>


          {/* =============================================
              INPUT
          ============================================= */}

          <form
            onSubmit={
              handleSubmit
            }
            className="
              p-4
              bg-white
              border-t
              border-slate-100
            "
          >

            <div className="flex gap-2">

              <input
                type="text"
                value={message}
                onChange={
                  (event) =>
                    setMessage(
                      event.target.value
                    )
                }
                placeholder="Ask the AI..."
                disabled={loading}
                className="
                  flex-1
                  min-w-0
                  px-3
                  py-3
                  bg-slate-50
                  border
                  border-slate-200
                  rounded-xl
                  outline-none
                  text-sm
                  text-slate-700
                  placeholder:text-slate-400
                  focus:bg-white
                  focus:border-blue-400
                  focus:ring-2
                  focus:ring-blue-100
                "
              />


              <button
                type="submit"
                disabled={
                  loading ||
                  !message.trim()
                }
                aria-label="Send message"
                className="
                  w-11
                  h-11
                  flex-shrink-0
                  rounded-xl
                  bg-blue-600
                  hover:bg-blue-700
                  text-white
                  flex
                  items-center
                  justify-center
                  transition
                  disabled:opacity-50
                  disabled:cursor-not-allowed
                "
              >

                <Send
                  size={17}
                />

              </button>

            </div>

          </form>

        </div>

      )}

    </>

  );

}


export default FloatingChatbot;
